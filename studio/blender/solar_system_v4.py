import bpy
import math
import os

# ============================================================
# CINEMATIC SOLAR SYSTEM — v4 (SPECTACULAR)
# Real 8k textures + Milky Way background + sun Glare glow
# + animated depth of field + parallax stars
# ============================================================

TEX = "/Users/richardecholsai7/Desktop/RMDW AI Consulting/Projects/animation-studio/assets/textures"

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
scene.render.filepath = "/tmp/solar4_frames/frame_"
scene.render.film_transparent = False

# ---- World: Milky Way starfield background (simple, robust) ----
world = bpy.data.worlds["World"]
world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
wout = nt.nodes.new('ShaderNodeOutputWorld')
wbg = nt.nodes.new('ShaderNodeBackground')
wbg.inputs[1].default_value = 1.0
wtex = nt.nodes.new('ShaderNodeTexImage')
wtex.image = bpy.data.images.load(os.path.join(TEX, "8k_stars_milky_way.jpg"))
wtex.image.colorspace_settings.name = 'sRGB'
wtex.projection = 'SPHERE'
# Milky Way texture directly drives the background color
nt.links.new(wtex.outputs['Color'], wbg.inputs['Color'])
nt.links.new(wbg.outputs['Background'], wout.inputs['Surface'])

# ---- Parallax stars (large emissive spheres at varying distances) ----
import random as _rnd
_rnd.seed(7)
star_mat = bpy.data.materials.new(name="StarMat")
star_mat.use_nodes = True
for n in list(star_mat.node_tree.nodes):
    star_mat.node_tree.nodes.remove(n)
so = star_mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
se = star_mat.node_tree.nodes.new('ShaderNodeEmission')
se.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
se.inputs['Strength'].default_value = 8.0
star_mat.node_tree.links.new(se.outputs['Emission'], so.inputs['Surface'])

for i in range(120):
    theta = _rnd.uniform(0, 2 * math.pi)
    phi = math.acos(_rnd.uniform(-1, 1))
    r = _rnd.uniform(40, 70)
    loc = (r * math.sin(phi) * math.cos(theta),
           r * math.sin(phi) * math.sin(theta),
           r * math.cos(phi))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=_rnd.uniform(0.15, 0.5), location=loc, segments=10, ring_count=6)
    s = bpy.context.object
    s.name = f"Star_{i}"
    s.data.materials.append(star_mat)
    s.visible_shadow = False

# ---- Helper: textured planet ----
def make_textured_planet(name, radius, texfile, loc):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=64, ring_count=32)
    obj = bpy.context.object
    obj.name = name
    mat = bpy.data.materials.new(name=f"{name}Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 0.7
    img = mat.node_tree.nodes.new('ShaderNodeTexImage')
    img.image = bpy.data.images.load(os.path.join(TEX, texfile))
    img.image.colorspace_settings.name = 'sRGB'
    mat.node_tree.links.new(img.outputs['Color'], bsdf.inputs['Base Color'])
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    return obj

# ---- The Sun (textured + emissive) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0), segments=64, ring_count=32)
sun = bpy.context.object
sun.name = "Sun"
sunmat = bpy.data.materials.new(name="SunMat")
sunmat.use_nodes = True
for n in list(sunmat.node_tree.nodes):
    sunmat.node_tree.nodes.remove(n)
sout = sunmat.node_tree.nodes.new('ShaderNodeOutputMaterial')
semit = sunmat.node_tree.nodes.new('ShaderNodeEmission')
simg = sunmat.node_tree.nodes.new('ShaderNodeTexImage')
simg.image = bpy.data.images.load(os.path.join(TEX, "sun_8k.jpg"))
simg.image.colorspace_settings.name = 'sRGB'
sstrength = sunmat.node_tree.nodes.new('ShaderNodeMath')
sstrength.operation = 'MULTIPLY'
sstrength.inputs[1].default_value = 8.0
sunmat.node_tree.links.new(simg.outputs['Color'], sstrength.inputs[0])
sunmat.node_tree.links.new(sstrength.outputs['Value'], semit.inputs['Strength'])
semit.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0)
sunmat.node_tree.links.new(semit.outputs['Emission'], sout.inputs['Surface'])
sun.data.materials.append(sunmat)
bpy.ops.object.select_all(action='DESELECT')
sun.select_set(True)
bpy.context.view_layer.objects.active = sun
bpy.ops.object.shade_smooth()

