"""Test : NUBO ultra-réaliste dans Blender (fourrure Cycles). Usage : python nubo_test.py sortie.png [largeur] [samples]"""
import math
import sys
import time

import bpy
from mathutils import Vector

out = sys.argv[1]
W = int(sys.argv[2]) if len(sys.argv) > 2 else 540
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 64

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = W, int(W * 16 / 9)
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"


def mat(name, color, rough=0.5, spec=0.5, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    return m


ORANGE = (1.0, 0.28, 0.035)

# --- corps
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(0, 0, 1.0))
body = bpy.context.object
body.scale = (1.0, 0.92, 0.95)
bpy.ops.object.shade_smooth()
body.data.materials.append(mat("skin", ORANGE, 0.8))

# fourrure (particules cheveux)
ps_mod = body.modifiers.new("fur", "PARTICLE_SYSTEM")
pset = ps_mod.particle_system.settings
pset.type = "HAIR"
pset.count = 12000
pset.hair_length = 0.2
pset.use_advanced_hair = True
pset.child_type = "INTERPOLATED"
pset.child_percent = 18
pset.rendered_child_count = 18
pset.clump_factor = 0.15
pset.roughness_1 = 0.03
pset.roughness_endpoint = 0.05
pset.roughness_2 = 0.02
pset.root_radius = 0.012
pset.tip_radius = 0.002
pset.radius_scale = 0.35
pset.child_length = 0.95
pset.child_length_threshold = 0.3
fur = bpy.data.materials.new("fur")
fur.use_nodes = True
nt = fur.node_tree
for n in list(nt.nodes):
    if n.type == "BSDF_PRINCIPLED":
        nt.nodes.remove(n)
hair = nt.nodes.new("ShaderNodeBsdfHairPrincipled")
hair.parametrization = "MELANIN"
hair.inputs["Melanin"].default_value = 0.16
hair.inputs["Melanin Redness"].default_value = 1.0
hair.inputs["Tint"].default_value = (1.0, 0.55, 0.3, 1)
hair.inputs["Roughness"].default_value = 0.35
hair.inputs["Radial Roughness"].default_value = 0.5
nt.links.new(hair.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
body.data.materials.append(fur)
pset.material = 2

# --- yeux
eye_m = mat("eye", (0.06, 0.025, 0.012), 0.05, coat=1.0)
for sx in (-0.33, 0.33):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.21, location=(sx, -0.98, 1.2))
    e = bpy.context.object
    e.scale = (1, 0.85, 1.08)
    bpy.ops.object.shade_smooth()
    e.data.materials.append(eye_m)

# --- sourire (arc)
scu = bpy.data.curves.new("smile", "CURVE")
scu.dimensions = "3D"
sp_ = scu.splines.new("POLY")
arc = [(math.cos(a) * 0.075, -1.14, 0.99 - math.sin(a) * 0.04) for a in [math.pi * (0.15 + 0.7 * i / 15) for i in range(16)]]
sp_.points.add(len(arc) - 1)
for p, c in zip(sp_.points, arc):
    p.co = (*c, 1)
scu.bevel_depth = 0.01
smo = bpy.data.objects.new("smile", scu)
sc.collection.objects.link(smo)
smo.data.materials.append(mat("smile", (0.12, 0.03, 0.01), 0.6))

# --- pieds et bras
for sx in (-0.42, 0.42):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(sx, -0.2, 0.12))
    f = bpy.context.object
    f.scale = (1, 1.3, 0.55)
    bpy.ops.object.shade_smooth()
    f.data.materials.append(mat("feet", (0.95, 0.24, 0.03), 0.85))
for sx in (-1, 1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(sx * 1.0, -0.1, 0.85))
    a = bpy.context.object
    a.scale = (0.7, 0.7, 1.3)
    a.rotation_euler = (0, math.radians(-25 * sx), 0)
    bpy.ops.object.shade_smooth()
    a.data.materials.append(mat("arm", (0.95, 0.26, 0.03), 0.85))

# --- mèche bouclée
cu = bpy.data.curves.new("tuft", "CURVE")
cu.dimensions = "3D"
spl = cu.splines.new("POLY")
pts = []
for i in range(60):
    u = i / 59
    if u < 0.5:
        pts.append((0, -0.1, 1.7 + u * 0.85))
    else:
        k = (u - 0.5) / 0.5
        a = k * 1.8 * math.pi
        r = 0.17 * (1 - 0.4 * k)
        pts.append((0.17 - math.cos(a) * r, -0.1, 2.12 + math.sin(a) * r))
spl.points.add(len(pts) - 1)
for p, c in zip(spl.points, pts):
    p.co = (*c, 1)
cu.bevel_depth = 0.045
cu.bevel_resolution = 6
tuft = bpy.data.objects.new("tuft", cu)
sc.collection.objects.link(tuft)
tuft.data.materials.append(mat("tuftm", (0.9, 0.22, 0.02), 0.9))

# --- décor
wall_m = mat("wall", (0.55, 0.45, 0.85), 0.9)
floor_m = bpy.data.materials.new("floor")
floor_m.use_nodes = True
fn = floor_m.node_tree
noise = fn.nodes.new("ShaderNodeTexWave")
noise.inputs["Scale"].default_value = 1.5
noise.inputs["Distortion"].default_value = 6
ramp = fn.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.35, 0.2, 0.12, 1)
ramp.color_ramp.elements[1].color = (0.6, 0.4, 0.25, 1)
fn.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
fb = fn.nodes["Principled BSDF"]
fn.links.new(ramp.outputs["Color"], fb.inputs["Base Color"])
fb.inputs["Roughness"].default_value = 0.35
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
bpy.context.object.data.materials.append(floor_m)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 3.0, 0), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(wall_m)

# --- lumières
bpy.ops.object.light_add(type="AREA", location=(-3, -4, 4))
key = bpy.context.object
key.data.energy = 900
key.data.size = 3
key.data.color = (1.0, 0.88, 0.75)
key.rotation_euler = (math.radians(55), 0, math.radians(-35))
bpy.ops.object.light_add(type="AREA", location=(3, -2, 2.5))
fill = bpy.context.object
fill.data.energy = 300
fill.data.size = 4
fill.data.color = (0.85, 0.8, 1.0)
fill.rotation_euler = (math.radians(60), 0, math.radians(50))
bpy.ops.object.light_add(type="AREA", location=(0, 2, 3.5))
rim = bpy.context.object
rim.data.energy = 600
rim.data.size = 2
rim.rotation_euler = (math.radians(-50), 0, 0)
world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.6, 0.55, 0.75, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
sc.world = world

# --- caméra
bpy.ops.object.camera_add(location=(0, -8.5, 1.6))
cam = bpy.context.object
cam.rotation_euler = (math.radians(88), 0, 0)
cam.data.lens = 50
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 7.4
cam.data.dof.aperture_fstop = 2.8
sc.camera = cam

sc.render.filepath = out
t = time.time()
bpy.ops.render.render(write_still=True)
print(f"RENDER_TIME {time.time() - t:.1f}s  {W}x{int(W * 16 / 9)} samples={SAMPLES}")
