import math
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'tools'))
import so101_gravity as calc


class GravityTests(unittest.TestCase):
    def test_one_meter_pendulum(self):
        model = '''<robot name="test"><link name="base"/><link name="arm"><inertial>
          <origin xyz="1 0 0"/><mass value="1"/></inertial></link>
          <joint name="hinge" type="revolute"><parent link="base"/><child link="arm"/>
          <axis xyz="0 1 0"/><limit lower="-3.14" upper="3.14"/></joint></robot>'''
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp) / 'test.urdf'; p.write_text(model)
            zero = calc.calculate(p, {})
            quarter = calc.calculate(p, {'hinge': 90})
        self.assertAlmostEqual(zero['gravity_torque_about_joint_axes_Nm']['hinge'], calc.G)
        self.assertAlmostEqual(zero['gravity_moment_at_base_origin_Nm'][1], calc.G)
        self.assertAlmostEqual(quarter['gravity_torque_about_joint_axes_Nm']['hinge'], 0, places=7)
        self.assertAlmostEqual(quarter['center_of_mass_m_in_base_frame'][2], -1)

    def test_upstream_torque_matches_potential_energy_derivative(self):
        angles = {'shoulder_pan': 13, 'shoulder_lift': -20, 'elbow_flex': 30, 'wrist_flex': 15, 'wrist_roll': -25, 'gripper': 10}
        original = calc.calculate(calc.URDF, angles, .1)
        h = 0.0001
        for name in angles:
            a = dict(angles); b = dict(angles)
            a[name] += h; b[name] -= h
            plus = calc.calculate(calc.URDF, a, .1); minus = calc.calculate(calc.URDF, b, .1)
            up = plus['total_mass_kg'] * calc.G * plus['center_of_mass_m_in_base_frame'][2]
            down = minus['total_mass_kg'] * calc.G * minus['center_of_mass_m_in_base_frame'][2]
            numerical = -(up-down) / (2*math.radians(h))
            self.assertAlmostEqual(original['gravity_torque_about_joint_axes_Nm'][name], numerical, places=7)

    def test_invalid_settings(self):
        for angles, payload in [({'shoulder_lift': 999}, 0), ({'typo': 0}, 0), ({}, -1), ({'gripper': float('nan')}, 0)]:
            with self.subTest(angles=angles, payload=payload), self.assertRaises(ValueError):
                calc.calculate(calc.URDF, angles, payload)


if __name__ == '__main__':
    unittest.main()
