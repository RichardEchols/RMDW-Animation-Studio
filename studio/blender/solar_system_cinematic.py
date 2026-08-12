import bpy
import math
import random

# ============================================================
# CINEMATIC SOLAR SYSTEM — v2
# Stars, glowing sun, orbital trails, textured planets,
# asteroid belt, camera motion, depth of field.
# ============================================================

# ---- Clear the scene ----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ---- Scene render settings ----
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "/tmp/solar2_frames/frame_"
scene.render.film_transparent = False

# Enable EEVEE bloom for the sun glow (removed in 5.2 API — use emissive halo instead)
# scene.eevee.use_bloom = True
# scene.eevee.bloom_intensity = 1.2
# scene.eevee.bloom_radius = 0.8
# scene.eevee.bloom_threshold = 0.8

# ---- Deep space background (gradient via world) ----
world = bpy.data.worlds["World"]
world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
wout = nt.nodes.new('ShaderNodeOutputWorld')
wbg = nt.nodes.new('ShaderNodeBackground')
wbg.inputs[0].default_value = (0.01, 0.01, 0.03, 1.0)  # deep space
wbg.inputs[1].default_value = 1.0
nt.links.new(wbg.outputs['Background'], wout.inputs['Surface'])

# ---- Stars (scattered emissive spheres — reliable rendering) ----
import random as _rnd
_rnd.seed(42)
star_mat = bpy.data.materials.new(name="StarMat")
star_mat.use_nodes = True
for n in list(star_mat.node_tree.nodes):
    star_mat.node_tree.nodes.remove(n)
so = star_mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
se = star_mat.node_tree.nodes.new('ShaderNodeEmission')
se.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
se.inputs['Strength'].default_value = 5.0
star_mat.node_tree.links.new(se.outputs['Emission'], so.inputs['Surface'])

for i in range(250):
    # random direction on a sphere of radius ~48
    theta = _rnd.uniform(0, 2 * math.pi)
    phi = math.acos(_rnd.uniform(-1, 1))
    r = _rnd.uniform(45, 52)
    loc = (r * math.sin(phi) * math.cos(theta),
           r * math.sin(phi) * math.sin(theta),
           r * math.cos(phi))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=_rnd.uniform(0.08, 0.2), location=loc, segments=8, ring_count=4)
    s = bpy.context.object
    s.name = f"Star_{i}"
    s.data.materials.append(star_mat)
    s.visible_shadow = False

# ---- The Sun (emissive, with glow via bloom) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0), segments=64, ring_count=32)
sun = bpy.context.object
sun.name = "Sun"
sunmat = bpy.data.materials.new(name="SunMat")
sunmat.use_nodes = True
for n in list(sunmat.node_tree.nodes):
    sunmat.node_tree.nodes.remove(n)
sout = sunmat.node_tree.nodes.new('ShaderNodeOutputMaterial')
semit = sunmat.node_tree.nodes.new('ShaderNodeEmission')
semit.inputs['Color'].default_value = (1.0, 0.85, 0.5, 1.0)  # warm
semit.inputs['Strength'].default_value = 8.0
sunmat.node_tree.links.new(semit.outputs['Emission'], sout.inputs['Surface'])
sun.data.materials.append(sunmat)
bpy.ops.object.select_all(action='DESELECT')
sun.select_set(True)
bpy.context.view_layer.objects.active = sun
bpy.ops.object.shade_smooth()

# ---- Sun glow halo (large soft emissive sphere) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=2.2, location=(0, 0, 0), segments=48, ring_count=24)
halo = bpy.context.object
halo.name = "SunHalo"
halomat = bpy.data.materials.new(name="SunHaloMat")
halomat.use_nodes = True
for n in list(halomat.node_tree.nodes):
    halomat.node_tree.nodes.remove(n)
hout = halomat.node_tree.nodes.new('ShaderNodeOutputMaterial')
# Mix transparent + emission for a soft glow
hmix = halomat.node_tree.nodes.new('ShaderNodeMixShader')
htrans = halomat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
hemit = halomat.node_tree.nodes.new('ShaderNodeEmission')
hemit.inputs['Color'].default_value = (1.0, 0.8, 0.4, 1.0)
hemit.inputs['Strength'].default_value = 3.0
# Fac controls glow strength (0.5 = half glow)
hmix.inputs['Fac'].default_value = 0.5
halomat.node_tree.links.new(htrans.outputs['BSDF'], hmix.inputs[1])
halomat.node_tree.links.new(hemit.outputs['Emission'], hmix.inputs[2])
halomat.node_tree.links.new(hmix.outputs['Shader'], hout.inputs['Surface'])
halo.data.materials.append(halomat)
# Make halo not cast shadows
halo.visible_shadow = False

