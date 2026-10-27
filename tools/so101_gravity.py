#!/usr/bin/env python3
"""Gravity-only SO-101 estimate from the pinned upstream URDF; not motor control."""
import argparse
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

URDF = Path(__file__).resolve().parents[1] / 'reference/SO-ARM100/Simulation/SO101/so101_new_calib.urdf'
G = 9.80665


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def point(t, p):
    return [sum(t[i][k] * p[k] for k in range(3)) + t[i][3] for i in range(3)]


def vector(t, p):
    return [sum(t[i][k] * p[k] for k in range(3)) for i in range(3)]


def transform(xyz=(0, 0, 0), rpy=(0, 0, 0)):
    r, p, y = rpy
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    return [[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr, xyz[0]],
            [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr, xyz[1]],
            [-sp, cp*sr, cp*cr, xyz[2]], [0, 0, 0, 1]]


def axis_rotation(axis, angle):
    norm = math.sqrt(sum(v*v for v in axis))
    if not norm:
        raise ValueError('Zero rotation axis')
    x, y, z = (v/norm for v in axis)
    c, s, q = math.cos(angle), math.sin(angle), 1-math.cos(angle)
    return [[c+x*x*q, x*y*q-z*s, x*z*q+y*s, 0],
            [y*x*q+z*s, c+y*y*q, y*z*q-x*s, 0],
            [z*x*q-y*s, z*y*q+x*s, c+z*z*q, 0], [0, 0, 0, 1]]


def values(element, attr, default='0 0 0'):
    return [float(v) for v in (element.get(attr, default) if element is not None else default).split()]


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def calculate(urdf, angles, payload_kg=0.0):
    if not math.isfinite(payload_kg) or payload_kg < 0:
        raise ValueError('Payload mass must be finite and nonnegative')
    xml = ET.parse(urdf).getroot()
    links = {e.get('name'): e for e in xml.findall('link')}
    joints = xml.findall('joint')
    names = {j.get('name') for j in joints if j.get('type') == 'revolute'}
    if set(angles) - names:
        raise ValueError(f'Unknown revolute joint(s): {sorted(set(angles)-names)}')
    children = {name: [] for name in links}
    child_names = set()
    for j in joints:
        parent = j.find('parent').get('link'); child = j.find('child').get('link')
        children[parent].append((j, child)); child_names.add(child)
    roots = set(links) - child_names
    if len(roots) != 1:
        raise ValueError('URDF must have exactly one root link')
    root = roots.pop()
    points = []
    joint_frames = {}
    descendants = {}

    def visit(name, t):
        link = links[name]; inertial = link.find('inertial'); subtree = []
        if inertial is not None and inertial.find('mass') is not None:
            m = float(inertial.find('mass').get('value'))
            pos = point(t, values(inertial.find('origin'), 'xyz'))
            item = (name, m, pos); points.append(item); subtree.append(item)
        if name == 'gripper_frame_link' and payload_kg:
            item = ('hypothetical_payload', payload_kg, point(t, [0, 0, 0]))
            points.append(item); subtree.append(item)
        for j, child in children[name]:
            kind = j.get('type'); origin = j.find('origin')
            jt = mul(t, transform(values(origin, 'xyz'), values(origin, 'rpy')))
            if kind == 'revolute':
                angle = math.radians(angles.get(j.get('name'), 0.0))
                lim = j.find('limit')
                if not math.isfinite(angle) or angle < float(lim.get('lower'))-1e-10 or angle > float(lim.get('upper'))+1e-10:
                    raise ValueError(f'Joint {j.get("name")} is outside URDF limits')
                axis = values(j.find('axis'), 'xyz', '1 0 0')
                n = math.sqrt(sum(v*v for v in axis)); axis = [v/n for v in axis]
                joint_frames[j.get('name')] = (point(jt, [0, 0, 0]), vector(jt, axis))
                child_t = mul(jt, axis_rotation(axis, angle))
            elif kind == 'fixed':
                child_t = jt
            else:
                raise ValueError(f'Unsupported joint type: {kind}')
            sub = visit(child, child_t)
            if kind == 'revolute': descendants[j.get('name')] = sub
            subtree.extend(sub)
        return subtree

    visit(root, transform())
    mass = sum(m for _, m, _ in points)
    com = [sum(m*p[i] for _, m, p in points)/mass for i in range(3)]
    torques = {}
    for name, (pivot, axis) in joint_frames.items():
        total = 0.0
        for _, m, p in descendants[name]:
            moment = cross([p[i]-pivot[i] for i in range(3)], [0, 0, -m*G])
            total += sum(moment[i]*axis[i] for i in range(3))
        torques[name] = total
    return {'root_link': root, 'assumed_gravity_m_s2': [0, 0, -G], 'payload_at_gripper_frame_kg': payload_kg,
            'angles_deg': {n: angles.get(n, 0.0) for n in sorted(names)},
            'total_mass_kg': mass, 'center_of_mass_m_in_base_frame': com,
            'gravity_force_N': [0, 0, -mass*G],
            'gravity_moment_at_base_origin_Nm': [-mass*G*com[1], mass*G*com[0], 0],
            'gravity_torque_about_joint_axes_Nm': torques}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--joint', action='append', default=[], metavar='NAME=DEGREES')
    parser.add_argument('--payload-kg', type=float, default=0.0, help='Hypothetical point mass at gripper frame')
    args = parser.parse_args()
    angles = {}
    for item in args.joint:
        try:
            name, val = item.split('=', 1)
            if name in angles: raise ValueError('duplicate joint')
            angles[name] = float(val)
        except ValueError as exc:
            parser.error(f'Invalid joint setting {item!r}: {exc}')
    try:
        print(json.dumps(calculate(URDF, angles, args.payload_kg), indent=2))
    except (ValueError, ZeroDivisionError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
