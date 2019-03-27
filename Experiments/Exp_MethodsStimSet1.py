# -*- coding: utf-8 -*-
"""============================ Exp_MethodsStimSet1.py ==================================
This script loops through the specified stimulus variables, rendering static images
for each condition requested for the stimulus set 1 released with Murphy & Leopold, 2019.

"""

import bpy
import mathutils as mu
import math
import numpy as np
import socket
from GetOSpath import GetOSpath
from InitBlendScene import InitBlendScene


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



SetupGeometry       = 7                         # Specify which physical setup stimuli will be presented in
StereoFormat        = 0
InitBlendScene(SetupGeometry, StereoFormat, 57)
[Prefix, temp]      = GetOSpath()
RenderDir           = Prefix + 'murphya/MacaqueFace3D/Methods Manuscript/StimSet1/Expressions'


#============ Set rendering parameters						
GazeElAngles    = [0]                                                       # Set elevation angles (degrees)
GazeAzAngles    = [0]                                                       # Set azimuth angles (degrees)
HeadElAngles    = range(-30, 40, 10)
HeadAzAngles    = range(-90, 100, 10)
MaxHeadAz       = 30                                                        # Azimuth angle after which head rotation stops and body rotation begins
Distances       = [0]                                                       # Set object distance from origin (centimeters)
Scales          = [1]                                                                   # Physical scale of object (proportion)
FurLengths      = [0.7]                                                                 # Set relative length of fur (0-1)
ExpStr          = ["Neutral","Fear","Threat","Coo","Yawn"]
ExpNo           = [0, 1, 2, 3, 4]                                                       # Which expressions to render
ExpWeights      = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp            = 0
ExpMagnitudes   = [0.25, 0.5, 0.75, 1.0]

ShowBody            = 1;                                # Render body?
InfiniteVergence    = 0;                                # Fixate (vergence) at infinity? 0 = camera distance
RotateBody          = 1;                                # 0 = rotate head relative to body; 1 = rotate whole body
GazeAtCamera        = 0;                                # Update gaze direction to maintain eye contact?
NoConditions        = len(HeadElAngles)*len(HeadAzAngles)*len(GazeElAngles)*len(GazeAzAngles)*len(Distances) #*len(Scales)        # Calculate total number of conditions
                  
    
msg                 = "Total renders = %d" % NoConditions				
print(msg)
body                = bpy.data.objects["Root"]
body.rotation_mode  = 'XYZ'
OrigBodyLoc         = body.location 
head                = bpy.data.objects["HeaDRig"]
GazeOrigin          = head.pose.bones['EyesTracker'].location
GazeOrigin[0]       = 0
GazeOrigin[2]       = 0

#bpy.ops.object.mode_set(mode='POSE')
Scene                                   = bpy.data.scenes['Scene']  # <<< Quick and dirty render!
#Scene.render.resolution_percentage      = 25
#bpy.context.scene.cycles.samples        = 10

if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             


#========================== Begin rendering loop
for cond in [0,1]:
    if cond == 1:
        bpy.context.scene.cycles.samples        = 1
        Scene.render.image_settings.file_format = 'HDR'
        RenderDir = RenderDir + "/LabelMaps"
        
    for exp in ExpNo:
        
        for ExpMag in ExpMagnitudes:
        
            #======= Set primary expression
            #bpy.ops.object.mode_set(mode='POSE')
            head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]*ExpMag))               # Wide mouthed 'yawn' expression
            head.pose.bones['Kiss'].location    = mu.Vector((0,0.02*ExpWeights[exp,2]*ExpMag,0))               # Pursed lip 'coo' expression
            head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]*ExpMag))               # Open-mouthed 'threat' expression
            head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0]*ExpMag,0))              # Bared-teeth 'fear' grimace

            #======= Set micro expression
            head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]*ExpMag))       # Close eye lids (blink)
            head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1]*ExpMag,0))        # Retract ears
            head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]*ExpMag))       # Raise brow
            head.pose.bones['EyesTracker'].scale = mu.Vector((0, 0.2+0.8*ExpMicroWeights[mexp, 3]*ExpMag, 0))  # Pupil dilation/ constriction

            
            for d in Distances:
                body.location = mu.Vector((OrigBodyLoc[0], OrigBodyLoc[1]+d/100, OrigBodyLoc[2]))

                for Hel in HeadElAngles:
                    for Haz in HeadAzAngles:
                        
                        #=========== Rotate head/ body
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
                            head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                            
                        elif RotateBody ==0:
                            HeadXYZ = HeadLookAt(Hel, Haz)
                            head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                        
                        
                        for Gel in GazeElAngles:
                            for Gaz in GazeAzAngles:

                                #=========== Rotate gaze
                                EyeLocations = GetEyeLocations()                                            # Get current world coordinates for eye objects
                                if GazeAtCamera == 1:                                                       # Gaze in direction of camera?
                                    if InfiniteVergence == 0:                                               # Gaze converges at camera distance?
                                        CamLocation = bpy.data.scenes["Scene"].camera.location
                                        head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 0.9))
                                        
                                    elif InfiniteVergence == 1:                                             # Gaze converges at (approximately) infinity?
                                        
                                        head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 10))
                                        
                                elif GazeAtCamera == 0:    
                                    GazeXYZ = GazeLookAt(Gel, Gaz)
                                    #print("Gaze coordinates =({}, {}, {});".format(*GazeXYZ))
                                    head.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, 0.26, 0))


                                #============ Update render and save
                                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                                if cond == 0:
                                    Filename = "MF3D_%s%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_RGBA.png" % (ExpStr[exp], ExpMag, Haz, -Hel, Gaz, Gel)
                                elif cond == 1:
                                    Filename = "MF3D_%s%.2f_Haz%d_Hel%d_Gaz%d_Gel%d_Label.hdr" % (ExpStr[exp], ExpMag, Haz, -Hel, Gaz, Gel)
                                print("Now rendering: " + Filename + " . . .\n")
                                bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                                bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering completed!\n")




