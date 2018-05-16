# -*- coding: utf-8-

import bpy
import mathutils as mu
import math
import numpy as np
import socket
import sys
import InitBlendScene

if socket.gethostname().find("MH01918639MACDT")==0 :
    BlenderDir      = "/Volumes/procdata/murphya/Stimuli/MacaqueAvatar/"
    BlenderFile     = "Geocorrect_fur.blend"
elif socket.gethostname().find("DESKTOP-5PBDLG6")==0 :
    # BlenderDir      = "P:/khandhadiaap/Blender/"
    BlenderDir      = "P:/leathersml/"
elif socket.gethostname().find("Aidans-Mac")==0:
    #BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/BlenderFiles/"
    BlenderFile     = "BlenderFiles/NGmacaqueHead09.blen.blend"

    
#sys.path.append(BlenderDir)
SetupGeometry       = 3                                                 # Specify which physical setup stimuli will be presented in
StereoFormat        = 0                                                 # Specify the stereoscopic format to render
InitBlend(SetupGeometry, StereoFormat)                                  # Initialize the Blender scene to meet requirements
if SetupGeometry == 3:
    BlenderDir = BlenderDir + "OLED_Renders"                            
    
RenderDir           = BlenderDir + "PCA_Statues_18"


#============ Set rendering parameters                        
StartingRotation=(0,0,0)
HeadElAngles    = [-30, 0, 30]                                          # Set elevation angles (degrees)
HeadAzAngles    = [-30, 30]                                             # Set azimuth angles (degrees)
NoPCs           = 5                                                     # How many PCs to use
Value1inSDs     = 3                                                     # How many SDs does shape key value '1' equal?
PCA_SDs         = [-3, -2, -1, 0, 1, 2, 3]                              # Set PCA Standard Deviations   
PCA_Vals        = PCA_SDs/Value1inSDs                                   # Convert SDs to corresponding shape key values
#Distances       = [-20, 0, 20]                                         # Set object distance from origin (centimeters)
NoConditions    = (len(HeadElAngles)+len(HeadAzAngles))*len(PCA_SDs)^NoPCs #*len(Scales)        # Calculate total number of conditions                   
    
HeadMesh   = bpy.data.objects["AverageMesh2"]
HeadMesh.rotation_euler = StartingRotation
for pc in NoPCs:
    PC(pc) = HeadMesh.data.shape_keys.key_blocks["PC%d_SD3" % pc]

#bpy.ops.object.mode_set(mode='POSE')

bpy.context.scene.render.image_settings.file_format = 'PNG'


#========================== Begin rendering loop
for SD1 in PCA_SDs:
    for SD2 in PCA_SDs:
        for SD3 in PCA_SDs:
            for SD4 in PCA_SDs:
                
                PC(pc)

                for Hel in HeadElAngles:
                    #=========== Rotate Elevation
                    Initial_Rot=HeadMesh.rotation_euler
                    HeadMesh.rotation_euler=(Initial_Rot[0]-math.radians(Hel),Initial_Rot[1],Initial_Rot[2])
                                    
                    #============ Update render and save
                    Haz = 0
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    Filename = "PCA18_SDs%d_%d_%d_%d_%d_Az%d_E%d" % (round(SD1),round(SD2), round(SD3),round(SD4), round(SD5), Haz, Hel)
                    print("Now rendering: " + Filename + " . . .\n")
                    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                    bpy.ops.render.render(write_still=True, use_viewport=True)
                    HeadMesh.rotation_euler = StartingRotation
                    
                for Haz in HeadAzAngles:
                    #=========== Rotate Azimuth
                    Initial_Rot=HeadMesh.rotation_euler
                    HeadMesh.rotation_euler=(Initial_Rot[0],Initial_Rot[1]+math.radians(Haz),Initial_Rot[2])
                    
                    #============ Update render and save
                    Hel = 0
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)    
                    Filename = "PCA18_SDs%d_%d_%d_%d_%d_Az%d_E%d" % (round(SD1),round(SD2), round(SD3),round(SD4), round(SD5), Haz, Hel)
                    print("Now rendering: " + Filename + " . . .\n")
                    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                    bpy.ops.render.render(write_still=True, use_viewport=True)
                    HeadMesh.rotation_euler = StartingRotation
                 
                                    
print("Rendering completed!\n")




