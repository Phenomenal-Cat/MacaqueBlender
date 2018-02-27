
#================ GetObjectScreenCoords.py =================
# Returns the x and y screen coordinates (pixels from bottom 
# left of screen) of the specified objects in the scene for
# the current frame. 

import numpy
import bpy
import bpy_extras

Targets         = ["CorneaL", "CorneaR", "TeethDown","TeethUp"]     # Specify which objects to get data for
cam             = bpy.data.objects['Camera']
scene           = bpy.context.scene
Resolution      = (bpy.data.scenes['Scene'].render.resolution_x, bpy.data.scenes['Scene'].render.resolution_y)

for t in Targets:
    obj         = bpy.data.objects[Targets[t]]
    origin_3D   = obj.location
    origin_2D   = bpy_extras.object_utils.world_to_camera_view(scene, cam, origin_3D)
    origin_pix[t,]  = origin_2D*Resolution
    
    
    
#   verts   = obj.data.vertices
#    for v in verts:
#        worldverts[v] = obj.matrix_world * verts[v].co

#    VertMean[t]     = numpy.mean[worldverts]
#    Vert2D[t]       = bpy_extras.object_utils.world_to_camera_view(scene, obj, VertMean[t])
#    VertScreen[t]   = Vert2D[t]*Resolution
    
    
    