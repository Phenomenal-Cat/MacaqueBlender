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


if socket.gethostname().find("STIM_S4")==0:
    BlenderDir      = "P:/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur3.blend"
elif socket.gethostname().find("MH01918639MACDT")==0 :
    BlenderDir      = "/Volumes/projects/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur.blend"
elif socket.gethostname().find("DESKTOP-5PBDLG6")==0 :
    BlenderDir      = "P:/murphya/MacaqueFace3D/GazeExperiments/Renders/Experiment7_v2/"
elif socket.gethostname().find("Aidans-Mac")==0:
    #BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/BlenderFiles/"
    BlenderFile     = "BlenderFiles/NGmacaqueHead09.blen.blend"

SetupGeometry       = 2                         # Specify which physical setup stimuli will be presented in
StereoFormat        = 1
#InitBlend(SetupGeometry, StereoFormat )
RenderDir           = BlenderDir # + "Renders"


#============ Set rendering parameters						
#GazeElAngles    = [-15, 0, 15] #[0]                                         # Set elevation angles (degrees)
#GazeAzAngles    = [-30, -15, 0, 15, 30]                                     # Set azimuth angles (degrees)
HeadElAngles    = [-15, 0, 15]
HeadAzAngles    = [-30, -15, 0, 15, 30]  
GazeElAngles    = [0]
GazeAzAngles    = [0] 
#Distances       = [-20, 0, 20] 						                          # Set object distance from origin (centimeters)
Distances       = [0]
Scales          = [1]                                                             # Physical scale of object (proportion)
FurLengths      = [0.7]                                                         # Set relative length of fur (0-1)
ExpStr          = ["Neutral","Fear","Threat","Coo","Yawn"]
ExpNo           = [0] #[0, 1, 2, 3, 4]                                          # Which expressions to render
ExpWeights      = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp            = 0

ShowBody            = 1;                                # Render body?
IncludeEyesOnly     = 0;                                # Include eyes only condition? 
InfiniteVergence    = 0;                                # Fixate (vergence) at infinity? 0 = camera distance
RotateBody          = 0;                                # 0 = rotate head relative to body; 1 = rotate whole body
GazeAtCamera        = 0;                                # Update gaze direction to maintain eye contact?
NoConditions        = len(HeadElAngles)*len(HeadAzAngles)*len(GazeElAngles)*len(GazeAzAngles)*len(Distances) #*len(Scales)        # Calculate total number of conditions
if IncludeEyesOnly == 1:
    NoConditions = NoConditions*2;                      
    
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


if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             

Conditions = [3]

#========================== Begin rendering loop
for cond in Conditions:
    if cond == 1:   #====================== Render eyes only
        bpy.data.objects['BodyZremesh2'].hide_render                = True      # Hide body from rendering
        # bpy.data.objects['MacaqueHeadNG_1expressions1'].hide_render = True 
        bpy.data.objects['TeethDown'].hide_render                   = True      # Hide internal mouth components
        bpy.data.objects['TeethUp'].hide_render                     = True  
        bpy.data.objects['Tongue_1'].hide_render                    = True  
        Head = bpy.data.objects['MacaqueHeadNG_1expressions1']
        Head.modifiers['Mouth hair'].show_render                    = False     # Turn off all facial hair
        Head.modifiers['ears'].show_render                          = False
        Head.modifiers['eyebrows'].show_render                      = False
        Head.modifiers['fuzz'].show_render                          = False
        Head.modifiers['mustaches'].show_render                     = False
        Head.modifiers['eyelashes'].show_render                     = False
        Head.modifiers['basefur'].show_render                       = False
        mat     = bpy.data.materials.get('HoldoutMat')                          # Get holdout material
        if mat is None:                                                         # If holdout material doesn't exist yet...
            mat     = bpy.data.materials.new(name='HoldoutMat')                 # Create holdout material
            nodes   = mat.node_tree.nodes                                       # Get material nodes
            holdout = nodes.get('Holdout')                                      # Get holdout node
            if holdout is None:
                holdout = nodes.new
        Head.active_material = mat                                              # Apply holdout material to head mesh
        
        
    elif cond == 0 or cond == 2: #====================== Render full face
        bpy.data.objects['MacaqueHeadNG_1expressions1'].hide_render = False
        bpy.data.objects['TeethDown'].hide_render                   = False
        bpy.data.objects['TeethUp'].hide_render                     = False
        bpy.data.objects['Tongue_1'].hide_render                    = False


    for exp in ExpNo:

        #======= Set primary expression
        #bpy.ops.object.mode_set(mode='POSE')
        head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]))               # Wide mouthed 'yawn' expression
        head.pose.bones['Kiss'].location    = mu.Vector((0,0.02*ExpWeights[exp,2],0))               # Pursed lip 'coo' expression
        head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]))               # Open-mouthed 'threat' expression
        head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0],0))              # Bared-teeth 'fear' grimace

        #======= Set micro expression
        head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]))       # Close eye lids (blink)
        head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1],0))        # Retract ears
        head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]))       # Raise brow
        head.pose.bones['EyesTracker'].scale = mu.Vector((0, 0.2+0.8*ExpMicroWeights[mexp, 3], 0))  # Pupil dilation/ constriction

        #======= condition 2 = eyes closed
        if cond == 2:
            head.pose.bones['blink'].location           = mu.Vector((0,0,0.02))
            bpy.data.objects['CorneaL'].hide_render     = True
            bpy.data.objects['CorneaR'].hide_render     = True
            bpy.data.objects['EyeL'].hide_render        = True
            bpy.data.objects['EyeR'].hide_render        = True

        #for s in Scales:
        #head.scale = mu.Vector((s, s, s))
        s = 1
        
        for d in Distances:
            body.location = mu.Vector((OrigBodyLoc[0], OrigBodyLoc[1]+d/100, OrigBodyLoc[2]))

            for Hel in HeadElAngles:
                for Haz in HeadAzAngles:
                    
                    #=========== Rotate head/ body
                    if RotateBody == 1:
                        body.rotation_euler = (math.radians(Hel), 0, math.radians(Haz))
                        
                    elif RotateBody ==0:
                        #bpy.ops.object.mode_set(mode='POSE')
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
                                print("Gaze coordinates =({}, {}, {});".format(*GazeXYZ))
                                head.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, 0.26, 0))


                            #============ Update render and save
                            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                            if cond == 0:
                                Filename = "MacaqueGaze_%s_Haz%d_Hel%d_Gaz%d_Gel%d_dist%d.png" % (ExpStr[exp], Haz, Hel, Gaz, Gel, d)
                            elif cond == 1:
                                Filename = "MacaqueGaze_EyesOnly_%s_Haz%d_Hel%d_Gaz%d_Gel%d_dist%d.png" % (ExpStr[exp], Haz, Hel, Gaz, Gel, d)
                            elif cond == 2:
                                Filename = "MacaqueGaze_EyesClosed_%s_Haz%d_Hel%d_GazNaN_GelNan_dist%d.png" % (ExpStr[exp], Haz, Hel, d)

                            print("Now rendering: " + Filename + " . . .\n")
                            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                            bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering completed!\n")




