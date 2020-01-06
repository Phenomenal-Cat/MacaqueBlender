
#============= Exp_RaysonExp_Compile.py

import bpy
import mathutils
import math
import numpy
import socket
import os
import glob
from sys import platform
import numpy as np
import pdb


#======================= LOAD FILE NAMES
def GetAllParamsFiles():
    RootDir     = '/Volumes/Kastner/aidanm/BlenderRenders/Rayson-Ferrari/'
    FramesDir   = os.path.join(RootDir, 'Frames4K')
    OutputDir   = os.path.join(RootDir, 'Animations')

    FrameImages = []
    MovieName   = []
    Objects     = ['Macaque']
    Expressions = ['Fear','Threat','LipSmack','Chewing','Neutral']
    HazAngles   = [-20, 20, 0, 0, 0]
    GazAngles   = [0, 0, -20, 20, 0]
    NoFrames    = 120
    MovNo       = 0
    for ob in Objects:
        for exp in Expressions:
            for haz in HazAngles:
                for gaz in GazAngles:
                    FrameImages.append([])
                    SubDir = 'Haz%d_Gaz%d/' % (haz, gaz)
                    MovieName.append('%s_%s_Haz%d_Gaz%d' % (ob, exp, haz, gaz))
                    SearchPath  = os.path.join(FramesDir, exp, SubDir)
                    print(SearchPath)
                    Filenames   = [f for f in os.listdir(SearchPath) if f.endswith('.png')]
                    for f in range(0, len(Filenames)):
                        Filename = "{:03d}.png".format(MovieName[MovNo], f+1)
                        Fullfile = os.path.join(FramesDir, exp, SubDir, Filenames[f])
                        FrameImages[MovNo].append(Fullfile)

                    MovNo=MovNo+1
                
    return (FramesDir, FrameImages, MovieName, OutputDir, DepthArrayIm)


#============= Set video encoding params
[FramesDir, FrameImages, MovieName, OutputDir, DepthArrayIm] = GetAllParamsFiles()

BackgroundRGB       = (0, 0, 0)                   # Background color (if plain)
PrefixNeutral       = 1                                 # Add neutral expression motion prior to main sequence?
PrefixFrames        = 30                                # How many frames of prior motion to add


S  = bpy.context.scene
if not S.sequence_editor:                               # If sequence editor doesn't exist...
    SE = S.sequence_editor_create()                     # Create sequence editor
else:
    SE = bpy.context.scene.sequence_editor
#S.render.image_settings.file_format    = 'H264'            # Set render format
S.render.image_settings.file_format     = 'FFMPEG'            # Set render format
S.render.ffmpeg.audio_codec             = 'MP3'                 
S.render.ffmpeg.format                  = 'MPEG4'
S.render.ffmpeg.codec                   = 'H264'
S.render.ffmpeg.constant_rate_factor    = 'PERC_LOSSLESS'
    
#======= Set output parameters to match or modify original video clips
S.render.resolution_x           = 3840
S.render.resolution_y           = 2160
S.render.resolution_percentage  = 50            # Reduce output resolution %?
S.render.fps                    = 60            
S.render.fps_base               = 1.0           
S.frame_start                   = 1             # Which frame number to start animation render from
FirstFrame                      = 30            # Which frame to put in frame #1 slot? 
ReverseFrameOrder               = 0             # Start movie with last frame?


#============= Loop through clips with rendered frames
for MovNo in range(0, len(MovieName)):
    
    S.render.filepath   = os.path.join(OutputDir + MovieName[MovNo] + ".mp4")       # Set output filename
    if os.path.isfile(S.render.filepath) == 0:                                      # If file doesn't already exist...
        
        #======== Load video frames
        NoFrames    = len(FrameImages[MovNo])
        print('Loading {:d} frames for movie clip {:s}'.format(NoFrames, MovieName[MovNo]))
        
        if ReverseFrameOrder == 0:
            FrameOrder  = np.concatenate((np.linspace(1, NoFrames, NoFrames, dtype=int), np.linspace(NoFrames, 1, NoFrames, dtype=int)))
        elif ReverseFrameOrder == 1:
            FrameOrder  = np.concatenate((np.linspace(NoFrames, 1, NoFrames, dtype=int), np.linspace(1, NoFrames, NoFrames, dtype=int)))
        if FirstFrame > 1:
            FrameOrder  = np.concatenate((FrameOrder[FirstFrame-1:], FrameOrder[0:FirstFrame-1]))
            
        for f in range(0, len(FrameOrder)):
            SE.sequences.new_image("Frame{:03d}".format(f+1), FrameImages[MovNo][FrameOrder[f]-1], 2, f+1)    # Add rendered frame images to SE
        
        for s in SE.sequences_all:
            s.blend_type = 'ALPHA_OVER'
            
        S.frame_end                     = len(FrameOrder)                               # Set clip length based on number of frames

        #======== Add background and foreground images
        Bkg     = SE.sequences.new_effect('Background', 'COLOR', 1, 1, len(FrameOrder)+1)       # Background
        SE.sequences_all["Background"].color = (BackgroundRGB);
        Frg     = SE.sequences.new_image('Foreground', DepthArrayIm, 3, 1)                      # Foreground
        SE.sequences_all["Foreground"].blend_type               = 'ALPHA_OVER'
        SE.sequences_all["Foreground"].frame_final_end     = len(FrameOrder)+1

        #======== Render to movie file
        bpy.ops.render.render(animation = True)                                         # Render animation 
        
        #======== Remove video frames
        bpy.ops.sequencer.select_all()                                                  # Select all clips
        bpy.ops.sequencer.delete()                                                      # Delete selected clips
    
    else:
        print('Movie file {:s} already exists! Skipping...'.format(MovieName[MovNo]))
    
print('Video endcoing completed!')

