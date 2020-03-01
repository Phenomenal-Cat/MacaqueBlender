
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
    RootDir     = '/Volumes/Seagate Backup 3/NIH_Stimuli/MF3D_R1/MF3D_Animations_V2/'
    FramesDir   = os.path.join(RootDir, 'Frames/')
    OutputDir   = os.path.join(RootDir, 'Animations2/')

    FrameImages = []
    MovieName   = []
    Expressions = ['Fear','Threat','LipSmack','Chewing','Yawn','Neutral']
    HazAngles   = [-60, -30, 0, 30, 60]
    GazAngles   = [0, 0, 0, 0, 0]
    NoFrames    = 120
    MovNo       = 0
    for exp in Expressions:
        SearchPath  = os.path.join(FramesDir, exp)
        Filenames   = [f for f in os.listdir(SearchPath) if f.endswith('.png')]
        Filenames.sort()
        print(Filenames)
        
        for az in range(0, len(HazAngles)):
            FrameImages.append([])
            SubDir = 'Haz%d_Gaz%d/' % (HazAngles[az], GazAngles[az])
            MovieName.append('MF3D_Animation_4K_%s_Haz%d_Gaz%d' % (exp, HazAngles[az], GazAngles[az]))
            FrameIndx = az*NoFrames
            print(az)
            print(FrameIndx)
            if len(Filenames) < NoFrames:
                print('Warning: only %d frames were found for movie %s!' % (len(Filenames), MovieName[-1]))

            for f in range(FrameIndx, (FrameIndx+NoFrames)):
                Fullfile = os.path.join(FramesDir, exp, Filenames[f])
                FrameImages[MovNo].append(Fullfile)

            MovNo=MovNo+1
            
    return (FramesDir, FrameImages, MovieName, OutputDir)


#============= Set video encoding params
[FramesDir, FrameImages, MovieName, OutputDir] = GetAllParamsFiles()

BackgroundRGB       = (0, 0, 0)                         # Background color (if plain)
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
S.render.resolution_percentage  = 100            # Reduce output resolution %?
S.render.fps                    = 60            
S.render.fps_base               = 1.0           
S.frame_start                   = 1             # Which frame number to start animation render from
S.frame_end                     = 120
FirstFrame                      = 1            # Which frame to put in frame #1 slot? 
ReverseFrameOrder               = 0             # Start movie with last frame?


#============= Loop through clips with rendered frames
for MovNo in range(0, len(MovieName)):
    
    S.render.filepath   = os.path.join(OutputDir + MovieName[MovNo] + ".mp4")       # Set output filename
    if os.path.isfile(S.render.filepath) == 0:                                      # If file doesn't already exist...
        
        #======== Load video frames
        NoFrames    = len(FrameImages[MovNo])
        print('Loading {:d} frames for movie clip {:s}'.format(NoFrames, MovieName[MovNo]))
        
        FrameOrder = np.linspace(0, NoFrames, NoFrames+1, dtype=int);
        print(FrameOrder)
        print(len(FrameImages[MovNo]))
        for f in range(0, len(FrameImages[MovNo])):
            seq = SE.sequences.new_image(MovieName[MovNo], filepath=FrameImages[MovNo][FrameOrder[f]], channel=2, frame_start=f+1)    # Add rendered frame images to SE

        S.frame_end                     = len(FrameOrder)-1                               # Set clip length based on number of frames

        #======== Add background and foreground images
        if not 'Bkg' in locals():
            Bkg     = SE.sequences.new_effect('Background', 'COLOR', channel=3, frame_start=1, frame_end=len(FrameOrder)+1)       # Background
            SE.sequences_all["Background"].color        = (BackgroundRGB);
            SE.sequences_all["Background"].blend_type   = 'ALPHA_UNDER'

        #======== Render to movie file
        bpy.ops.render.render(animation = True)                                         # Render animation 
        SE.sequences.remove(seq)                                                        # Remove video frames
#        bpy.ops.sequencer.select_all()                                                  # Select all clips
#        bpy.ops.sequencer.delete()                                                      # Delete selected clips
    
    else:
        print('Movie file {:s} already exists! Skipping...'.format(MovieName[MovNo]))
    
    
    
print('Video endcoing completed!')

