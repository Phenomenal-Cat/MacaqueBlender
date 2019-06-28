# -*- coding: utf-8 -*-
"""============================ Exp_MethodsStimSet1.py ==================================
This script loops through the specified stimulus variables, rendering static images
for each condition requested for the stimulus set 1 released with Murphy & Leopold, 2019.

"""

import bpy
import mathutils as mu
import math
import os
import numpy as np
import socket
from GetOSpath import GetOSpath
from InitBlendScene import InitBlendScene


def RenderFrame(Filename, RenderDir, Render=1, Overwrite=0):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == 1:
        if (os.path.isfile(RenderDir + "/" + Filename) == 0) or (Overwrite == 1):
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif (os.path.isfile(RenderDir + "/" + Filename) == 1) and (Overwrite == 0):
            print("File " + Filename + " already exists. Skipping . . .\n")
            
def HeadLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ

def GazeLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    GazeXYZ = mu.Vector((X, Y, Z))
    return GazeXYZ    
    
def GetEyeLocations():                        #=============== Get current eye locations
    EyeObjects      = ["EyeL","EyeR"]
    EyeBones        = ["eyeL","eyeR"]
    EyeLocations    = [[0 for x in range(3)] for y in range(2)] 
    for e in range(0,len(EyeBones)-1):
        EyeObject   = bpy.data.objects[EyeObjects[e]]
        EyeBone     = bpy.data.objects["HeaDRig"].pose.bones[EyeBones[e]]
        #armature    = bpy.context.active_object
        #EyeBone     = bpy.context.active_pose_bone
        vec         = mu.Vector((1, 0, 0))
        EyeLocations[e] = EyeObject.matrix_world.inverted() * EyeBone.bone.matrix_local.inverted() * vec
    return EyeLocations

SetKeyFrames        = 1                         # Set key frames?
Render              = 0                         # Render images? Set to 0 for script testing
Overwrite           = 0                         # Overwrite existing images?
SetupGeometry       = 7                         # Specify which physical setup stimuli will be presented in
StereoFormat        = 0
InitBlendScene(SetupGeometry, StereoFormat, 57)
[Prefix, temp]      = GetOSpath()
RenderDir           = Prefix + 'murphya/MacaqueFace3D/Methods Manuscript/MF3D_R1/MF3D_Identities/'


#============ Set rendering parameters						
GazeElAngles    = [0]                                                       # Set elevation angles (degrees)
GazeAzAngles    = [0]                                                       # Set azimuth angles (degrees)
HeadElAngles    = [0]
HeadAzAngles    = range(-10, 15, 5)
MaxHeadAz       = 30                                                        # Azimuth angle after which head rotation stops and body rotation begins
PClevels        = [0.5, 1.25, 2, 2.75, 3.5]
PCcombos        = [[0,1],[0,2],[1,2]]
PCcombosA       = [0,1,2]
PCcombosB       = [0,1,2]
#PCangles        = [0, 22.5, 45, 67.5, 90]                                          # Set angles of trajectories within 2D PCA space (degrees)
#PCangles        = [16.4, 30.7, 45, 59.3, 73.6]
PCbase          = [6.8, 25.9, 45, 64.1, 83.2]
PCangles        = [6.8, 25.9, 45, 64.1, 83.2]
for q in range(1,4):
    for ang in range(0, len(PCbase)):
        PCangles.append(PCbase[ang]+(90*q))

PCangles        = [45, 135, 225, 315]
Distances       = [0]                                                       # Set object distance from origin (centimeters)
Scales          = [1]                                                                   # Physical scale of object (proportion)
FurLengths      = [0.7]                                                                 # Set relative length of fur (0-1)
MinusPlus       = ['-','','+']

ShowBody            = 1;                                # Render body?
InfiniteVergence    = 0;                                # Fixate (vergence) at infinity? 0 = camera distance
RotateBody          = 1;                                # 0 = rotate head relative to body; 1 = rotate whole body
GazeAtCamera        = 0;                                # Update gaze direction to maintain eye contact?
NoConditions        = len(HeadElAngles)*len(HeadAzAngles)*len(GazeElAngles)*len(GazeAzAngles)*len(PClevels)*len(PCcombosA) #*len(Scales)        # Calculate total number of conditions
                
                
msg                 = "Total renders = %d" % NoConditions				
print(msg)
body                = bpy.data.objects["IdentityModel"]
body.rotation_mode  = 'XYZ'
OrigBodyLoc         = body.location 
head                = bpy.data.objects["AverageMesh_N=23.001"]
headrig             = bpy.data.objects["HeaDRig"]
#GazeOrigin          = head.pose.bones['EyesTracker'].location
#GazeOrigin[0]       = 0
#GazeOrigin[2]       = 0
Gaz = 0
Gel = 0
#bpy.ops.object.mode_set(mode='POSE')
Scene                      = bpy.data.scenes['Scene']  
Scene.frame_start          = 1         
Scene.frame_end            = NoConditions    # How many frames in animation?

