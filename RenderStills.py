# -*- coding: utf-8 -*-
"""============================ RenderGazeStills.py ==================================

This script loops through the specified stimulus variables, rendering static images
for each condition requested.

06/07/2016 - Written by APM (murphyap@mail.nih.gov)
06/02/2017 - Updated for final rigged model (APM)
12/05/2017 - Updated to render stills for gaze direction stimuli
"""

import bpy
import mathutils as mu
import math
import numpy as np
import socket
#from InitBlendScene import InitBlend

def HeadLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*-Rad
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


if socket.gethostname().find("STIM_S4")==0:
    BlenderDir      = "P:/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur3.blend"
elif socket.gethostname().find("MH01918639MACDT")==0 :
    BlenderDir      = "/Volumes/projects/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur.blend"
elif socket.gethostname().find("DESKTOP-5PBDLG6")==0 :
    BlenderDir      = "P:/murphya/MacaqueFace3D/BlenderFiles/"
elif socket.gethostname().find("Aidans-Mac")==0:
    #BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/BlenderFiles/"
    BlenderFile     = "BlenderFiles/NGmacaqueHead09.blen.blend"

SetupGeometry       = 2                         # Specify which physical setup stimuli will be presented in
StereoFormat        = 1
#InitBlend(SetupGeometry, StereoFormat )
RenderDir           = BlenderDir + "Renders"


#============ Set rendering parameters						
GazeElAngles    = [0]  # [-20,-10, 0, 10,20]                                           # Set elevation angles (degrees)
GazeAzAngles    = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]                # Set azimuth angles (degrees)
HeadElAngles    = GazeElAngles
HeadAzAngles    = GazeAzAngles
#Distances       = [-20, 0, 20] 						                          # Set object distance from origin (centimeters)
Distances       = [0]
Scales          = [1]                                                             # Physical scale of object (proportion)
FurLengths      = [0.7]                                                         # Set relative length of fur (0-1)
ExpStr          = ["Neutral","Fear","Threat","Coo","Yawn"]
ExpNo           = [0] #[0, 1, 2, 3, 4]
ExpWeights      = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp            = 0

ShowBody            = 0;                                
IncludeEyesOnly     = 0;                                # Include eyes only condition? 
InfiniteVergence    = 0;                                # Fixate (vergence) at infinity?
RotateBody          = 2;                                # 0 = rotate head relative to body; 1 = rotate whole body; 2 = rotate head (not using rig)
GazeAtCamera        = 1;                                # Update gaze direction to maintain eye contact?
MoveGazeOnly        = 0;
NoConditions        = len(HeadElAngles)*len(HeadAzAngles)*len(GazeElAngles)*len(GazeAzAngles)*len(Distances) #*len(Scales)        # Calculate total number of conditions
if IncludeEyesOnly == 1:
    NoConditions = NoConditions*2;                      
    
msg                 = "Total renders = %d" % NoConditions				
print(msg)
body                = bpy.data.objects["Root"]
body.rotation_mode  = 'XYZ'
OrigBodyLoc         = body.location 
head                = bpy.data.objects["HeaDRig"]
#bpy.ops.object.mode_set(mode='POSE')


if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             


#========================== Begin rendering loop
for exp in ExpNo:

    #======= Set primary expression
    #bpy.ops.object.mode_set(mode='POSE')
    head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]))           # Wide mouthed 'yawn' expression
    head.pose.bones['Kiss'].location    = mu.Vector((0,0.02*ExpWeights[exp,2],0))           # Pursed lip 'coo' expression
    head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]))           # Open-mouthed 'threat' expression
    head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0],0))          # Bared-teeth 'fear' grimace

    #======= Set micro expression
    head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]))   # Close eye lids (blink)
    head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1],0))    # Retract ears
    head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]))   # Raise brow
    head.pose.bones['EyesTracker'].scale = mu.Vector((0, 1*ExpMicroWeights[mexp, 3], 0))    # Pupil dilation/ constriction

    #for s in Scales:
    #head.scale = mu.Vector((s, s, s))
    s = 1
    
    for d in Distances:
        body.location = mu.Vector((OrigBodyLoc[0], d/100, OrigBodyLoc[2]))

        for Hel in HeadElAngles:
            for Haz in HeadAzAngles:
                
                for Gel in GazeElAngles:
                    for Gaz in GazeAzAngles:

                        #=========== Rotate head/ body
                        if RotateBody == 1:
                            body.rotation_euler = (math.radians(Hel), 0, math.radians(Haz))
                            
                        elif RotateBody ==0:
                            if MoveGazeOnly == 0:
                                #bpy.ops.object.mode_set(mode='POSE')
                                HeadXYZ = HeadLookAt(Hel, Haz)
                                head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                                
                        elif RotateBody ==2:
                            head.rotation_euler = (math.radians(Hel+10), 0, math.radians(Haz))


                        #=========== Rotate gaze
                        EyeLocations = GetEyeLocations()                                            # Get current world coordinates for eye objects
                        if GazeAtCamera == 1:                                                       # Gaze in direction of camera?
                            if InfiniteVergence == 0:                                               # Gaze converges at camera distance?
                                CamLocation = bpy.data.scenes["Scene"].camera.location
                                head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 0.9))
                                
                            elif InfiniteVergence == 1:                                             # Gaze converges at (approximately) infinity?
                                
                                head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 10))
                            
                        if MoveGazeOnly == 1:
                            GazeXYZ = GazeLookAt(Gel, Gaz)
                            head.pose.bones['EyesTracker'].location = GazeXYZ

                        
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                        Filename = "MacaqueGaze_%s_Haz%d_Hel%d_Gaz%d_Gel%d_dist%d.png" % (ExpStr[exp], Haz, Hel, Gaz, Gel, d)
                        print("Now rendering: " + Filename + " . . .\n")
                        #bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                        #bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering completed!\n")




