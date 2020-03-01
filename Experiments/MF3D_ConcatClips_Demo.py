
#====================== MF3D_ConcatClips.py ======================
# This script demonstrates how multiple short animated clips from 
# the MF3D R1 animation stimulus set can be combined to form longer
# sequences of continuous motion.
#
#==================================================================

import bpy
import numpy as np
import os
import glob
from sys import platform
import pdb

IncludeVox          = 0
AddForegroundIm     = 0
AddCaptions         = 1

#======= Read spreadsheet data and generate clip order
MF3D_dir    = '/Volumes/Seagate Backup 3/NIH_Stimuli/MF3D_R1/MF3D_Animations_V2/'
SummaryFile = MF3D_dir + 'MF3D_Animation_Summary.csv'
Dtypes      = ("|U60","|U10","|U20", int, int, "|U10", float, int)
AllData     = np.genfromtxt(SummaryFile, dtype=Dtypes, delimiter=',', names=True)

ExpIndx     = np.where(AllData['Category']=='Exp')              # Find indices of expressions
ExpNames    = np.unique(AllData['Action'][ExpIndx])             # Get unique expression names
VoxIndx     = np.where(AllData['Category']=='Vox')              # Find indices of vocalizations
VoxNames    = np.unique(AllData['Action'][VoxIndx])             # Get unique vocalization names
HazAngles   = np.unique(AllData['Head_azimuth_start'])          # Get unique head azimuth angles
if IncludeVox == 1:
    ExpIndx  = np.append(ExpIndx, VoxIndx)
    ExpNames = np.append(ExpNames, VoxNames)
else:
    ExpIndx  = ExpIndx[0]
    ExpNames = np.asarray(ExpNames)
    
NoExp       = len(ExpNames)
NoHaz       = len(HazAngles)
TotalCond   = NoExp*NoHaz
ExpOrder    = np.random.permutation(TotalCond)
ExpFiles    = AllData['RGB_file'][ExpIndx[ExpOrder]]
ExpFrames   = AllData['Frames'][ExpIndx[ExpOrder]]
IsVox       = AllData['Category'][ExpIndx[ExpOrder]]=='Vox'
ExpOrder    = np.append(ExpOrder, ExpOrder[-1])
AllTurnIndx = np.where(AllData['Category']=='Turn') 

HeadTurnFiles   = np.empty([0, TotalCond], dtype="U60")
HeadTurnFrames  = np.empty([0, TotalCond])

#======= Interleave head rotation clips where necessary
for e in range(0, TotalCond):
    HazStart    = AllData['Head_azimuth_end'][ExpIndx[ExpOrder[e]]]
    HazEnd      = AllData['Head_azimuth_start'][ExpIndx[ExpOrder[e+1]]]
    if HazStart != HazEnd:      # If head angle chnages between expression clips...
        HeadTurnIndx = np.where((AllData['Head_azimuth_start']==HazStart) & (AllData['Head_azimuth_end']==HazEnd))
        HeadTurnFiles   = np.append(HeadTurnFiles, AllData['RGB_file'][HeadTurnIndx])  
        HeadTurnFrames  = np.append(HeadTurnFrames, AllData['Frames'][HeadTurnIndx])  
    elif HazStart == HazEnd:    # If consecutive expressions clips have same head angle...
        BlinkIndx = np.where((AllData['Action']=='Blink') & (AllData['Head_azimuth_start']==HazStart))
        HeadTurnFiles   = np.append(HeadTurnFiles, AllData['RGB_file'][BlinkIndx])
        HeadTurnFrames  = np.append(HeadTurnFrames, AllData['Frames'][BlinkIndx])
    
#======= Set output video parameters
S  = bpy.context.scene
S.render.image_settings.file_format     = 'FFMPEG'            # Set render format
S.render.ffmpeg.audio_codec             = 'MP3'                 
S.render.ffmpeg.format                  = 'MPEG4'
S.render.ffmpeg.codec                   = 'H264'
S.render.ffmpeg.constant_rate_factor    = 'PERC_LOSSLESS'
S.render.resolution_x                   = 3840
S.render.resolution_y                   = 2160
S.render.resolution_percentage          = 50
S.render.fps                            = 60
S.render.fps_base                       = 1.0

