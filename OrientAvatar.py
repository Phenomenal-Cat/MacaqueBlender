# ======================== OrientAvatar.py =================================
# This function updates the torso, head, and gaze directions of the macaque 
# model based on the input spherical coordinates (degrees) provided in tuple 
# format as follows: 
#
#       Body:   (Elevation (degres), Azimuth (degrees))
#       Head:   (Elevation (degres), Azimuth (degrees))
#       Gaze:   (Elevation (degres), Azimuth (degrees), Distance (metres))
#
# Positive elevation and azimuth values correspond to upward and clockwise
# rotations respectively. Leave any of the three inputs empty to leave that
# bone in it's current position.
#
# EXAMPLE:
# from OrientAvatar import OrientAvatar
# OrientAvatar((Bel, Baz), (Hel, Haz), (Gel, Gaz, ViewingDistance))
# =======================================================================

import bpy
import numpy as np
import math
import mathutils as mu
    
#=============== 
def HeadLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*-Rad
    Y   = np.sin(math.radians(El))*-Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ

#=============== 
def GazeLookAt(El, Az, Rad=1):
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*-Rad
    Y   = np.sin(math.radians(El))*Rad
    GazeXYZ = mu.Vector((X, Y, Z))
    return GazeXYZ  

#=============== 
def OrientAvatar(BodyEA, HeadEA, GazeEAR):

    #====== Get bone / tracker handles
    BodyBase = bpy.data.objects["Root"]
    HeadBone = bpy.data.objects["HeaDRig"].pose.bones["HeadTracker"]
    GazeBone = bpy.data.objects["HeaDRig"].pose.bones["EyesTracker"]

    #====== Head
    if HeadEA:
        HeadXYZ     = HeadLookAt(HeadEA[0], HeadEA[1])
        HeadBone.location = HeadXYZ
    #====== Gaze  
    if GazeEAR:
        GazeXYZ     = GazeLookAt(GazeEAR[0], GazeEAR[1], GazeEAR[2])
        GazeBone.location = GazeXYZ
    #====== Body
    if BodyEA:
        BodyBase.rotation_euler = [math.radians(-BodyEA[0]), 0, math.radians(-BodyEA[1])]
    
    

#=============== Translate the avatar so that the cyclopean eye is aligned with input coords
def CenterCyclopean(XYZ):
    body                = bpy.data.objects["Root"]
    body.rotation_mode  = 'XYZ'
    EyeLocations        = GetEyeLocations()                         # Get coordinates of eye balls             
    #CyclopeanOrigin     = (EyeLocations[0] + EyeLocations[1])/2     # Average eye ball coordinates to find cyclopean eye coordinates    
    CyclopeanOrigin     = ((0,0,0))  
    bpy.context.scene.cursor_location   = CyclopeanOrigin           # Set current cursor position to cyclopean eye coordinates
    bpy.context.scene.objects.active    = body                      # Set avatar rig as active object
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')                 # Set origin of avatar to cyclopean eye  
    
    
#=============== Get current coordinates of eye balls
def GetEyeLocations():                        
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

    