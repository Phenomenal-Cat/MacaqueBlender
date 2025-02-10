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
from random import shuffle


#MovieDir        = "/Volumes/Seagate Backup 1/Stimuli/Movies/MonkeyThieves/MacaqueClips/FacialDeformities/"
MovieRootDir    = "/Users/murphyap/Documents/NIF_Stimuli/DSCS_Clipped/DSCS_Identity/"
MovieSubDir     = "Cats"
MovieDir        = os.path.join(MovieRootDir, MovieSubDir)
InputFormat     = ".mp4"

#=========== Render settings
NoPermutations      = 1                         # How many blocks/ output movies to generate
DurPerClip          = 2                       # Individual clip duration (seconds)
InterClipInterval   = int(0)                         # Duration of blank interval between clips
BlockDuration       = 40                        # Duration of full concatenated block (seconds)
BackgroundRGB       = (0.5, 0.5, 0.5)           # Set background color (if not full screen)
AudioOn             = 0                         # Encode original audio?
AddPhotodiode       = 0                         # Add photodiode marker for stimulus onsets?

#=========== Check input files
fileList = [ ] 
for file in os.listdir(MovieDir):
    if file.endswith(InputFormat):
        fileList.append(os.path.join(MovieDir , file))
        
NoClips             = int(BlockDuration/(DurPerClip+InterClipInterval))
if (len(fileList) < NoClips):
    print("ERROR: number of %s files in %s (%d) is less than the number required (%d)!\n" % (InputFormat, MovieDir, len(fileList), NoClips))
ClipOrder = [i for i in range(NoClips)]
shuffle(ClipOrder)                              # Pseudorandomly shuffle order of clips

#=========== 
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
S.render.resolution_x           = 1920
S.render.resolution_y           = 1080
S.render.resolution_percentage  = 100
S.render.fps                    = 30
S.render.fps_base               = 1.0
S.frame_start                   = int(1)
MovieChannel                    = 1             # Which video sequence editor channel to put movie clips on
TotalFrames                     = BlockDuration*S.render.fps

#=========== Load all files
for b in range(NoPermutations):
    shuffle(ClipOrder)                          # Pseudo-randomly shuffle order of clips
    
    CurrentFrame = int(0)
    for c in range(NoClips):             
        ClipName        = "Clip %d" % c       
        ClipFile        = fileList[ClipOrder[c]]
        CurrentFrame    = CurrentFrame+int(S.render.fps)*(DurPerClip+InterClipInterval)
        SE.sequences.new_movie(ClipName, ClipFile, int(b)+2, CurrentFrame)
        SE.sequences_all[ClipName].frame_final_duration = S.render.fps*DurPerClip
        
        


#======== Add background and foreground images
Bkg     = SE.sequences.new_effect('Background', 'COLOR', 1, 1, TotalFrames)       # Background
SE.sequences_all["Background"].color = (BackgroundRGB);
#Frg     = SE.sequences.new_image('Foreground', DepthArrayIm, 3, 1)                      # Foreground
#SE.sequences_all["Foreground"].blend_type          = 'ALPHA_OVER'
#SE.sequences_all["Foreground"].frame_final_end     = len(FrameOrder)+1

#======== Render to movie file
#bpy.ops.render.render(animation = True)                                         # Render animation 
