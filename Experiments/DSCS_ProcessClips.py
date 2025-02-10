#================ CompileMovieClips.py ===================
# Load a series of movie clips and concatenate them into a 
# block of continuous or intermittent presentations.

import bpy
import numpy as np
import mathutils as mu
import math
import socket
import os
import glob
from sys import platform
import random
from moviepy.editor import VideoFileClip




#=========== Check input files
def CheckInputFiles(ClipDir):
    fileList = [ ] 
    for file in os.listdir(ClipDir):
        if file.endswith(InputFormat):
            clip = VideoFileClip(file)
            
            
            Duration = clip.duration
            if Duration >= DurPerClip:
                fileList.append(os.path.join(ClipDir, file))
            else:
                print("WARNING: clip %s is less than the requested duration (%.2f seconds)!\n", file, Duration)
            
    NoClips             = int(BlockDuration/(DurPerClip+InterClipInterval))
    if (len(fileList) < NoClips):
        print("ERROR: number of %s files in %s (%d) is less than the number required (%d)!\n" % (InputFormat, MovieDir, len(fileList), NoClips))                                  # Pseudorandomly shuffle order of clips
    return fileList

#=========== Check video file duration

RootDir         = "/Volumes/NIFVAULT/projects/murphyap_NIF/NIF_Stimuli/"
#RootDir         = "/Volumes/Seagate Backup 3/NIH_Stimuli/Movies/"
MovieDir        = os.path.join(RootDir, "DSCS_Clipped/DSCS_Identity/")
OutputDir       = os.path.join(RootDir, "DSCS_Clipped/DSCS_Identity/Blocks/")
CategoryNames   = ['Adults', 'Cats', 'Elderly', 'FacialDeformities', 'Heterospecifics', 'Infants']
InputFormat     = ".mp4"

#=========== Render settings
FLipHorizontal      = 0                         # Create horizontally flipped copies?
DurPerClip          = 2.0                       # Individual clip duration (seconds)
BackgroundRGB       = (0.5, 0.5, 0.5)           # Set background color (if not full screen)
AudioOn             = 0                         # Encode original audio?
    
#=========== Set video output properties
S  = bpy.context.scene
if not S.sequence_editor:                               # If sequence editor doesn't exist...
    SE = S.sequence_editor_create()                     # Create sequence editor
else:
    SE = bpy.context.scene.sequence_editor
    
#S.render.image_settings.file_format    = 'H264'        # Set render format
S.render.image_settings.file_format     = 'FFMPEG'      # Set render format
S.render.ffmpeg.audio_codec             = 'MP3'                 
S.render.ffmpeg.format                  = 'MPEG4'
S.render.ffmpeg.codec                   = 'H264'
S.render.ffmpeg.constant_rate_factor    = 'PERC_LOSSLESS'

#======= Set output parameters to match original video clips
S.render.resolution_x           = 1920
S.render.resolution_y           = 1080
S.render.resolution_percentage  = 100
S.render.fps                    = 30
S.render.fps_base               = 1.0
FramesPerClip                   = S.render.fps*DurPerClip
MovieChannel                    = 1             # Which video sequence editor channel to put movie clips on


#======== Add background and foreground images
#Bkg     = SE.sequences.new_effect('Background', 'COLOR', 1, 1, frame_end=TotalFrames)    # Background
#SE.sequences_all["Background"].color = (BackgroundRGB);
#Frg     = SE.sequences.new_image('Foreground', DepthArrayIm, 3, 1)                      # Foreground
#SE.sequences_all["Foreground"].blend_type          = 'ALPHA_OVER'
#SE.sequences_all["Foreground"].frame_final_end     = len(FrameOrder)+1

#=========== Load all files
for cat in CategoryNames:
    ClipDir                 = os.path.join(MovieDir, cat)
    [fileList]   = CheckInputFiles(ClipDir)
    
    OriginalLengthFrames = []
    
    CurrentFrame = 1
    for c in range(len(fileList)):             
        ClipFile        = fileList[c]
        ClipName        = ClipFile   
        Fullfile        = os.path.join(ClipDir, ClipFile)
        
        SE.sequences.new_movie(ClipName, Fullfile, MovieChannel, S.frame_start)
        OriginalLengthFrames[c] = SE.sequences_all[ClipName].frame_final_duration
        
        if SE.sequences_all[ClipName].fps != S.render.fps:
            S.render
        
        if OriginalLengthFrames[c] > FramesPerClip:
            Diff = OriginalLengthFrames[c]- FramesPerClip
            StartFrame  = random.randrange(Diff)
            EndFrame    = StartFrame + FramesPerClip -1
            
        else:
            StartFrame  = 1
            EndFrame    = FramesPerClip
            
        S.frame_start                   = StartFrame
        S.frame_end                     = EndFrame
        
        
        SE.sequences_all[ClipName].frame_final_duration = S.render.fps*DurPerClip
        CurrentFrame    = CurrentFrame+(S.render.fps*(DurPerClip+InterClipInterval))
            
        #======== Save block to new movie file
        OutputFile = os.path.join(OutputDir, cat,  + '.mp4')
        bpy.context.scene.render.filepath = OutputFile
        bpy.ops.render.render(animation=True)
        
        #======== Clear VSE
        for strip in SE.sequences:
            SE.sequences.remove(strip)
