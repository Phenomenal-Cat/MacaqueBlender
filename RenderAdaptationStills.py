# -*- coding: utf-8 -*-
"""============================ RenderAdaptationStills.py ==================================

This script loops through the specified stimulus variables, rendering static images
for each condition requested for the fMRI adaptation experiment.

06/07/2016 - Written by APM (murphyap@mail.nih.gov)
06/02/2017 - Updated for final rigged model (APM)
12/05/2017 - Updated to render stills for gaze direction stimuli
19/07/2017 - Updated to save condition data to .mat file
"""

import bpy
import mathutils as mu
import math
import numpy as np
import socket
#from scipy import io
from InitBlendScene import InitBlendScene

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
    
def GetEyeLocations():                        #=============== Get current eye locations in world coordinates
    EyeObjects      = ["EyeL","EyeR"]
    EyeBones        = ["eyeL","eyeR"]
    EyeLocations    = [[0 for x in range(3)] for y in range(2)] 
    for e in range(0,len(EyeObjects)):
        EyeObject   = bpy.data.objects[EyeObjects[e]]
        EyeBone     = bpy.data.objects["HeaDRig"].pose.bones[EyeBones[e]]
        #armature    = bpy.context.active_object
        #EyeBone     = bpy.context.active_pose_bone
        
        EyeLocations[e] = EyeObject.matrix_world * EyeObject.location       # 3D world coordinates (mm from scene origin)
        #EyePixCoord[e]  = EyeLocations[e][0,2]
        
        #vec         = mu.Vector((1, 0, 0))
        #EyeLocations[e] = EyeObject.matrix_world.inverted() * EyeBone.bone.matrix_local.inverted() * vec
    return EyeLocations


def CenterCyclopean(EyeLocations):              #================ Caclulate in-plane translation to center camera axis on cyclopean eye
    CycEyeLocation = [0, 0, 0]
    for dim in range(0, len(EyeLocations[0])):
        CycEyeLocation[dim] = np.mean([EyeLocations[0][dim], EyeLocations[1][dim]])              # Calculate 3D coordinates of cyclopean eye (mid point along inter-ocular line)
    return CycEyeLocation



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


ExperimentName      = "AdaptationExp"           
SetupGeometry       = 6                         # Specify which physical setup stimuli will be presented in
StereoFormat        = 1                         # Side-by-side stereo renders
#InitBlendScene(SetupGeometry, StereoFormat)
RenderDir           = BlenderDir + ExperimentName


#============ Set rendering parameters				
GazeElAngles    = [0]                                                       # Set elevation angles (degrees)
GazeAzAngles    = [0]                                                       # Set azimuth angles (degrees)
HeadElAngles    = [0]                                                       # Set elevation angles (degrees)
HeadAzAngles    = [-60, -30, 0, 30, 60]                                     # Set azimuth angles (degrees)
Distances       = [0]                                                       # Set object distance from origin (centimeters)
Scales          = [1]                                                       # Physical scale of object (proportion)
FurLengths      = [0.7]                                                     # Set relative length of fur (0-1)
ExpStr          = ["Neutral","Fear","Threat","Coo","Yawn"]                  # Set facial expressions
ExpNo           = [0, 1, 2, 3, 4]                                           
ExpWeights      = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp            = 0


CondParams = {'GazeAzAngles':GazeAzAngles, 'GazeElAngles': GazeElAngles, 'HeadAzAngles':HeadAzAngles, 'HeadElAngles':HeadElAngles, 'Distances':Distances, 'Scales':Scales, 'FurLengths':FurLengths, 'Expressions':ExpStr, 'ExpWeights':ExpWeights, 'ExpMicroWeights':ExpMicroWeights}

KeepCyclopeanCenter = 1                                 # Move body in order to maintain cyclopean eye in camera's optical axis
ShowBody            = 1;                                # Render body?
IncludeEyesOnly     = 0;                                # Include eyes only condition? 
InfiniteVergence    = 0;                                # Fixate (vergence) at infinity?
RotateBody          = 0;                                # 0 = rotate head relative to body; 1 = rotate whole body
GazeAtCamera        = 0;                                # Update gaze direction to maintain eye contact?
MoveGazeOnly        = 0;
NoConditions        = len(ExpNo)*len(HeadElAngles)*len(HeadAzAngles)*len(GazeElAngles)*len(GazeAzAngles)*len(Distances) #*len(Scales)        # Calculate total number of conditions
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
    
