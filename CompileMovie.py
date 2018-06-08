
#============================= CompileMovie.py ==================================
# This script loads rendered animation frame images from the specified directory 
# and assembles them in the desired sequence in teh video seqience editor for encoding
# as a movie file.

import bpy 
import os 
import sys 


Prefix          = '/Volumes/projects'
FrameDir        = Prefix + '/murphya/MacaqueFace3D/Macaque_video/RenderedFrames/BE_Coo_mov53/'
FrameList       = os.listdir(FrameDir)  # List all files in specified directory
FileType        = ".png"                # What file format are teh input images
FileSBS         = 1                     # Are input images side-by-side 3D renders?
FileSqueeze     = 0                     # Are input images squeezed SBS?

OutputFormat    = ".mp4"                # File format of movie
OutputFPS       = 30                    # Frame rate of movie (fps)
OutputRes       = [1920, 1080]          # Desired output resolution [X,Y] (pixels)


#======== Filter file list by valid file types.
candidates = []
c = 0
for item in FrameList:
    fileName, fileExtension = os.path.splitext(FrameList[c])
    if fileExtension == FileType:
        candidates.append(item)
    c = c + 1
    
    
#======== Load images to video sequence editor
file = [{"name":i} for i in candidates]   
n = len(file) 
print(n)   
a = bpy.ops.sequencer.image_strip_add(directory = FrameDir, files = file, channel=1, frame_start=0, frame_end=n-1) 

Scene = bpy.data.scenes["Scene"]
Frame = Scene.sequence_editor.sequences_all[]
    
if FileSBS == 1:                                        # If input format is side-by-side 3D...
    Frame.use_crop              = 1                     # Crop image
    Frame.crop.max_x            = ImageWidth/2          # Crop right half of image for 2D render
    Scene.render.resolution_x   = ImageWidth            # Set x resolution to full
    
elif :                                                  # Generate squeezed frame SBS
    Frame.use_crop              = 0                     # Do not crop image
    Scene.render.resolution_x   = ImageWidth/2          # 
    
#======== Load audio to video sequence editor
    


#======== Encode sequence to movie file
stripname=file[0].get("name"); 
bpy.data.scenes["Scene"].frame_end                          = n 
bpy.data.scenes["Scene"].render.image_settings.file_format  = 'AVI_JPEG' 
bpy.data.scenes["Scene"].render.filepath                    = FrameDir
#bpy.ops.render.render( animation=True ) 