# ---- Sun glow halo ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=2.6, location=(0, 0, 0), segments=48, ring_count=24)
halo = bpy.context.object
halo.name = "SunHalo"
halomat = bpy.data.materials.new(name="SunHaloMat")
halomat.use_nodes = True
for n in list(halomat.node_tree.nodes):
    halomat.node_tree.nodes.remove(n)
hout = halomat.node_tree.nodes.new('ShaderNodeOutputMaterial')
hmix = halomat.node_tree.nodes.new('ShaderNodeMixShader')
htrans = halomat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
hemit = halomat.node_tree.nodes.new('ShaderNodeEmission')
hemit.inputs['Color'].default_value = (1.0, 0.8, 0.4, 1.0)
hemit.inputs['Strength'].default_value = 4.0
hmix.inputs['Fac'].default_value = 0.4
halomat.node_tree.links.new(htrans.outputs['BSDF'], hmix.inputs[1])
halomat.node_tree.links.new(hemit.outputs['Emission'], hmix.inputs[2])
halomat.node_tree.links.new(hmix.outputs['Shader'], hout.inputs['Surface'])
halo.data.materials.append(halomat)
halo.visible_shadow = False

# ---- Textured planets (8k) ----
mercury = make_textured_planet("Mercury", 0.12, "mercury_8k.jpg", (2.2, 0, 0))
venus = make_textured_planet("Venus", 0.2, "venus_surface_8k.jpg", (3.2, 0, 0))
earth = make_textured_planet("Earth", 0.22, "earth_daymap_8k.jpg", (4.2, 0, 0))
mars = make_textured_planet("Mars", 0.16, "mars_8k.jpg", (5.2, 0, 0))
jupiter = make_textured_planet("Jupiter", 0.5, "jupiter_8k.jpg", (6.8, 0, 0))
saturn = make_textured_planet("Saturn", 0.42, "saturn_8k.jpg", (8.4, 0, 0))
uranus = make_textured_planet("Uranus", 0.34, "uranus.jpg", (9.8, 0, 0))
neptune = make_textured_planet("Neptune", 0.32, "neptune.jpg", (11.0, 0, 0))

# ---- Saturn's rings (textured with alpha) ----
bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.06, location=(8.4, 0, 0), major_segments=128, minor_segments=32)
rings = bpy.context.object
rings.name = "SaturnRings"
rings.rotation_euler = (math.radians(75), 0, 0)
rmat = bpy.data.materials.new(name="RingMat")
rmat.use_nodes = True
rbsdf = rmat.node_tree.nodes.get("Principled BSDF")
rbsdf.inputs["Roughness"].default_value = 0.7
rimg = rmat.node_tree.nodes.new('ShaderNodeTexImage')
rimg.image = bpy.data.images.load(os.path.join(TEX, "saturn_ring_alpha_8k.png"))
rimg.image.colorspace_settings.name = 'sRGB'
rmat.node_tree.links.new(rimg.outputs['Color'], rbsdf.inputs['Base Color'])
rmat.blend_method = 'BLEND'
rmat.node_tree.links.new(rimg.outputs['Alpha'], rbsdf.inputs['Alpha'])
rings.data.materials.append(rmat)

# ---- Camera (cinematic dolly with animated depth of field) ----
bpy.ops.object.camera_add(location=(0, -24, 16))
cam = bpy.context.object
cam.name = "SolarCam"
track = cam.constraints.new(type='TRACK_TO')
track.target = sun
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
bpy.context.scene.camera = cam
cam.location = (0, -24, 16)
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (2, -26, 18)
cam.keyframe_insert(data_path="location", frame=180)
# Depth of field: focus on the sun, shallow for cinematic feel
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
cam.data.dof.focus_object = sun

# ---- Lighting ----
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sunlight = bpy.context.object
sunlight.data.energy = 3.0

# ---- Animate: planets orbit ----
scene.frame_start = 1
scene.frame_end = 180
orbits = [
    (mercury, 2.2, 0.9), (venus, 3.2, 0.7), (earth, 4.2, 0.55), (mars, 5.2, 0.45),
    (jupiter, 6.8, 0.3), (saturn, 8.4, 0.22), (uranus, 9.8, 0.16), (neptune, 11.0, 0.12),
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
