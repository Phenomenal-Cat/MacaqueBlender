

#=================== RenderStim_Marta.py =======================

import bpy
import math
import os
import numpy as np
import mathutils as mu
import socket
#from InitBlendScene import InitBlendScene

def RenderFrame(Filename, RenderDir, Render=True, Overwrite=1):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == True:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")
                
                

ViewingDistance = 0.5
IPDs = [0.065, 0.035]
IPD_labels = ["Human", "Macaque"]


#InitBlendScene(2,1,ViewingDistance)

Test        = False     # Set lower render resolution for quick tests?
Render      = False     # Render each stimulus immediately?
KeyFrame    = True      # Set each stimulus configuration as a new key frame?
FrameCount  = 1

if Test == True:
  bpy.data.scenes["Scene"].render.resolution_percentage = 25
  bpy.data.scenes["Scene"].cycles.samples = 20
else:
  bpy.data.scenes["Scene"].render.resolution_percentage = 100
  bpy.data.scenes["Scene"].cycles.samples = 200

ObjAngles   = np.radians([90, -90])
ObjDepths   = [0.20, 0.10, 0.05, -0.05, -0.10, -0.20]
ObjXpos     = [-0.15, -0.125, -0.10, -0.075, -0.05, -0.025, 0.025, 0.05, 0.075, 0.10, 0.125, 0.15]
ObjNames    = ["Monkey1", "Monkey2", "Apple", "Banana", "Mug", "Spoon"]
FloorZ      = -0.12


#======= Initialize scene
Fix                 = bpy.data.objects["Fixation"]
Floor               = bpy.data.objects["Floor_checkered"]
Fix.hide_render     = True
Floor.hide_render   = True



# Render all stimuli for both experimenter (human) and subject (macaque) inter-ocular distances
for ipd in range(0, len(IPDs)):
    RenderDir = "/Volumes/NIFVAULT/projects/murphyap_NIF/MF3D/MartaStim/VD=%s/%s/" % (ViewingDistance, IPD_labels[ipd])
    bpy.data.cameras["Camera"].stereo.interocular_distance  = IPDs[ipd]
    #bpy.data.cameras["Camera"].keyframe_insert(data_path="interocular_distance")
    
    #=== Render fixation marker at all depths
    Fix.hide_render = False
    for d in ObjDepths:
        Fix.location[1] = -ViewingDistance+d
        Filename = "Fixation_Depth%d.%s" % (d*100, "png")
        RenderFrame(Filename, RenderDir, Render)
    Fix.hide_render = True
    
    #=== Render floor plane
    Floor.hide_render = False
    Floor.location[2] = FloorZ
    Filename = "Floorplane.png"
    RenderFrame(Filename, RenderDir, Render)
    Floor.hide_render = True
    
    #=== Render each object
    for obn in ObjNames:
        
        # First, hide all objects in the scene and their children
        for AllOb in ObjNames:
            NextOb = bpy.data.objects[AllOb]
            NextOb.hide_render = True
            NextOb.hide_viewport = True
            if KeyFrame:
                NextOb.keyframe_insert(data_path="hide_render", frame=FrameCount)
                NextOb.keyframe_insert(data_path="hide_viewport", frame=FrameCount)
            list_of_children = bpy.data.objects[AllOb].children
            for ch in list_of_children:
                ch.hide_render = True
                ch.hide_viewport = True
                if KeyFrame:
                    ch.keyframe_insert(data_path="hide_render", frame=FrameCount)
                    ch.keyframe_insert(data_path="hide_viewport", frame=FrameCount)
        
        # Next, unhide the current object and its children
        obj = bpy.data.objects[obn]
        obj.hide_render = False
        obj.hide_viewport = False
        if KeyFrame:
            obj.keyframe_insert(data_path="hide_render", frame=FrameCount)
            obj.keyframe_insert(data_path="hide_viewport", frame=FrameCount)
        for ch in obj.children:
            ch.hide_render = False
            ch.hide_viewport = False
            if KeyFrame:
                ch.keyframe_insert(data_path="hide_render", frame=FrameCount)
                ch.keyframe_insert(data_path="hide_viewport", frame=FrameCount)
        
        # Now iterate through the other parameters
        for d in ObjDepths:
            for x in ObjXpos:
                if (x > 0):
                    ang = 0
                else:
                    ang = 1
                obj.rotation_euler[2]   = ObjAngles[ang]
                obj.location            = [x, -ViewingDistance+d, FloorZ]
                
                if Render:
                    Filename = "%s_Ang%d_Xpos%.1f_Depth%d.%s" % (obn, np.degrees(ObjAngles[ang]), x*100, d*100, "png")
                    RenderFrame(Filename, RenderDir, Render)
                if KeyFrame:
                    print('Inserting keyframe %d...' % FrameCount)
                    obj.keyframe_insert(data_path="location", frame=FrameCount)
                    obj.keyframe_insert(data_path="rotation_euler", frame=FrameCount)
                    bpy.context.scene.frame_set(FrameCount)
                    FrameCount = FrameCount+1
                    
if KeyFrame:
    bpy.context.scene.frame_start  = 1 
    bpy.context.scene.frame_end     = FrameCount 