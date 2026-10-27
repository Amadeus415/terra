"""Export STL meshes for the README renders: the quadruped, the SO-101 arm placed as in the Fusion
placement study, and the thick mount concept rebuilt from tools/fusion_thick_mount_concept.py.

Output frame is Z-up (Blender). The Fusion study frame is Y-up, so everything is rotated +90 about X.
"""
import sys
import cadquery as cq

ROOT = "/Users/colenba/Documents/ChatGPT/robotics_terra"
OUT = sys.argv[1]


def bbox(wp):
    return cq.Compound.makeCompound(wp.vals()).BoundingBox()


def show(name, wp):
    b = bbox(wp)
    print(f"{name}: x {b.xmin:.1f}..{b.xmax:.1f}  y {b.ymin:.1f}..{b.ymax:.1f}  z {b.zmin:.1f}..{b.zmax:.1f}")


def export(name, wp, tol=0.05, ang=0.15):
    cq.exporters.export(wp, f"{OUT}/{name}.stl", tolerance=tol, angularTolerance=ang)
    print("wrote", name)


# Study frame (Y up) -> Blender frame (Z up): rotate +90 about X, so (x, y, z) -> (x, -z, y).
def z_up(wp):
    return wp.rotate((0, 0, 0), (1, 0, 0), 90)


# --- Quadruped: kept in its source position, as in the study.
quad = cq.importers.importStep(f"{ROOT}/reference/quadruped-v2/quadruped_v2.step")
show("quad (study frame)", quad)

# --- Arm: the study's occurrence transform is rotate -90 about X, then sit the base on the raised plate top.
arm = cq.importers.importStep(f"{ROOT}/reference/SO-ARM100/STEP/SO101/SO101 Assembly.step")
show("arm (native)", arm)
arm = arm.rotate((0, 0, 0), (1, 0, 0), -90)
b = bbox(arm)
PLATE_TOP = 80.384
arm = arm.translate((0, PLATE_TOP - b.ymin, 0))
show("arm (study frame, expect x +-55.5, z -93.6..226.8)", arm)

# --- Mount concept, built directly in the Blender frame: bx = x, by = -z, bz = y.
PLATE_BOTTOM = 76.384
plate = cq.Workplane("XY").box(120, 100, 4, centered=False).translate((-60, -40, PLATE_BOTTOM))
arm_holes = [(x, -z) for x, z in [(-31.75, -45.42), (31.75, -45.42), (-27.78, 24.35), (27.78, 24.35)]]
support_holes = [(x, -z) for x in (-51.5, 51.5) for z in (-34, 24)]
plate = plate.faces(">Z").workplane().pushPoints(arm_holes).hole(5.2).faces(">Z").workplane().pushPoints(support_holes).hole(3.4)


def support(side_z, top_z, width):
    """One L-shaped support on the +X side; wall 8 mm thick, flange 4 mm."""
    y0 = -side_z - width / 2
    wall = cq.Workplane("XY").box(8, width, PLATE_BOTTOM - 10.5, centered=False).translate((56.5, y0, 10.5))
    flange = cq.Workplane("XY").box(64.5 - 36, width, 4, centered=False).translate((36, y0, 72.384))
    body = wall.union(flange)
    side_hole = cq.Solid.makeCylinder(1.7, 30, cq.Vector(50, -side_z, 14.5), cq.Vector(1, 0, 0))
    top_hole = cq.Solid.makeCylinder(1.7, 30, cq.Vector(51.5, -top_z, 60), cq.Vector(0, 0, 1))
    return body.cut(cq.Workplane("XY").add(side_hole)).cut(cq.Workplane("XY").add(top_hole))


supports = cq.Workplane("XY")
for side_z, top_z, width in [(-24.65, -34, 28), (24, 24, 12)]:
    s = support(side_z, top_z, width)
    supports = supports.add(s.vals()).add(s.mirror("YZ").vals())

# --- The two simulated single supports (4 mm and 8 mm walls), from the exported STEP files.
thin = cq.importers.importStep(f"{ROOT}/outputs/raised-front-support-SIMULATION-ONLY.step")
thick = cq.importers.importStep(f"{ROOT}/outputs/thick-front-support-SIMULATION-ONLY.step")
show("thin support (study frame)", thin)
show("thick support (study frame)", thick)

export("quadruped", z_up(quad), tol=0.1, ang=0.25)
export("arm", z_up(arm), tol=0.08, ang=0.2)
export("plate", plate, tol=0.02, ang=0.1)
export("supports", supports, tol=0.02, ang=0.1)
export("support-4mm", z_up(thin), tol=0.02, ang=0.1)
export("support-8mm", z_up(thick), tol=0.02, ang=0.1)
