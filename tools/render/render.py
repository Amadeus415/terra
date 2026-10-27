"""Render the README images from the STL meshes: blender -b --python render.py -- MESH_DIR OUT_DIR"""
import math
import sys

import bpy
from mathutils import Vector

mesh_dir, out_dir = sys.argv[sys.argv.index("--") + 1 :][:2]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1200
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"

try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = "GPU"
except Exception as e:  # noqa: BLE001
    print("GPU unavailable, using CPU:", e)


def material(name, rgb, rough=0.45, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m


MATS = {
    "quadruped": material("charcoal", (0.018, 0.018, 0.02), 0.5),
    "arm": material("bone", (0.82, 0.77, 0.66), 0.55),
    "plate": material("orange", (0.95, 0.32, 0.04), 0.4),
    "supports": material("orange2", (0.95, 0.32, 0.04), 0.4),
    "support-4mm": material("orange3", (0.95, 0.32, 0.04), 0.4),
    "support-8mm": material("orange4", (0.95, 0.32, 0.04), 0.4),
}


def load(name):
    bpy.ops.wm.stl_import(filepath=f"{mesh_dir}/{name}.stl", global_scale=0.001)
    obj = bpy.context.selected_objects[0]
    obj.name = name
    obj.data.materials.append(MATS[name])
    obj.data.shade_smooth()
    mod = obj.modifiers.new("edges", "EDGE_SPLIT")
    mod.split_angle = math.radians(32)
    return obj


OBJS = {n: load(n) for n in MATS}


def bounds(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


# Floor at the quadruped's feet, and a soft studio: a big key, a fill and a bright world.
lo, hi = bounds([OBJS["quadruped"]])
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, lo.z - 0.0005))
floor = bpy.context.object
floor.name = "floor"
floor.data.materials.append(material("floor", (0.82, 0.82, 0.8), 0.7))

world = bpy.data.worlds.new("studio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.85, 0.87, 0.92, 1)
bg.inputs["Strength"].default_value = 0.3


def light(name, loc, energy, size, rot):
    bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot)
    l = bpy.context.object
    l.name = name
    l.data.energy = energy
    l.data.size = size
    return l


light("key", (0.9, -0.8, 1.3), 140, 1.2, (math.radians(45), 0, math.radians(48)))
light("fill", (-1.1, -0.5, 0.7), 45, 1.6, (math.radians(65), 0, math.radians(-60)))
light("rim", (0.2, 1.2, 0.9), 70, 1.0, (math.radians(-55), 0, math.radians(10)))

cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 60
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam


def frame(objs, azimuth, elevation, fill=0.78, aim_shift=(0, 0, 0)):
    """Point the camera at the objects' centre from the given angles, far enough to fit them."""
    lo, hi = bounds(objs)
    centre = (lo + hi) / 2 + Vector(aim_shift)
    radius = (hi - lo).length / 2
    fov = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
    dist = radius / math.sin(fov / 2) / fill
    az, el = math.radians(azimuth), math.radians(elevation)
    cam.location = centre + Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el))) * dist
    direction = centre - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render(name, visible):
    for n, o in OBJS.items():
        o.hide_render = n not in visible
    scene.render.filepath = f"{out_dir}/{name}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", name)


robot = ["quadruped", "arm", "plate", "supports"]
frame([OBJS[n] for n in robot], azimuth=-38, elevation=16, fill=0.9)
render("terra-hero", robot)

frame([OBJS[n] for n in ("plate", "supports")], azimuth=-55, elevation=14, fill=0.42, aim_shift=(0, 0, 0.01))
render("terra-mount", robot)

# The two simulated supports side by side: 4 mm wall on the left, 8 mm on the right.
thin, thick = OBJS["support-4mm"], OBJS["support-8mm"]
for o in (thin, thick):
    lo, hi = bounds([o])
    o.location -= Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z - floor.location.z))
thin.location.x -= 0.03
thick.location.x += 0.03
bpy.context.view_layer.update()
scene.view_settings.exposure = -1.2
frame([thin, thick], azimuth=-30, elevation=22, fill=0.7)
render("terra-supports", ["support-4mm", "support-8mm"])
