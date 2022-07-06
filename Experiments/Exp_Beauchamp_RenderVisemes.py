#======================= AnimateExpressionKeyframes.py ======================
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
# from GetOSpath import GetOSpath
from sys import platform
import numpy as np
# from InitBlendScene import InitBlendScene
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

def GazeLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    GazeXYZ = mu.Vector((X, Y, Z))
    return GazeXYZ    

#======================= LOAD FILE NAMES
def GetAllParamsFiles():
    RootDir     = '/Volumes/Seagate Backup 3/NIH_MF3D/MF3D_Collaborations/Beauchamp/'
    DataDir     = RootDir + 'Human_Videos/ExtractedParameters/'
    OutputDir   = RootDir + 'Macaque_Visemes/Renders/'

    ParamsFiles = []
    MovieFiles = []
    for v in range(0, len(Visemes)):
        MovieDir    = RootDir + 'Human_Videos/all_%s_stimuli/' % Visemes[v].lower()
        ParamsDir   = RootDir + 'Human_Videos/ExtractedParameters/%s_Edited/' % Visemes[v]
        ParamsRow = []
        MovieRow = []
        for a in Actors:
            ParamsRow.append(glob.glob(ParamsDir + "%s_*.%d_smoothed.csv" % (Visemes[v], a)))
            MovieRow.append(glob.glob(MovieDir + "*.%d.mp4" % a))
        ParamsFiles.append(ParamsRow)
        MovieFiles.append(MovieRow)

    return ParamsFiles, MovieFiles;

#======================= READ PARAMS DATA
def ReadParamsData(ParamsFile):
    with open(ParamsFile, "rt") as csvfile:
        reader = csv.reader(csvfile)    
        AllData = list(reader)
    csvfile.close()
    return AllData

#======================= ITERATE THROUGH CLIPS
Visemes         = ['Ba','Da','Ga']
Actors          = [1,2,3,4,5,6,7,8]
AddKeyframes    = 1
LoadOrigMovie   = 0                                         # Render original movie to a plane in the scene?
StereoFormat    = 0
#SetupGeometry   = 7  
#InitBlendScene(SetupGeometry, StereoFormat, 57)
# [DataDir, ParamsFiles, MovieDir, MovieFiles, OutputDir] = GetAllParamsFiles()
[ParamsFiles, MovieFiles] = GetAllParamsFiles()

# ParamsFile = ['Da_5.1_smoothed.csv'] 

    
HeadAzimuths    = [0] #[-20, 20, 0, 0, 0]
GazeAzimuths    = [0] #[0, 0, -20, 20, 0]
IsCoo           = 0
ConstrainBrow   = 0
frametotal      = 1

