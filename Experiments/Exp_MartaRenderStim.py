

#=================== Exp_MartaRenderStim.py =======================

import bpy
import math
import os
import numpy as np
import mathutils as mu
import socket
from InitBlendScene import InitBlendScene

def RenderFrame(Filename, RenderDir, Render=True, Overwrite=1):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == True:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")
                
                

RenderDir = "/Volumes/NIFVAULT/projects/murphyap_NIF/MF3D/Marta_TEST/"
                
ViewingDistance = 0.5

InitBlendScene(2,1,ViewingDistance)

Test = True
Render = True
if Test == True:
  bpy.data.scenes["Scene"].render.resolution_percentage = 50
  bpy.data.scenes["Scene"].cycles.samples = 50
else:
  bpy.data.scenes["Scene"].render.resolution_percentage = 100
  bpy.data.scenes["Scene"].cycles.samples = 200

ObjAngles   = np.radians([90, -90])
ObjDepths   = [0.2, 0.15, 0.05, -0.05, -0.15, -0.2]
ObjXpos     = [-0.25, -0.15, -0.05, 0.05, 0.15, 0.25]
ObjNames    = ["monkey2"]


for obn in ObjNames:
    obj = bpy.data.objects[obn]
    obj.hide_render = False
    for ang in ObjAngles:
        obj.rotation_euler[2] = ang
        for d in ObjDepths:
            for x in ObjXpos:
                obj.location = [x, -ViewingDistance+d, 0]
                Filename = "%s_Ang%d_Xpos%d_Depth%d.%s" % (obn, ang, x*10, d*10, "png")
                RenderFrame(Filename, RenderDir, Render)
                
                

