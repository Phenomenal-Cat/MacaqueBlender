
#================== Dome_Retinotopy.py ============================
# Construct a virtual environemnt to match the physical geometry of 
# the SCNI's iDome rig, add a fisheye camera and a stimulus plane 
# that is constrained to always face the camera. A render loop is created
# for all stimulus locations and sizes (specified in spherical coordinates 
# and metric depth units).

import bpy
import math
import numpy as np
import bmesh

#============ Set physical hemispheric dome parameters
dome_radius                 = 1.2           # Dome radius in meters
dome_truncationElevation    = 45            # Elevation angle of dome truncated edge (degrees)
dome_projectorResolution    = [3840, 2160]  # Dome projector resolution in pixels

stim_diameters              = [2]
stim_azimuths               = []
stim_elevations             = np.linspace()
stim_distances              = [-10, 0, 10]
fix_diameter                = 0.005
fix_location                = np.array([0,1,0])


#============ Set scene and camera settings
Scene                                   = bpy.data.scenes[0]
Scene.unit_settings.system              = 'METRIC'
Scene.render.engine                     = 'CYCLES'
Scene.render.resolution_x               = Resolution[0]
Scene.render.resolution_y               = Resolution[1]
Scene.render.resolution_percentage      = 100

Camera                                  = Scene.camera
Camera.type                             = 'PANO'
Camera.cycles.panorama_type             = 'FISHEYE_EQUISOLID' 
Camera.cycles.fisheyelens               = 9
Camera.shift_y                          = -0.15
Camera.stereo.convergence_mode          = 'OFF_AXIS'
Camera.stereo.convergence_distance      = dome_radius
Camera.stereo.interocular_distance      = 0.03              # Subejct's interpupillary distance im meters
Camera.stereo.use_spherical_stereo      = False
Camera.stereo.pivot                     = 'CENTER'


#me      = bpy.data.meshes.new("Circles")
#obj     = bpy.data.objects.new("Circles", me)
#bpy.context.scene.objects.link(obj)
#bm      = bmesh.new()                        # Make a new BMesh
#bmesh.ops.create_circle(bm, cap_ends=True, radius=fix_diameter, segments=8)
#bm.to_mesh(me)

bpy.ops.mesh.primitive_circle_add(vertices=32, radius=fix_diameter/2, fill_type='NGON', calc_uvs=True, enter_editmode=False, align='WORLD', location=fix_location, rotation=(math.radians(90), 0.0, 0.0), scale=(0.0, 0.0, 0.0))
fix = bpy.data.objects['Circle']
fix.name = 'Fixation_marker'
fix.

#============ Create stimulus plane mesh
bpy.ops.mesh.primitive_plane_add(radius=1.0, location=(0,0,0))              # Create a plane primitive
stim                    = bpy.data.objects['Plane']                         # Get plane object handle
stim.name               = 'Stim_plane'                                      # Rename object                                     
mod                     = path.modifiers.new(name="Bevel", type='BEVEL')    # Apply a bevel modifier to the plane
mod.use_only_vertices   = True                                              # Adjust bevel parameters
mod.segments            = 5
mod.width               = 0.2
bpy.ops.object.convert(target='CURVE')                                      # Convert mesh to curve

#============ Constrain stimulus plane to always face subject camera
obj                         = bpy.data.objects['Plane']
Follow                      = obj.constraints.new(type='TRACK_TO')
Follow.target               = Camera
Follow.track_axis           = '-Z'
Follow.up_axis              = 'Y'

#============ Key frame stimulus locations
for d in stim_diameters:
    for a in stim_azimuths:
        for e in stim_elevations:
            for d in stim_distances:
                obj
                
                