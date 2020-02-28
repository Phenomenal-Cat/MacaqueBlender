
#====================== MF3D_ConcatClips.py ======================
# This script demonstrates how multiple short animated clips from 
# the MF3D R1 animation stimulus set can be combined to form longer
# sequences of continuous motion.
#
#==================================================================

import bpy
import numpy as np
import os
import csv
import glob
from sys import platform

#======= READ SPREADSHEET DATA
def ReadSummaryData(SummaryFile):
    with open(SummaryFile, "rt") as csvfile:
        reader = csv.reader(csvfile)    
        AllData = list(reader)
    csvfile.close()
    return AllData


MF3D_dir    = '/Volumes/Seagate Backup 3/NIH_Stimuli/MF3D_R1/MF3D_Animations_V2/'
SummaryFile = MF3D_dir + 'MF3D_Animation_Summary.csv'
MF3D_data   = ReadSummaryData(SummaryFile)
    
    
#======= Set output video parameters
S.render.image_settings.file_format     = 'FFMPEG'            # Set render format
S.render.ffmpeg.audio_codec             = 'MP3'                 
S.render.ffmpeg.format                  = 'MPEG4'
S.render.ffmpeg.codec                   = 'H264'
S.render.ffmpeg.constant_rate_factor    = 'PERC_LOSSLESS'
S.render.resolution_x                   = 3840
S.render.resolution_y                   = 2160
S.render.resolution_percentage          = 100
S.render.fps                            = 60
S.render.fps_base                       = 1.0


S  = bpy.context.scene
if not S.sequence_editor:                               # If sequence editor doesn't exist...
    SE = S.sequence_editor_create()                     # Create sequence editor
else:
    SE = bpy.context.scene.sequence_editor
    
