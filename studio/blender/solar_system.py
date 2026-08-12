import bpy
import math

# ---- Clear the scene ----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ---- Helper to make a planet ----
def make_planet(name, radius, color, loc):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=32, ring_count=16)
    obj = bpy.context.object
    obj.name = name
    mat = bpy.data.materials.new(name=f"{name}Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.4
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    return obj

# ---- The Sun (emissive, glowing) ----
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0), segments=48, ring_count=24)
sun = bpy.context.object
sun.name = "Sun"
sunmat = bpy.data.materials.new(name="SunMat")
sunmat.use_nodes = True
for n in list(sunmat.node_tree.nodes):
    sunmat.node_tree.nodes.remove(n)
sout = sunmat.node_tree.nodes.new('ShaderNodeOutputMaterial')
semit = sunmat.node_tree.nodes.new('ShaderNodeEmission')
semit.inputs['Color'].default_value = (1.0, 0.75, 0.2, 1.0)  # warm yellow
semit.inputs['Strength'].default_value = 6.0
sunmat.node_tree.links.new(semit.outputs['Emission'], sout.inputs['Surface'])
sun.data.materials.append(sunmat)
bpy.ops.object.select_all(action='DESELECT')
sun.select_set(True)
bpy.context.view_layer.objects.active = sun
bpy.ops.object.shade_smooth()

# ---- Planets (radius, color, orbit distance) ----
# Mercury
mercury = make_planet("Mercury", 0.12, (0.6, 0.6, 0.6, 1.0), (2.2, 0, 0))
# Venus
venus = make_planet("Venus", 0.2, (0.9, 0.7, 0.4, 1.0), (3.2, 0, 0))
# Earth
earth = make_planet("Earth", 0.22, (0.2, 0.5, 0.9, 1.0), (4.2, 0, 0))
# Mars
mars = make_planet("Mars", 0.16, (0.8, 0.3, 0.2, 1.0), (5.2, 0, 0))
# Jupiter
jupiter = make_planet("Jupiter", 0.5, (0.8, 0.6, 0.4, 1.0), (6.8, 0, 0))
# Saturn (with rings)
saturn = make_planet("Saturn", 0.42, (0.85, 0.75, 0.5, 1.0), (8.4, 0, 0))
# Add Saturn's rings (parented to Saturn so they follow it)
bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.06, location=(8.4, 0, 0))
rings = bpy.context.object
rings.name = "SaturnRings"
rings.rotation_euler = (math.radians(80), 0, 0)
rmat = bpy.data.materials.new(name="RingMat")
rmat.use_nodes = True
rbsdf = rmat.node_tree.nodes.get("Principled BSDF")
rbsdf.inputs["Base Color"].default_value = (0.75, 0.65, 0.5, 1.0)
rbsdf.inputs["Roughness"].default_value = 0.6
rings.data.materials.append(rmat)
# Uranus
uranus = make_planet("Uranus", 0.34, (0.5, 0.8, 0.8, 1.0), (9.8, 0, 0))
# Neptune
neptune = make_planet("Neptune", 0.32, (0.2, 0.4, 0.9, 1.0), (11.0, 0, 0))

# ---- Camera (top-down view of the whole system, tracks the sun) ----
bpy.ops.object.camera_add(location=(0, -22, 18))
cam = bpy.context.object
cam.name = "SolarCam"
track = cam.constraints.new(type='TRACK_TO')
track.target = sun
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
bpy.context.scene.camera = cam

# ---- Lighting ----
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sunlight = bpy.context.object
sunlight.data.energy = 2.0

# ---- Animate: planets orbit the sun ----
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 180  # 6 seconds at 30fps

# Each planet orbits at a different speed (inner = faster)
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
    # Animate orbit via a circular path
    for frame, angle in [(1, 0), (90, math.pi * speed * 2), (180, math.pi * speed * 4)]:
        planet.location = (dist * math.cos(angle), dist * math.sin(angle), 0)
        planet.keyframe_insert(data_path="location", frame=frame)
    # Saturn's ring follows the exact same orbit path as Saturn
    if planet.name == "Saturn":
        for frame, angle in [(1, 0), (90, math.pi * speed * 2), (180, math.pi * speed * 4)]:
            rings.location = (dist * math.cos(angle), dist * math.sin(angle), 0)
            rings.keyframe_insert(data_path="location", frame=frame)

# ---- Render settings (EEVEE, 1080p, 30fps, PNG frames) ----
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "/tmp/solar_frames/frame_"
scene.render.film_transparent = False

# Dark space background
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.02, 0.02, 0.05, 1.0)  # deep space blue-black
    bg.inputs[1].default_value = 1.0

# Render animation
bpy.ops.render.render(animation=True)
print("RENDER_DONE")
