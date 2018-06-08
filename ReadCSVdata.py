#==========================  ReadCSVdata.py ==================================
# This script reads timecourse data from the specified CSV files (previously extracted from video clips) 
# and applies it to keyframes of the appropriate bones/ shape keys. CSV file should contain
# N columns, each with a header row containing the string of the Blender scene bone/ shape key to
# apply to. The first column should contain timestamps (seconds).
#
#
# 05/08/2018 - Written by murphyap@nih.gov
#=============================================================================

import bpy
import csv
import math
import mathutils as mu
import os
from sys import platform
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


#======================= LOAD DATA
if platform == "linux":
    Prefix = '/projects/'
elif platform == "darwin":
    Prefix = '/Volumes/projects/'
elif platform == "win32":
    Prefix = 'P:/'

DataFile        = 'BE_Coo_mov53'                                 # Name of video clip used
IsCoo           = 1                                                 # Is the main facial expression a 'coo' face?
LoadOrigMovie   = 0                                                 # Render original movie to a plane in the scene?

DataDir     = Prefix + 'murphya/MacaqueFace3D/Macaque_video/ExtractedParams/'
OutputDir   = Prefix + 'murphya/MacaqueFace3D/Macaque_video/RenderedFrames/' + DataFile + '/'
MovieFile   = Prefix + 'murphya/MacaqueFace3D/Macaque_video/OriginalMovies/' + DataFile + '.mpg'
DataFull    = DataDir + DataFile + '.csv'
if os.path.exists(OutputDir) ==0:
    os.mkdir(OutputDir)

with open(DataFull, "rt") as csvfile:
    reader = csv.reader(csvfile)    
    AllData = list(reader)
    
csvfile.close()

#============== Set parameters
BoneNames       = ['blink', 'Kiss', 'jaw', 'ears', 'Fear', 'yawn', 'eyebrow', 'HeadTracker']
BoneVectorIndx  = [2, 1, 2, 1, 1, 2, 2, 1]
BoneDirection   = [1, 1, 1, -1, -1, 1, -1, -1]
BoneWeight      = [0.007, 0.04, 0.02, 0.04, 0.02, 0.02, 0.02, 1] 
BoneOffset      = [0, 0, 0, 0.02, 0, 0, 0, 0]
HeadAzimuths    = [-60, -30, 0, 30, 60]

#    #======= Set primary expression
#    bpy.ops.object.mode_set(mode='POSE')
#    head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]))           # Wide mouthed 'yawn' expression
#    head.pose.bones['Kiss'].location    = mu.Vector((0,0.04*ExpWeights[exp,2],0))           # Pursed lip 'coo' expression
#    head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]))           # Open-mouthed 'threat' expression
#    head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0],0))          # Bared-teeth 'fear' grimace
#
#    #======= Set micro expression
#    head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]))   # Close eye lids (blink)
#    head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1],0))    # Retract ears
#    head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]))   # Raise brow
#    head.pose.bones['EyesTracker'].scale = mu.Vector((0, 1*ExpMicroWeights[mexp, 3], 0))    # Pupil dilation/ constriction

FrameDur        = float(AllData[2][0])                              # Get duration of each frame of data
FPS             = 1/FrameDur                                        # Calculate data frame rate
OutputFPS       = 30                                                # Specify desired output frame rate
FrameRatio      = round(OutputFPS/FPS)                              # Calculate ratio of input vs output frame rates

head            = bpy.data.objects["HeaDRig"]                       # Get handle for macaque avatar head
head2           = bpy.context.object
#bpy.ops.object.mode_set(mode='POSE')                                # Enter pose mode


#============== Load reference movie to 3D plane
if LoadOrigMovie == 1:
    HeadAzimuths    = [0]
    bpy.data.objects['Camera'].location = mu.Vector((-0.1, -1, 0))
    
    mc = bpy.data.movieclips.load(MovieFile)
    bpy.ops.import_image.to_plane(files=[{'name': os.path.basename(MovieFile)}],
            directory=os.path.dirname(MovieFile))
    bpy.data.objects[DataFile].rotation_euler  = mu.Vector((math.radians(90), 0, 0))
    bpy.data.objects[DataFile].location        = mu.Vector((-0.2, 0, 0))
    bpy.data.objects[DataFile].scale           = ((0.15, 0.15, 0.15))   
    
#============== For 'coo' vocalizations...
if IsCoo == 1:
    bpy.data.objects['TeethDown'].hide_render   = True
    bpy.data.objects['TeethUp'].hide_render     = True
    bpy.data.objects['Tongue_1'].hide_render    = True
elif IsCoo == 0:
    bpy.data.objects['TeethDown'].hide_render   = False
    bpy.data.objects['TeethUp'].hide_render     = False
    bpy.data.objects['Tongue_1'].hide_render    = False

#================== Set animation parameters
scn                         = bpy.context.scene
scn.frame_start             = 1         
scn.frame_end               = (len(AllData)-1)*FrameRatio           # How many frames in animation?
scn.render.frame_map_old    = 1         
scn.render.frame_map_new    = 1         
scn.render.fps              = OutputFPS                             # Set frames per second
scn.render.use_placeholder  = 1
scn.render.use_overwrite    = 0

#============== Add keyframes
for haz in HeadAzimuths:

    frame = 1
    for n in AllData[1:]:
        timestamp   = float(AllData[frame][0])                                                                  # Get timestamp of current data frame 
        #bpy.ops.anim.change_frame(frame = round((frame-1)*FrameRatio))                                         # Move timeline to correct output frame
        bpy.context.scene.frame_set( round((frame-1)*FrameRatio) )                                              # Move timeline to correct output frame

        exp = 0
        for e in BoneNames:                                                
            if exp < 7:                                                                                                                                 # For each bone...
                Vector                                          = mu.Vector((0,0,0))                                                                    # Initialize location vector
                Vector[ BoneVectorIndx[exp] ]                   = BoneOffset[exp] + BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1])     # Set relevant vector component
                head.pose.bones[ BoneNames[exp] ].location      = Vector                                                                                # Apply to bone location
                # head.pose.bones[ AllData[0][col] ].location   = Vector                                                                                # 
                #bpy.ops.anim.keyframe_insert_menu(type='Location')                                                                                     # Add keyframe
                bpy.context.object.keyframe_insert(data_path="location", index=-1)                                                                      # Add keyframe
            elif exp == 7:
                hel     = BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1])   
                HeadXYZ = HeadLookAt(hel, haz)
                head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
            exp += 1                                                                                                                


        #======= Insert keyframe
        #bpy.ops.anim.keyframe_insert_menu(type='Location')
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        Filename = "%s_animation_Haz%d_%d.png" % (DataFile, haz, frame)
        if os.path.isfile(OutputDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = OutputDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(OutputDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")

        frame += 1

print("Rendering completed!\n")