#============== For each viseme...
for v in range(0,1): #range(0, len(ParamsFiles )):
    
    #========== For each actor...
    for a in range(0, 1):
        print("Rendering " + ParamsFiles[v][a][0])
        AllData     = ReadParamsData(ParamsFiles[v][a][0])
        

        #============== Set parameters
        BoneNames       = ['blink',     'Kiss',     'jaw',  'ears',     'Fear',     'yawn',     'eyebrow',  'HeadTracker']      # Bone names
        BoneVectorIndx  = [2,           1,          2,      1,          1,          2,          2,          1]                  # Which channel (X,Y or Z) to apply values to
        BoneDirection   = [1,           1,          1,      1,         -1,         1,          -1,         -1]                 # Direction for each bone
        BoneWeight      = [0.007,       0.04,       0.02,   0.02,       0.02,       0.02,       0.02,       1]                  # Maximum values for each bone position
        BoneOffset      = [0,           0,          0,      0.02,       0,          0,          0,          0]                  
        
        
        if Visemes[v] == 'Ba':
            BoneWeight[2] = BoneWeight[2]*0.6
            
        elif Visemes[v] == 'Da':
             BoneWeight[2] = BoneWeight[2]*0.6
             BoneWeight[4] = BoneWeight[4]*0.3
             
        elif Visemes[v] == 'Ga':
             BoneWeight[2] = BoneWeight[2]*0.6
             BoneWeight[1] = BoneWeight[1]*0.4

        TongueProtrude    = 0
        if AllData[0][5] == 'lipsmack':
            BoneNames[4]      = 'LipSmack'
            BoneWeight[1]     = 0.022
            TongueLoc         = [0.0023, -0.005, -0.046]
            TongueStart       = np.array([0.002345, 0.018105, -0.04262])
            TongueDiff        = np.array([0, -0.0231, -0.0034])
            TongueRot         = 2
            TongueScale       = 0.02
            bpy.data.objects['TeethDown'].hide_render   = True
            bpy.data.objects['TeethUp'].hide_render     = True
            bpy.data.objects['Tongue_1'].hide_render    = False
            
        else:
            bpy.data.objects['TeethDown'].hide_render   = False
            bpy.data.objects['TeethUp'].hide_render     = False
            bpy.data.objects['Tongue_1'].hide_render    = False
            TongueLoc         = [0.0023, -0.005, -0.046]
            
        if AllData[0][5] == 'chew':
            BoneNames[4]      = 'Chew'
            JawOffset         = -0.0015
            JawHandle         = bpy.data.objects['TeethDown']
            JawLoc            = JawHandle.location

        #if IsCoo == 1:                          # If the expression being used is 'coo'
        #    BoneWeight[2] = 0                   # Turn off jaw movements
        #    print('Using kiss expression...')

        #if f.find("BarkGrowl")>0:               # For lip retraction during 'BarkGrowl'
        #    BoneWeight[4] = BoneWeight[4]/2     # Reduce weight of lip retraction by 50%
        #    print('Bark growl detected...')

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
        OutputFPS       = 60                                                # Specify desired output frame rate
        FrameRatio      = 2                                                 # Calculate ratio of input vs output frame rates

        head            = bpy.data.objects["HeaDRig"]                       # Get handle for macaque avatar head
        head2           = bpy.context.object

        #================== Set animation parameters
        scn                         = bpy.context.scene
        scn.frame_start             = 1         
        scn.frame_end               = (len(AllData)-1)*FrameRatio*len(HeadAzimuths)    # How many frames in animation?
        scn.render.frame_map_old    = 1         
        scn.render.frame_map_new    = 1         
        scn.render.fps              = OutputFPS                             # Set frames per second
        scn.render.use_placeholder  = True
        scn.render.use_overwrite    = 0

        #============== Add keyframes
        NoFrames    = (len(AllData)-1)
        
        
        for indx in range(0, len(HeadAzimuths)):
            
            #=============== Set head and eye gaze directions
            bpy.context.scene.frame_set(frametotal)
            HeadXYZ = HeadLookAt(0, HeadAzimuths[indx])
            head.pose.bones['HeadTracker'].location = HeadXYZ + head.location

            
            frame = 1
            #============== For each frame
            for n in AllData[1:]:
                #bpy.ops.anim.change_frame(frame = round((frame-1)*FrameRatio))                                         # Move timeline to correct output frame
                #bpy.context.scene.frame_set( round((frame-1)*FrameRatio) )                                              # Move timeline to correct output frame
                
                #SetFrameIndx = ((frame-1)*len(HeadAzimuths)*FrameRatio*NoFrames) + (indx*FrameRatio*NoFrames)+ 1+(frame-1)*FrameRatio
                SetFrameIndx = 1+(frame-1)*FrameRatio
                print('Frame index = %d' % SetFrameIndx)
                bpy.context.scene.frame_set(SetFrameIndx) 

                for exp in range(0, len(BoneNames)):   
                   
                    if AllData[frame][exp+1]=='NaN':
                        AllData[frame][exp+1] = 0                    
                             
                    if exp < 7:  #=============== For each bone...
                        
                        if (exp == 4) & (AllData[0][5] == 'lipsmack'):
                            #print('Data =' + AllData[frame][exp+1])
                            #AllData[frame][exp+1] = float(AllData[frame][exp+1])
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1expressionsSmackClosed"].value = float(AllData[frame][exp+1])                        # Set lip-smack shape key value 
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1expressionsSmackClosed"].keyframe_insert('value')
                            
                            if TongueProtrude == 1:
                                bpy.data.objects['Tongue_1'].location           = TongueStart + (TongueDiff*float(AllData[frame][2]))
                                bpy.data.objects['Tongue_1'].rotation_euler[0]  = math.radians(TongueRot*float(AllData[frame][2]))
                                bpy.data.objects['Tongue_1'].scale[2]           = 0.12 + (0.02*float(AllData[frame][2]))
                                bpy.data.objects['Tongue_1'].keyframe_insert('location')
                                bpy.data.objects['Tongue_1'].keyframe_insert('rotation_euler')
                                bpy.data.objects['Tongue_1'].keyframe_insert('scale')
                            
                        elif (exp == 4) & (AllData[0][5] == 'chew'):
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1expressionsChewing"].value = float(AllData[frame][exp+1])  # Set chew shape key value 
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1expressionsChewing"].keyframe_insert('value')
                            
                            JawHandle.location = ((float(AllData[frame][exp+1])*JawOffset, JawLoc[1], JawLoc[2]))
                            JawHandle.keyframe_insert('location')
                            
                        elif (exp == 4) & (Visemes[v] == 'Ba'):
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1viseme_B"].value = float(AllData[frame][exp+1])  # Set viseme shape key value 
                            bpy.data.shape_keys["Key.001"].key_blocks["MacaqueHeadNG_1viseme_B"].keyframe_insert('value')
                            
                        #elif (exp == 4) &  (Visemes[v] == 'Da'):   
                            
                        else :
                            
                            Vector                                          = mu.Vector((0,0,0))                                                                    # Initialize location vector
                            Vector[ BoneVectorIndx[exp] ]                   = BoneOffset[exp] + (BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1]))   # Set relevant vector component
                            head.pose.bones[ BoneNames[exp] ].location      = Vector                                                                                # Apply to bone location
                            head.pose.bones[ BoneNames[exp] ].keyframe_insert(data_path="location", index=-1)                                                       # Add keyframe
                        
                    elif exp == 7:  #============= Set head orientation
                        if len(AllData[frame]) < exp+1:
                            print('Error: params doesn''t include head elevation data!')
                        
                        hel     = BoneWeight[exp]*BoneDirection[exp]*float(AllData[frame][exp+1])   
                        HeadXYZ = HeadLookAt(hel, HeadAzimuths[indx])
                        head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
                        head.pose.bones['HeadTracker'].keyframe_insert(data_path="location")   
                                                                                                                         
                    #=============== Set gaze position
        #            BlinkProp = float(AllData[frame][1])
        #            if BlinkProp > 0.25:
        #                BlinkCorrect = -(0.16 + HeadXYZ[1] + head.location[1])
        #            else:
                    BlinkCorrect = 0
                    GazeXYZ = GazeLookAt(0, GazeAzimuths[indx])                     
                    GazeYpos    = 0.16 + HeadXYZ[1] + head.location[1] + BlinkCorrect
                    if (ConstrainBrow == 1) & (GazeYpos < 0.02):
                        GazeYpos = 0.02
                    #head.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, 0.12 + HeadXYZ[1] + head.location[1], 0))          
                    head.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, GazeYpos, 0))
                    head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1)     


                #======= Insert keyframe
                if AddKeyframes == 1:
                    print('Inserting keyframe %d of %d' % (frametotal, scn.frame_end ))
                    
                elif AddKeyframes == 0:
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    Filename = "%s_animation_Haz%d_%03d.png" % (DataFile, haz, frame)
                    if os.path.isfile(ExampleOutputDir + "/" + Filename) == 0:
                        print("Now rendering: " + Filename + " . . .\n")
                        bpy.context.scene.render.filepath = ExampleOutputDir + "/" + Filename
                        bpy.ops.render.render(write_still=True, use_viewport=True)
                    elif os.path.isfile(ExampleOutputDir + "/" + Filename) == 1:
                        print("File " + Filename + " already exists. Skipping . . .\n")

                #======= Next frame 
                frame += 1
                frametotal += 1 
            
            #====== Set final frame of sequence    
            # SetFrameIndx = ((indx*FrameRatio*NoFrames)+ 1+(frame-1)*FrameRatio)-1
            #SetFrameIndx = (f*len(HeadAzimuths)*FrameRatio*NoFrames) + (indx*FrameRatio*NoFrames)+ 1+(frame-1)*FrameRatio
            #bpy.context.scene.frame_set(frametotal) 
            head.pose.bones['HeadTracker'].location = HeadXYZ + head.location
            head.pose.bones['HeadTracker'].keyframe_insert(data_path="location")  
            head.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, 0.16 + HeadXYZ[1] + head.location[1] + BlinkCorrect, 0))
            head.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1)  
            

print("Rendering completed!\n")
