
#============= Exp_ObjectTracking_Compile.py

import bpy
import mathutils
import math
import numpy
import socket
import os
import glob
from GetOSpath import GetOSpath
from sys import platform
import numpy as np
import pdb


#======================= LOAD FILE NAMES
def GetAllParamsFiles():
    [Prefix, temp] = GetOSpath()
    FramesDir   = os.path.join(Prefix, 'murphya/Stimuli/AvatarRenders_2018/ObjectTracking/Frames/')
    OutputDir   = os.path.join(Prefix, 'murphya/Stimuli/AvatarRenders_2018/ObjectTracking/Movies/')
    DepthArrayIm= os.path.join(Prefix, 'murphya/Stimuli/AvatarRenders_2018/SizeDistance/BackgroundArrays/BackgroundArray_01.png')
    FrameImages = []
    MovieName   = []
    Objects     = ['Macaque_eyes','Macaque_head','Apple','Banana']
    NoFrames    = 120
    MovNo       = 0
    Suffix      = "_HeadTrack_360_20cm_frame"
    for ob in Objects:
        FrameImages.append([])
        MovieName.append('%s%s' % (ob, Suffix))
        for f in range(0, NoFrames):
            Filename = "{}_frame{:03d}.png".format(MovieName[MovNo], f+1)
            Fullfile = os.path.join(FramesDir, Filename)
            if os.path.isfile(Fullfile):
                FrameImages[MovNo].append(Fullfile)
            else:
                print("Movie {} is missing expected frames! Skipping...".format(MovieName[MovNo]))
                break
        MovNo=MovNo+1
                
    return (FramesDir, FrameImages, MovieName, OutputDir, DepthArrayIm)


#============= Set video encoding params
[FramesDir, FrameImages, MovieName, OutputDir, DepthArrayIm] = GetAllParamsFiles()

BackgroundRGB       = (0.5, 0.5, 0.5)

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
    
#======= Set output parameters to match original video clips
S.render.resolution_x           = 3840
S.render.resolution_y           = 2160
S.render.resolution_percentage  = 100
S.render.fps                    = 30
S.render.fps_base               = 1.0
S.frame_start                   = 1             # Which frame number to start animation render from
FirstFrame                      = 30            # Which frame to put in frame #1 slot? 
ReverseFrameOrder               = 1             # Start movie with last frame?



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