# ---- Helper: make a planet with optional procedural texture ----
def make_planet(name, radius, color, loc, texture_type=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=48, ring_count=24)
    obj = bpy.context.object
    obj.name = name
    mat = bpy.data.materials.new(name=f"{name}Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.5
    # Add procedural texture (bands for gas giants, noise for rocky)
    if texture_type == "bands":
        # striped bands via a wave texture
        tex = mat.node_tree.nodes.new('ShaderNodeTexWave')
        tex.wave_type = 'BANDS'
        tex.bands_direction = 'Z'
        tex.inputs['Scale'].default_value = 3.0
        tex.wave_profile = 'SIN'
        col = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        col.inputs[1].default_value = color
        col.inputs[2].default_value = (color[0]*0.6, color[1]*0.6, color[2]*0.6, 1.0)
        mat.node_tree.links.new(tex.outputs['Fac'], col.inputs['Fac'])
        mat.node_tree.links.new(col.outputs['Color'], bsdf.inputs['Base Color'])
    elif texture_type == "noise":
        tex = mat.node_tree.nodes.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = 8.0
        tex.inputs['Detail'].default_value = 6.0
        col = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        col.inputs[1].default_value = color
        col.inputs[2].default_value = (color[0]*0.5, color[1]*0.5, color[2]*0.5, 1.0)
        mat.node_tree.links.new(tex.outputs['Fac'], col.inputs['Fac'])
        mat.node_tree.links.new(col.outputs['Color'], bsdf.inputs['Base Color'])
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    return obj

# ---- Planets with textures ----
mercury = make_planet("Mercury", 0.12, (0.6, 0.6, 0.6, 1.0), (2.2, 0, 0), "noise")
venus = make_planet("Venus", 0.2, (0.9, 0.7, 0.4, 1.0), (3.2, 0, 0), "noise")
earth = make_planet("Earth", 0.22, (0.2, 0.5, 0.9, 1.0), (4.2, 0, 0), "noise")
mars = make_planet("Mars", 0.16, (0.8, 0.3, 0.2, 1.0), (5.2, 0, 0), "noise")
jupiter = make_planet("Jupiter", 0.5, (0.8, 0.6, 0.4, 1.0), (6.8, 0, 0), "bands")
saturn = make_planet("Saturn", 0.42, (0.85, 0.75, 0.5, 1.0), (8.4, 0, 0), "bands")
uranus = make_planet("Uranus", 0.34, (0.5, 0.8, 0.8, 1.0), (9.8, 0, 0), "noise")
neptune = make_planet("Neptune", 0.32, (0.2, 0.4, 0.9, 1.0), (11.0, 0, 0), "noise")

# ---- Saturn's rings (detailed, parented) ----
bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.05, location=(8.4, 0, 0))
rings = bpy.context.object
rings.name = "SaturnRings"
rings.rotation_euler = (math.radians(75), 0, 0)
rmat = bpy.data.materials.new(name="RingMat")
rmat.use_nodes = True
rbsdf = rmat.node_tree.nodes.get("Principled BSDF")
rbsdf.inputs["Base Color"].default_value = (0.75, 0.65, 0.5, 1.0)
rbsdf.inputs["Roughness"].default_value = 0.6
rings.data.materials.append(rmat)
# Keyframe ring to follow Saturn's orbit (same path)

