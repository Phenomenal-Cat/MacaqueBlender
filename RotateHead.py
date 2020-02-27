

import bpy
import csv
import math
import mathutils as mu
import numpy as np
from bpy_extras.io_utils import ImportHelper

#============== Update head angle
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


HazAngles   = [-60, -30, 0, 30, 60]     # All head azimuth angles to rotate between (degrees)

FPS         = 60
Saccade     = 1                         # Saccade to final gaze direction precedes head rotation?
SaccadeMax  = 30                        # Maximum angle (degrees) of saccade
SaccadeDur  = 0.1                       # Duration of saccade (seconds)
SaccFrames  = round(SaccadeDur*FPS)     # Duration of saccade (frames)
RotSpeed    = 120                       # Average head rotation speed (degrees per second)

#========= Generate all rotation combos
RotCombo = []
for h1 in HazAngles:
    for h2 in HazAngles:
        if h1 != h2:
            RotCombo.append([h1, h2])

print('Total rotation sequences = ' + str(len(RotCombo)))

head            = bpy.data.objects["HeaDRig"]                       # Get handle for macaque avatar head
HeadDefault     = head.pose.bones['HeadTracker'].location
GazeDefault     = head.pose.bones['EyesTracker'].location

FrameCount = 1
for seq in range(0, len(RotCombo)):
    
    RotDeg      = abs(RotCombo[seq][0] - RotCombo[seq][1])
    RotDur      = RotDeg/RotSpeed
    RotFrames   = RotDur*FPS
    GazeDir     = (RotCombo[seq][0] - RotCombo[seq][1])/RotDeg 
    GazeAz      = min(SaccadeMax, RotDeg)*-GazeDir
    
    print('Head rotation '+str(seq)+': '+str(RotCombo[seq][0])+ 'deg to '+str(RotCombo[seq][1])+ 'deg = '+ str(RotFrames)+ 'frames')
    
    # Set head and gaze start positions
    bpy.context.scene.frame_set(FrameCount)
    HeadXYZ_start = HeadLookAt(0, RotCombo[seq][0])
    head.pose.bones['HeadTracker'].location = HeadXYZ_start
    head.pose.bones['HeadTracker'].keyframe_insert(data_path="location")   
    head.pose.bones['EyesTracker'].location = GazeDefault
    head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1) 
    
    # Set saccade end position
    GazeXYZ = GazeLookAt(0, GazeAz)
    bpy.context.scene.frame_set(FrameCount + SaccFrames)
    head.pose.bones['HeadTracker'].location = HeadXYZ_start
    head.pose.bones['HeadTracker'].keyframe_insert(data_path="location")  
    head.pose.bones['EyesTracker'].location = mu.Vector((GazeXYZ[0], GazeDefault[1], GazeDefault[2]))
    head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1)     
    
    # Set head and eye end positions
    bpy.context.scene.frame_set(FrameCount + RotFrames)
    HeadXYZ_end = HeadLookAt(0, RotCombo[seq][1])
    head.pose.bones['HeadTracker'].location = HeadXYZ_end
    head.pose.bones['HeadTracker'].keyframe_insert(data_path="location")   
    head.pose.bones['EyesTracker'].location = mu.Vector((0, GazeDefault[1], GazeDefault[2]))
    head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1) 
    
    # Set earlier end eye position for large head rotations
#    if RotDeg > SaccadeMax:
#        head.pose.bones['EyesTracker'].location = GazeDefault
#        head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1)
    
    
    FrameCount = FrameCount+RotFrames+1
    
    
    
    
    
    