if not S.sequence_editor:                               # If sequence editor doesn't exist...
    SE = S.sequence_editor_create()                     # Create sequence editor
else:
    SE = bpy.context.scene.sequence_editor

#pdb.set_trace()

#============= Load clips into Video Sequence Editor
FrameStart = 1
for clip in range(0, TotalCond):
    
    #======== Insert next expression animation clip
    ClipFilename    = os.path.join(MF3D_dir, 'Animations', ExpFiles[clip])
    FrameStart      = np.sum(ExpFrames[0:clip]) + np.sum(HeadTurnFrames[0:clip])+1
    if (os.path.isfile(ClipFilename) == 0):                                  # If file doesn't exist...
        print('MF3D animation clip '+ExpFiles[clip]+ 'was not found in '+ os.path.join(MF3D_dir, 'Animations') + '!')
    else:
        print("Adding expression clip {:01d}/{:01d}: {:s}".format(clip, TotalCond, ExpFiles[clip]))
    Mov = SE.sequences.new_movie("Clip{:01d}".format(clip+1), ClipFilename, 2, FrameStart)
    if IsVox[clip]:
        SE.sequences.new_sound("Clip{:01d}".format(clip+1), ClipFilename, 3, FrameStart)
        
    if AddCaptions == 1:
        Mov.blend_type = 'ALPHA_UNDER'
        Txt = SE.sequences.new_effect("Text{:01d}".format(clip), 'TEXT', 1, FrameStart, FrameStart+ExpFrames[clip])
        Txt.text        = "{:s} ({:01d} deg)".format(AllData['Action'][ExpIndx[ExpOrder[clip]]], AllData['Head_azimuth_start'][ExpIndx[ExpOrder[clip]]])
        Txt.align_y     = 'BOTTOM'
        Txt.align_x     = 'LEFT'
        Txt.font_size   = 120
        Txt.location    = [0.05, 0.9]

    #======== Add foreground image
    if AddForegroundIm == 1:
        Frg = SE.sequences.new_image('Foreground', ForegroundIm, 1, FrameStart)                  
        SE.sequences_all["Foreground"].blend_type          = 'ALPHA_OVER'
        SE.sequences_all["Foreground"].frame_final_end     = FrameStart + ExpFrames[clip]
        
    #======== Insert next inter-trial clip 
    ClipFilename    = os.path.join(MF3D_dir, 'Animations', HeadTurnFiles[clip])
    FrameStart      = np.sum(ExpFrames[0:clip+1]) + np.sum(HeadTurnFrames[0:clip])+1
    if (os.path.isfile(ClipFilename) == 0):                                  # If file doesn't exist...
        print('MF3D animation clip '+HeadTurnFiles[clip]+ 'was not found in '+ os.path.join(MF3D_dir, 'Animations') + '!')
    else:
        print("Adding ITI clip {:01d}/{:01d}: {:s}".format(clip, TotalCond, HeadTurnFiles[clip]))
        
    SE.sequences.new_movie("ITI{:01d}".format(clip+1), ClipFilename, 2, FrameStart)
    
    #======== Add foreground image
    if AddForegroundIm == 1:
        Frg = SE.sequences.new_image('Foreground', ForegroundIm, 1, FrameStart)                  
        SE.sequences_all["Foreground"].blend_type          = 'ALPHA_OVER'
        SE.sequences_all["Foreground"].frame_final_end     = FrameStart + HeadTurnFrames[clip]

S.frame_end = np.sum(ExpFrames) + np.sum(HeadTurnFrames)

#======== Add background?
#Bkg     = SE.sequences.new_effect('Background', 'COLOR', 1, 1, len(FrameOrder)+1)       # Background
#SE.sequences_all["Foreground"].blend_type               = 'ALPHA_UNDER'
#SE.sequences_all["Background"].color = (BackgroundRGB);

#======== Render to movie file
#S.render.filepath   = os.path.join(OutputDir + MovieName[MovNo] + ".mp4")   # Set output filename
#S.frame_end         = len(FrameOrder)                                       # Set clip length (frames)
##if os.path.isfile(S.render.filepath) == 0:                                  # If file doesn't exist...
##    bpy.ops.render.render(animation = True)                                 # Render new movie
