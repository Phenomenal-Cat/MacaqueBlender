
# Exp_ObjectSelectivity.py

import bpy
import numpy as np
import mathutils as mu
import os

from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath
from SetDepthMapMode import SetDepthMapMode


def makeInvisible(ob, reverse):
    for child in ob.children:
        if reverse == 0:
            child.hide          = True
            child.hide_render   = True
            makeInvisible(child, reverse)
        elif reverse == 1:
            child.hide          = False
            child.hide_render   = False
            makeInvisible(child, reverse)

def RenderFrame(Filename, RenderDir, Render=1, Overwrite=1):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == 1:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")
            
            
Prefix              = GetOSpath()                                   # Get path prefix for OS          
RenderDir           = Prefix[0] + '/murphya/Stimuli/AvatarRenders_2018/ObjectSelectivity/'

Fruits      = ["Apple","Banana","Blackberry","Grapes","Kiwi","Mango","Orange","Pear","Potato"]
FamObj      = ["OBJ_Bucket"]
UnfamObj    = ["OBJ_Violin","OBJ_FrenchHorn","OBJ_Bass","OBJ_DrumKit"]
Azimuths    = [-90, -45, 0, 45, 90]
Elevations  = [-45, 0, 45]
FileFormat  = ".png"

ViewingDistance = 80

InitBlendScene(2, 1, ViewingDistance)    

for obj in Fruits:
    
    #============ Hide all other objects
    for o in Fruits:
        makeInvisible(bpy.data.objects[o], 0)
    makeInvisible(bpy.data.objects[obj], 1)

    
    #============ Update rotation
    for az in Azimuths:
        for el in Elevations:
            bpy.data.objects[obj].rotation_euler = mu.Vector((np.radians(el), 0, np.radians(az)))
            
            for z in [0,1]:
                FileFormat = SetDepthMapMode(z)
                Filename = "%s_Az%d_El%d%s" % (obj, az, el, FileFormat)
                RenderFrame(Filename, RenderDir, 1)