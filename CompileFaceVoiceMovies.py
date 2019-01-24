
#============= GenerateFaceVoiceMovies.py

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
    FramesDir   = Prefix + 'murphya/MacaqueFace3D/Macaque_video/RenderedFrames/' 
    AudioDir    = Prefix + 'murphya/MacaqueFace3D/Macaque_video/OriginalWAVs/'
    #OutputDir   = Prefix + 'murphya/MacaqueFace3D/Macaque_video/RenderedComparisons/'
    OutputDir   = Prefix + 'murphya/MacaqueFace3D/Macaque_video/RenderedMovies/'
    AudioFiles  = sorted(glob.glob(os.path.join(AudioDir, "*.wav")))
    ClipNames   = sorted(next(os.walk(FramesDir))[1])
    HazAngles   = [-60, -30, 0, 30, 60]
    FrameImages = []
    for c in range(0, len(ClipNames)):
        #FrameImages.append(sorted(glob.glob(os.path.join(FramesDir + ClipNames[c] + '/Comparison', "*.png"))))
        for haz in HazAngles:
            FrameImages.append(sorted(glob.glob(os.path.join(FramesDir + ClipNames[c], ClipNames[c] + "_animation_Haz%d" % haz + "*.png"))))
        
    return (ClipNames, AudioDir, AudioFiles, FramesDir, FrameImages, OutputDir)


#============= Set video encoding params
[ClipNames, AudioDir, AudioFiles, FramesDir, FrameImages, OutputDir] = GetAllParamsFiles()

HazAngles   = [-60, -30, 0, 30, 60]

S  = bpy.context.scene
if not S.sequence_editor:                               # If sequence editor doesn't exist...
    SE = S.sequence_editor_create()                     # Create sequence editor
else:
    SE = bpy.context.scene.sequence_editor
#S.render.image_settings.file_format = 'H264'            # Set render format
S.render.image_settings.file_format = 'FFMPEG'            # Set render format
S.render.ffmpeg.audio_codec         = 'MP3'                 
S.render.ffmpeg.format              = 'MPEG4'
S.render.ffmpeg.codec               = 'H264'
S.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
    
#======= Set output parameters to match original video clips
S.render.resolution_x           = 1080
S.render.resolution_y           = 1080
S.render.resolution_percentage  = 100
S.render.fps                    = 30
S.render.fps_base               = 1.0
S.frame_start                   = 1 
FirstFrames                     = round(0.5*S.render.fps)

#============= Loop through clips with rendered frames
for c in range(0, len(ClipNames)):
    
    #======== Load audio file
    ac = bpy.data.sounds.load(AudioFiles[c])
    ah = SE.sequences.new_sound(FramesDir[c], AudioFiles[c], 2, 1)                      # Load audio file
    ah.frame_start  = FirstFrames+1                                                     # Set start frame
    ah.pitch        = 1;                                                                # Set relative pitch
    ah.volume       = 1;                                                                # Set volume
    ah.pan          = 0;                                                                # Set left-right balance
    
    #======== Loop through head angles
    for haz in range(0, len(HazAngles)):
    
        #======== Load video frames
        print('Loading frames for movie clip ' + ClipNames[c] + ', head azimuth %d' % HazAngles[haz] )
        ClipIndx = c*len(HazAngles) + haz
        
        for f in range(0, FirstFrames+1):
            SE.sequences.new_image(ClipNames[c]+ ("_frame01"), FrameImages[ClipIndx][0], 1, f+1) 
        
        for f in range(1, len(FrameImages[ClipIndx])):
            SE.sequences.new_image(ClipNames[c]+ ("_frame%02d" % f), FrameImages[ClipIndx][f], 1, f+FirstFrames+1)     # Add rendered frame images to sequence editor
            
        S.frame_end                     = len(FrameImages[ClipIndx]) + FirstFrames                                      # Set clip length based on number of frames

        #======== Render to movie file
        #S.render.filepath   = OutputDir + ClipNames[c] + "_comparison.mp4"              # Set output filename
        S.render.filepath   = os.path.join(OutputDir + ClipNames[c], ClipNames[c] + "_Haz%d.mp4" % HazAngles[haz]) # Set output filename
        if os.path.isfile(S.render.filepath) == 0:                                      # If file doesn't already exist...
            bpy.ops.render.render(animation = True)                                     # Render animation 
        
        #======== Remove video frames
        bpy.ops.sequencer.select_all()                      # Select all clips
        ah.select = False                                   # De-select audio clip
        bpy.ops.sequencer.delete()                          # Delete selected clips
        
    #======== Remove audio
    ah.select = True
    bpy.ops.sequencer.delete()
    
print('Video endcoing completed!')