# ---- Orbital trail rings (visible paths) ----
trail_mats = {}
def make_orbit_trail(dist, color):
    bpy.ops.mesh.primitive_torus_add(major_radius=dist, minor_radius=0.008, location=(0, 0, 0))
    trail = bpy.context.object
    trail.name = f"Orbit_{dist}"
    mat = bpy.data.materials.new(name=f"TrailMat_{dist}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.8
    trail.data.materials.append(mat)
    return trail

# Faint orbit trails for each planet
for dist in [2.2, 3.2, 4.2, 5.2, 6.8, 8.4, 9.8, 11.0]:
    make_orbit_trail(dist, (0.3, 0.3, 0.4, 1.0))

# ---- Asteroid belt (particles between Mars and Jupiter) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(0, 0, 0))
asteroid = bpy.context.object
asteroid.name = "Asteroid"
amat = bpy.data.materials.new(name="AsteroidMat")
amat.use_nodes = True
absdf = amat.node_tree.nodes.get("Principled BSDF")
absdf.inputs["Base Color"].default_value = (0.5, 0.45, 0.4, 1.0)
asteroid.data.materials.append(amat)
# Particle system for the belt
psys = asteroid.modifiers.new(name="Belt", type='PARTICLE_SYSTEM')
ps = psys.particle_system
ps.settings.count = 3000
ps.settings.frame_start = 1
ps.settings.frame_end = 1
ps.settings.lifetime = 1000
ps.settings.emit_from = 'VOLUME'
ps.settings.particle_size = 0.02
# Distribute in a torus between Mars (5.2) and Jupiter (6.8)
# Use a vertex group on a flattened torus instead — simpler: use a disc
bpy.ops.object.select_all(action='DESELECT')
asteroid.select_set(True)
bpy.context.view_layer.objects.active = asteroid
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='ONLY_FACE')
bpy.ops.object.mode_set(mode='OBJECT')
# Scatter vertices in a ring between 5.6 and 6.4
import bmesh
# Rebuild as a disc of vertices
bpy.ops.mesh.primitive_grid_add(size=12, x_subdivisions=40, y_subdivisions=40, location=(0,0,0))
belt_grid = bpy.context.object
belt_grid.name = "BeltGrid"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='ONLY_FACE')
bpy.ops.object.mode_set(mode='OBJECT')
# Move grid vertices into a ring
for v in belt_grid.data.vertices:
    x, y = v.co.x, v.co.y
    r = math.sqrt(x*x + y*y)
    if 5.6 <= r <= 6.4:
        # keep, add slight z jitter
        v.co.z = random.uniform(-0.1, 0.1)
    else:
        v.co = (0, 0, 0)  # collapse outside ring
# Particle system on the belt grid
psys2 = belt_grid.modifiers.new(name="Belt2", type='PARTICLE_SYSTEM')
ps2 = psys2.particle_system
ps2.settings.count = 4000
ps2.settings.frame_start = 1
ps2.settings.frame_end = 1
ps2.settings.lifetime = 1000
ps2.settings.emit_from = 'VERT'
ps2.settings.particle_size = 0.02
belt_grid.data.materials.append(amat)

# ---- Camera (cinematic slow dolly, tracks the sun) ----
bpy.ops.object.camera_add(location=(0, -24, 16))
cam = bpy.context.object
cam.name = "SolarCam"
track = cam.constraints.new(type='TRACK_TO')
track.target = sun
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
bpy.context.scene.camera = cam
# Slow camera dolly for cinematic feel
cam.location = (0, -24, 16)
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (2, -26, 18)
cam.keyframe_insert(data_path="location", frame=180)

# ---- Lighting ----
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sunlight = bpy.context.object
sunlight.data.energy = 2.5

# ---- Animate: planets orbit ----
scene.frame_start = 1
scene.frame_end = 180

orbits = [
    (mercury, 2.2, 0.9),
    (venus, 3.2, 0.7),
    (earth, 4.2, 0.55),
    (mars, 5.2, 0.45),
    (jupiter, 6.8, 0.3),
    (saturn, 8.4, 0.22),
    (uranus, 9.8, 0.16),
    (neptune, 11.0, 0.12),
]

for planet, dist, speed in orbits:
    for frame, angle in [(1, 0), (90, math.pi * speed * 2), (180, math.pi * speed * 4)]:
        planet.location = (dist * math.cos(angle), dist * math.sin(angle), 0)
        planet.keyframe_insert(data_path="location", frame=frame)
    if planet.name == "Saturn":
        for frame, angle in [(1, 0), (90, math.pi * speed * 2), (180, math.pi * speed * 4)]:
            rings.location = (dist * math.cos(angle), dist * math.sin(angle), 0)
            rings.keyframe_insert(data_path="location", frame=frame)

# Render animation
bpy.ops.render.render(animation=True)
print("RENDER_DONE")
