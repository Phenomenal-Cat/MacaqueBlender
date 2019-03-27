#==========================  Exp_LoomingVox_Render.py ==========================
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
import glob
from GetOSpath import GetOSpath
from sys import platform
import numpy as np
from InitBlendScene import InitBlendScene
import pdb

from bpy_extras.io_utils import ImportHelper

#============== Update head angle
def HeadLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ

#======================= LOAD FILE NAMES
def GetAllParamsFiles():
    [Prefix, temp] = GetOSpath()
    DataDir     = Prefix + 'murphya/MacaqueFace3D/Macaque_video/ExtractedParams/'
    MovieDir    = Prefix + 'murphya/MacaqueFace3D/Macaque_video/OriginalMovies/'
    OutputDir   = Prefix + 'murphya/Stimuli/AvatarRenders_2018/LoomingVox/RenderedFrames/' 
    
    os.chdir(DataDir)
    DataFiles = sorted(glob.glob("*.csv"))
    os.chdir(MovieDir)
    MovieFiles =  sorted(glob.glob("*.mpg"))
    return (DataDir, DataFiles, MovieDir, MovieFiles, OutputDir)

#======================= READ PARAMS DATA
def ReadParamsData(ParamsFile):
    with open(ParamsFile, "rt") as csvfile:
        reader = csv.reader(csvfile)    
        AllData = list(reader)
    csvfile.close()
    return AllData

