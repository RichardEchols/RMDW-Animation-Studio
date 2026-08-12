import bpy
import math

# ---- Clear the scene ----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ---- RMDW crimson metallic sphere (high poly) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0), segments=64, ring_count=32)
sphere = bpy.context.object
sphere.name = "RMDWSphere"
mat = bpy.data.materials.new(name="RMDWMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.694, 0.118, 0.184, 1.0)  # #B11E2F
bsdf.inputs["Metallic"].default_value = 0.9
bsdf.inputs["Roughness"].default_value = 0.15
sphere.data.materials.append(mat)
bpy.ops.object.select_all(action='DESELECT')
sphere.select_set(True)
bpy.context.view_layer.objects.active = sphere
bpy.ops.object.shade_smooth()

# ---- "RMDW" text (rotated to face camera, above sphere) ----
bpy.ops.object.text_add(location=(0, 0, 1.9))
txt = bpy.context.object
txt.name = "RMDWText"
txt.data.body = "RMDW"
txt.data.align_x = 'CENTER'
txt.data.size = 1.0
txt.data.extrude = 0.12
txt.data.bevel_depth = 0.02
txt.rotation_euler = (math.radians(90), 0, 0)  # face the camera (+Y)
tmat = bpy.data.materials.new(name="TextMat")
tmat.use_nodes = True
# Emissive white text — guaranteed bright against the dark background
for n in list(tmat.node_tree.nodes):
    tmat.node_tree.nodes.remove(n)
tout = tmat.node_tree.nodes.new('ShaderNodeOutputMaterial')
temit = tmat.node_tree.nodes.new('ShaderNodeEmission')
temit.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
temit.inputs['Strength'].default_value = 3.0
tmat.node_tree.links.new(temit.outputs['Emission'], tout.inputs['Surface'])
txt.data.materials.append(tmat)

# ---- Camera (fixed, level, frames sphere + text) ----
bpy.ops.object.camera_add(location=(0, -9.5, 1.5))
cam = bpy.context.object
cam.name = "MainCam"
cam.rotation_euler = (math.radians(90), 0, 0)  # look along +Y at the scene
bpy.context.scene.camera = cam

# ---- Lighting (balanced) ----
bpy.ops.object.light_add(type='SUN', location=(4, 4, 8))
sun = bpy.context.object
sun.data.energy = 2.0
bpy.ops.object.light_add(type='AREA', location=(-4, -4, 3))
area = bpy.context.object
area.data.energy = 80.0
bpy.ops.object.light_add(type='AREA', location=(0, 3, -2))
fill = bpy.context.object
fill.data.energy = 40.0

# ---- Animate: sphere rotates, text bobs ----
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 180  # 6 seconds at 30fps

# Sphere rotation
sphere.rotation_euler = (0, 0, 0)
sphere.keyframe_insert(data_path="rotation_euler", frame=1)
sphere.rotation_euler = (0, math.radians(360), 0)
sphere.keyframe_insert(data_path="rotation_euler", frame=180)

# Text gentle bob
txt.location = (0, 0, 1.9)
txt.keyframe_insert(data_path="location", frame=1)
txt.location = (0, 0, 2.15)
txt.keyframe_insert(data_path="location", frame=90)
txt.location = (0, 0, 1.9)
txt.keyframe_insert(data_path="location", frame=180)

# ---- Render settings (EEVEE, 1080p, 30fps, PNG frames) ----
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "/tmp/rmdw_3d_frames/frame_"
scene.render.film_transparent = False

# Dark world background
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.11, 0.11, 0.11, 1.0)  # #1C1C1C
    bg.inputs[1].default_value = 1.0

# Render animation
bpy.ops.render.render(animation=True)
print("RENDER_DONE")