# bpy.data.particles["ParticleSettings.003"].path_end           = FurLengths    # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             

#============= Prepare condition settings variables to save to .mat file
CondMatrix      = np.zeros(shape=(NoConditions, 6)) 
CondFields      = [('Filename','S20'),('FullFile', 'S20'),('Expression','S10'),('HeadAzimuth','i4'),('HeadElevation','i4'),('HeadVectorCoord','float64', (3,)),('GazeAzimuth','i4'),('GazeElevation','i4'),('GazeVectorCoord','float64', (3,)),('Distance','i4'),('BodyRotation','i4'),('EyeLocations','float64', (2, 3))]
CondStruct      = np.zeros((NoConditions,), dtype=CondFields) 
Matfile         = RenderDir + "/%s_Conditions.mat" % (ExperimentName)                       # Construct the full path for the conditions .mat file

#========================== Begin rendering loop
r = 0
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
        body.location = mu.Vector((OrigBodyLoc[0], d/100, OrigBodyLoc[2]))                  # Move entire avatar d cm in depth from starting position

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


                        #=========== Rotate gaze
                        if GazeAtCamera == 1:                                                       # Gaze in direction of camera?
                            if InfiniteVergence == 0:                                               # Gaze converges at camera distance?
                                CamLocation = bpy.data.scenes["Scene"].camera.location
                                head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 0.9))
                                
                            elif InfiniteVergence == 1:                                             # Gaze converges at (approximately) infinity?
                                head.pose.bones['EyesTracker'].location = mu.Vector((0, 0.1, 10))

                        if MoveGazeOnly == 1:
                            GazeXYZ = GazeLookAt(Gel, Gaz)
                            head.pose.bones['EyesTracker'].location = GazeXYZ

                        #=========== Get eye positions
                        EyeLocations = GetEyeLocations()                                            # Get current world coordinates for eye objects
                        CycEyeLocations = CenterCyclopean(EyeLocations)                             # Get offset of cyclopean eye from world origin
                        print(CycEyeLocations)                                                         # Print eye coordinates for current scene (for debugging)
                        #if KeepCyclopeanCenter == 1:
                            #body.location = mu.Vector((OrigBodyLoc[0]-CycEyeLocations[0], d/100, OrigBodyLoc[2]-CycEyeLocations[2])) 


                        #=========== Render image and save to file
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                        RenderFilename = "MacaqueGaze_%s_Haz%d_Hel%d_Gaz%d_Gel%d_dist%d.png" % (ExpStr[exp], Haz, Hel, Gaz, Gel, d)
                        print("Now rendering: " + RenderFilename + " . . .\n")
                        #bpy.context.scene.render.filepath = RenderDir + "/" + RenderFilename
                        #bpy.ops.render.render(write_still=True, use_viewport=True)
                        
                        #=========== Update conditions data
                        CondMatrix[r]                   = [exp, Haz, Hel, Gaz, Gel, d];
                        CondStruct[r]['Filename']       = RenderFilename
                        CondStruct[r]['FullFile']       = RenderDir + "/" + RenderFilename
                        CondStruct[r]['Expression']     = ExpStr[exp]
                        CondStruct[r]['HeadAzimuth']    = Haz
                        CondStruct[r]['HeadElevation']  = Hel
                        CondStruct[r]['HeadVectorCoord']= head.pose.bones['HeadTracker'].location
                        CondStruct[r]['GazeAzimuth']    = Gaz
                        CondStruct[r]['GazeElevation']  = Gel
                        CondStruct[r]['GazeVectorCoord']= head.pose.bones['EyesTracker'].location
                        CondStruct[r]['Distance']       = d
                        CondStruct[r]['BodyRotation']   = RotateBody
                        CondStruct[r]['EyeLocations']   = EyeLocations
                        
                        r = r+1
                       
                        
                        
print("Rendering completed!\n")
io.savemat(Matfile, {'CondMatrix':CondMatrix, 'CondStruct':CondStruct, 'CondParams' :CondParams })       # Save conditions data to a Matlab .mat file
print("Conditions data saved to " + Matfile)