#======================= ITERATE THROUGH CLIPS
LoadOrigMovie   = 0                                         # Render original movie to a plane in the scene?
InitBlendScene(2, 1, 95)
[DataDir, ParamsFiles, MovieDir, MovieFiles, OutputDir] = GetAllParamsFiles()
for n in range(0, len(ParamsFiles)):
    f           = ParamsFiles[n]
    DataFile    = f[0:-4]
    AllData     = ReadParamsData(DataDir + f)
    print("Rendering " + f)

    ExampleOutputDir = OutputDir + f[0:-4]
    if os.path.isdir(ExampleOutputDir)==0:
        os.mkdir(ExampleOutputDir)
        
    IsCoo   = f.find("Bark")==-1 & f.find("Scream")==-1         # Is the main facial expression a 'coo' face?

    #============== Set parameters
    BoneNames       = ['blink',     'Kiss',     'jaw',  'ears',     'Fear',     'yawn',     'eyebrow',  'HeadTracker']      # Bone names
    BoneVectorIndx  = [2,           1,          2,      1,          1,          2,          2,          1]                  # Which channel (X,Y or Z) to apply values to
    BoneDirection   = [1,           1,          1,      1,         -1,         1,          -1,         -1]                 # Direction for each bone
    BoneWeight      = [0.007,       0.04,       0.02,   0.02,       0.02,       0.02,       0.02,       1]                  # Maximum values for each bone position
    BoneOffset      = [0,           0,          0,      0.02,       0,          0,          0,          0]                  
    HeadAzimuths    = [0]
    
    if IsCoo == 1:                          # If the expression being used is 'coo'
        BoneWeight[2] = 0                   # Turn off jaw movements
        print('Using kiss expression...')

    if f.find("BarkGrowl")>0:               # For lip retraction during 'BarkGrowl'
        BoneWeight[4] = BoneWeight[4]/2     # Reduce weight of lip retraction by 50%
        print('Bark growl detected...')

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

    #============= Frame rate
    FrameDur        = float(AllData[2][0])                              # Get duration of each frame of data
    FPS             = 1/FrameDur                                        # Calculate data frame rate
    OutputFPS       = 30                                                # Specify desired output frame rate
    FrameRatio      = round(OutputFPS/FPS)                              # Calculate ratio of input vs output frame rates

    body            = bpy.data.objects["Root"]
    head            = bpy.data.objects["HeaDRig"]                       # Get handle for macaque avatar head
    head2           = bpy.context.object
    #bpy.ops.object.mode_set(mode='POSE')                                # Enter pose mode

    #bpy.context.scene.cycles.samples        = 10               # <<<< Temporary override for quick test rendering
        
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
    NoFrames                    = OutputFPS*2
    VoxStartFrame               = round((NoFrames/2)-(len(AllData)-1)/2)
    scn                         = bpy.context.scene
    scn.frame_start             = 1         
    scn.frame_end               = NoFrames                                  # How many frames in animation?
    scn.render.frame_map_old    = 1         
    scn.render.frame_map_new    = 1         
    scn.render.fps              = OutputFPS                             # Set frames per second
    scn.render.use_placeholder  = True
    scn.render.use_overwrite    = 0
    
    
    PosExtremes     = [-0.20, 0, 0.20]                                  # Minimum and maximum position in depth (relative to screen in cm)
    PosInDepth      = np.empty([5, NoFrames])
    for pos in range(0, len(PosExtremes)):
        PosInDepth[pos]   = np.tile(PosExtremes[pos], NoFrames)
    PosInDepth[len(PosExtremes)]    = np.linspace(PosExtremes[0], PosExtremes[2], NoFrames)
    PosInDepth[len(PosExtremes)+1]  = np.linspace(PosExtremes[2], PosExtremes[1], NoFrames)
    
    #============== Add keyframes
    for pos in range(0, len(PosInDepth)):
        for haz in HeadAzimuths:

            frame = 1
            for n in AllData[1:]:
                timestamp   = float(AllData[frame][0])                                                                  # Get timestamp of current data frame 
                #bpy.ops.anim.change_frame(frame = round((frame-1)*FrameRatio))                                         # Move timeline to correct output frame
                bpy.context.scene.frame_set( round((frame-1)*FrameRatio) )                                              # Move timeline to correct output frame

                body.location = mu.Vector((0, PosInDepth[pos][frame-1], 0))                                             # Update avatar position in depth

                for exp in range(0, len(BoneNames)):                       
                    if AllData[frame][exp+1]=='NaN':
                        AllData[frame][exp+1] = 0                         
                    if exp < 7:                                                                                                                                 # For each bone...
                        Vector                                          = mu.Vector((0,0,0))                                                                    # Initialize location vector
                        Vector[ BoneVectorIndx[exp] ]                   = BoneOffset[exp] + (BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1]))   # Set relevant vector component
                        head.pose.bones[ BoneNames[exp] ].location      = Vector                                                                                # Apply to bone location
                        # head.pose.bones[ AllData[0][col] ].location   = Vector                                                                                # 
                        #bpy.ops.anim.keyframe_insert_menu(type='Location')                                                                                     # Add keyframe
                        bpy.context.object.keyframe_insert(data_path="location", index=-1)                                                                      # Add keyframe
                        
                    elif exp == 7:
                        if len(AllData[frame]) < exp+1:
                            print('Error: params doesn''t include head elevation data!')
                        print('Adjusting head elevation')
                        hel     = BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1])   
                        HeadXYZ = HeadLookAt(hel, haz)
                        head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                                   
                    #pdb.set_trace()                                                                                                   


                #======= Insert keyframe
                #bpy.ops.anim.keyframe_insert_menu(type='Location')
                
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                Filename = "%s_animation_DepthCond%d_%03d.png" % (DataFile, pos, frame)
                if os.path.isfile(ExampleOutputDir + "/" + Filename) == 0:
                    print("Now rendering: " + Filename + " . . .\n")
                    bpy.context.scene.render.filepath = ExampleOutputDir + "/" + Filename
                    bpy.ops.render.render(write_still=True, use_viewport=True)
                elif os.path.isfile(ExampleOutputDir + "/" + Filename) == 1:
                    print("File " + Filename + " already exists. Skipping . . .\n")

                frame += 1

    print("Rendering completed!\n")
    
    if LoadOrigMovie == 1:
        bpy.data.objects[DataFile].hide_render   = True         # Hide video plane before creating next!

