# -*- coding: utf-8 -*-
"""============================ RenderGazeStills.py ==================================

This script loops through the specified stimulus variables, rendering static images
for each condition requested.

06/07/2016 - Written by APM (murphyap@mail.nih.gov)
06/02/2017 - Updated for final rigged model (APM)
12/05/2017 - Updated to render stills for gaze direction stimuli
18/06/2018 - Updated to render depth maps for RDS
"""

import bpy
import mathutils as mu
import math
import os
import numpy as np
import socket
#import AddDepthArray

from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath
import OrientAvatar as OA
from SetDepthMapMode import SetDepthMapMode


def HeadLookAt(El, Az):
    Rad = 0.7
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*-Rad
    Y   = np.sin(math.radians(El))*Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ


bpy.types.UserPreferencesEdit.keyframe_new_interpolation_type = 'LINEAR'    # F-curve interpolation defaults to linear


#============ Initialize scene
Prefix              = GetOSpath()                                   # Get path prefix for OS
BlenderDir          = Prefix[0] + '/murphya/Stimuli/AvatarRenders_2018/'            
RenderDir           = BlenderDir + "PeripheralGaze"
SetupGeometry       = 2                                             # Specify which physical setup stimuli will be presented in
StereoFormat        = 1                                             # Render as stereo-pair?
ViewingDistance     = 70                                           # Distance of subject from screen (cm) 
InitBlendScene(SetupGeometry, StereoFormat, ViewingDistance)        # Initialize scene
#AddDepthArray()                                                     # Add depth array?

#============ Set rendering parameters	
GazeElAngles    = [0]#[-20,-10, 0, 10, 20]                              # Set elevation angles (degrees)
GazeAzAngles    = [0]#[-30, -20, -10, 0, 10, 20, 30]                    # Set azimuth angles (degrees)
HeadElAngles    = [0]
HeadAzAngles    = [-45,-30,-15,0,15,30,45]
BodyElAngles    = [0]
BodyAzAngles    = [0]
Distances       = [-20, 0, 20] 						                   # Set object depth distance from origin (centimeters)
Eccentricities  = [-30, -15, 0, 15, 30]		
LocationX       = np.empty([len(Distances), len(Eccentricities)])
for d in range(0, len(Distances)):
    for e in range(0, len(Eccentricities)):
        LocationX[d][e] = math.tan(math.radians(Eccentricities[e]))*(ViewingDistance + Distances[d])

#Scales          = [0.666, 1.0, 1.333]                               # Physical scale of object (proportion)
#Distances       = [0] 						                        # Set object distance from origin (centimeters)
Scales          = [1.0]                                             # Physical scale of object (proportion)
FurLengths      = [0.7]                                             # Set relative length of fur (0-1)
ExpStr          = ["Neutral","Fear","Threat","Coo","Yawn"]          # Expression names   
ExpNo           = [0] #[0, 1, 2, 3, 4]                              # Expression numbers
ExpWeights      = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp            = 0

ShowBody            = 1;                                            # Turn on/ off body visibility
IncludeEyesOnly     = 0;                                            # Include eyes only condition? 
InfiniteVergence    = 0;                                            # Fixate (vergence) at infinity?
GazeAtCamera        = 0;                                            # Update gaze direction to maintain eye contact with camera?

NoConditions        = len(HeadElAngles)*len(HeadAzAngles)*len(Distances)*len(Eccentricities)        # Calculate total number of conditions
if IncludeEyesOnly == 1:
    NoConditions = NoConditions*2;                      
    
msg                 = "Total renders = %d" % NoConditions				
print(msg)

#============== FOR QUICK TESTS
#Scene                                    = bpy.data.scenes['Scene']  # Quick and dirty render!
#Scene.render.resolution_percentage      = 50
#bpy.context.scene.cycles.samples        = 10


#=============== Set cyclopean eye as avatar origin point?
head                = bpy.data.objects["HeaDRig"]
body                = bpy.data.objects["Root"]
body.rotation_mode  = 'XYZ'
OffsetCyclopean     = 0                                         # Translate whole avatar so that cyclopean eye is always in the same position?
CyclopeanOrigin     = ((0,0,0))                                 # World coordinate to move cyclopean eye to (if OffsetCyclopean = 1)

bpy.context.scene.cursor_location   = CyclopeanOrigin           # Set current cursor position to cyclopean eye coordinates
bpy.context.scene.objects.active    = body                      # Set avatar rig as active object
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')                 # Set origin of avatar to cyclopean eye                                   

#bpy.ops.object.mode_set(mode='POSE')
OrigBodyLoc         = body.location 
OrigBodyScale       = body.scale


if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             


#========================== Begin rendering loop
for exp in ExpNo:

    #======= Set primary expression
    head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]))           # Wide mouthed 'yawn' expression
    head.pose.bones['Kiss'].location    = mu.Vector((0,0.02*ExpWeights[exp,2],0))           # Pursed lip 'coo' expression
    head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]))           # Open-mouthed 'threat' expression
    head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0],0))          # Bared-teeth 'fear' grimace

    #======= Set micro expression
    head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]))   # Close eye lids (blink)
    head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1],0))    # Retract ears
    head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]))   # Raise brow
    head.pose.bones['EyesTracker'].scale = mu.Vector((0, 1*ExpMicroWeights[mexp, 3], 0))    # Pupil dilation/ constriction

    for s in Scales:
        body.scale = mu.Vector((OrigBodyScale[0]*s, OrigBodyScale[1]*s, OrigBodyScale[2]*s))        # Apply scaling to entire avatar
    
        for d in range(0, len(Distances)):
            for e in range(0, len(LocationX[d])):
                body.location = mu.Vector((LocationX[d][e]/100, Distances[d]/100, OrigBodyLoc[2])) 


                for Hel in HeadElAngles:
                    for Haz in HeadAzAngles:
                            HeadXYZ = HeadLookAt(Hel, Haz)
                            head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
            
                            #=========== Render color and Z-buffer images
                            for z in [0,1]:
                                FileFormat = SetDepthMapMode(z)
                                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                                Filename = "MacaqueGaze_%s_Haz%d_dist%d_ecc%d%s" % (ExpStr[exp], Haz, Distances[d], Eccentricities[e], FileFormat)
                                if os.path.isfile(RenderDir + "/" + Filename) == 0:
                                    print("Now rendering: " + Filename + " . . .\n")
                                    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                                    bpy.ops.render.render(write_still=True, use_viewport=True)
                                elif os.path.isfile(RenderDir + "/" + Filename) == 1:
                                    print("File " + Filename + " already exists. Skipping . . .\n")

print("Rendering completed!\n")