if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             


#========================== Begin rendering loop
frametotal = 1
bpy.context.scene.frame_set(frametotal) 
for cond in [0]:
    if cond == 1:
        bpy.context.scene.cycles.samples        = 1
        Scene.render.image_settings.file_format = 'HDR'
        RenderDir = RenderDir + "LabelMaps"
    else:
        RenderDir = RenderDir + "ColorImages"
        
#    for pcA in PCcombosA:
#        for pcB in PCcombosB:
    for c in range(0, len(PCcombos)):
        pcA = PCcombos[c][0]
        pcB = PCcombos[c][1]
            
        #=========== Determine trajectory polarity in 2D PC-space
        pcbdir = 1

        
        #=========== For each 'distinctiveness' level (i.e. Euclidean distance from mean)
        #pcl = 2
        
        for pcang in PCangles:
            for pcl in PClevels:
            
                if pcA != pcB:
                    pclsign     = pcl/abs(pcl)
                    pclA        = np.sin(np.radians(pcang))*pcl
                    pclB        = np.cos(np.radians(pcang))*pcl
                else:
                    pclA = pcl
                    pclB = 0
                    
                
                #=========== Set PC shape key values
                for pc in range(0, 10):
                    
                    if pcA == pc:
                        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = (1/3)*pclA 
                    elif pcB == pc:
                        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = (1/3)*pclB*pcbdir 
                    else:
                        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = 0
                    head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value")
            
            
                for d in Distances:
                    body.location = mu.Vector((OrigBodyLoc[0], OrigBodyLoc[1]+d/100, OrigBodyLoc[2]))
                    
                    #=========== Rotate head
                    for Hel in HeadElAngles:
                        for Haz in HeadAzAngles:
                            
                            #=========== Rotate body
                            if RotateBody == 1:
                                if abs(Haz) > 0:
                                    if abs(Haz) > MaxHeadAz:
                                        Baz     = (abs(Haz) - MaxHeadAz)*Haz/abs(Haz)
                                    else:
                                        Baz = 0
                                else:
                                    Baz = 0
                                    
                                body.rotation_euler = (0, 0, math.radians(Baz))
                                
                                Haz2    = Haz-Baz
                                print("Head azimuth angle = %d, Body azimuth angle = %d" % (Haz2, Baz))
                                HeadXYZ = HeadLookAt(Hel, Haz2)
                                headrig.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                                headrig.pose.bones['HeadTracker'].keyframe_insert(data_path="location") 
                                
                            elif RotateBody ==0:
                                HeadXYZ = HeadLookAt(Hel, Haz)
                                headrig.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                                headrig.pose.bones['HeadTracker'].keyframe_insert(data_path="location") 
       

                            #============ Update render and save
                            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                            if cond == 0:
                                if pcA == pcB:
                                    Filename = "MF3D_PC%d=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_RGBA.png" % (pcA+1, pcl, Haz, -Hel, Gaz, Gel)
                                else:
                                    if pcang==90:
                                        Filename = "MF3D_PC%d%sPC%d=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_RGBA.png" % (pcA+1, MinusPlus[pcbdir+1], pcB+1, pcl, Haz, -Hel, Gaz, Gel)
                                    else:
                                        Filename = "MF3D_PC%d%sPC%d_(%.1fdeg)=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_RGBA.png" % (pcA+1, MinusPlus[pcbdir+1], pcB+1, pcang, pcl, Haz, -Hel, Gaz, Gel)
                                   
                            elif cond == 1:
                                if pcA == pcB:
                                    Filename = "MF3D_PC%d=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_Label.hdr" % (pcA+1, pcl, Haz, -Hel, Gaz, Gel)
                                else:
                                    if pcang==90:
                                        Filename = "MF3D_PC%d%sPC%d=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_Label.hdr" % (pcA+1, MinusPlus[pcbdir+1], pcB+1, pcl, Haz, -Hel, Gaz, Gel)
                                    else:
                                        Filename = "MF3D_PC%d%sPC%d_(%.1fdeg)=%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_Label.hdr" % (pcA+1, MinusPlus[pcbdir+1], pcB+1, pcang, pcl, Haz, -Hel, Gaz, Gel)
                                        
                            if SetKeyFrames == 1:
                                print("Set keyframe... ")
                                for pc in range(0, 10):
                                    head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value")
                                
                            elif SetKeyFrames == 0:
                                RenderFrame(Filename, RenderDir, Render, Overwrite)
                          
                            frametotal = frametotal+1
                            bpy.context.scene.frame_set(frametotal) 

print("Rendering completed!\n")




