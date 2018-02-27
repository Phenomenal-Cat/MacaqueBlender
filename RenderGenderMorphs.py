# -*- coding: utf-8-

import bpy
import mathutils as mu
import math
import numpy as np
import socket
import sys

if socket.gethostname().find("STIM_S4")==0:
    BlenderDir      = "P:/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur3.blend"
elif socket.gethostname().find("MH01918639MACDT")==0 :
    BlenderDir      = "/Volumes/projects/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur.blend"
elif socket.gethostname().find("DESKTOP-5PBDLG6")==0 :
    # BlenderDir      = "P:/khandhadiaap/Blender/"
    BlenderDir      = "P:/leathersml/"
elif socket.gethostname().find("Aidans-Mac")==0:
    #BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/BlenderFiles/"
    BlenderFile     = "BlenderFiles/NGmacaqueHead09.blen.blend"
elif socket.gethostname().find("SCNI-Red-DataPixx")==0:
    BlenderDir      = "/projects/khandhadiaap/Blender/"
elif socket.gethostname().find("MH01971918MACDT")==0:
    BlenderDir      = "/Volumes/PROJECTS/khandhadiaap/Blender"
elif socket.gethostname().find('MH02086178MACLT')==0:       # Aidan's NIH MacBook Pro
    BlenderDir      = "/Volumes/PROJECTS/murphya/Stimuli/MeshMorphing/"
    
sys.path.append(BlenderDir)
#import InitBlendScene_Special
#SetupGeometry       = 3                         # Specify which physical setup stimuli will be presented in
#StereoFormat        = 0
#InitBlendScene_Special.InitBlendScene(SetupGeometry, StereoFormat )
RenderDir           = BlenderDir + "GenderMorphs/"


#============ Set rendering parameters                        
HeadElAngles    = [0]                                              # Set elevation angles (degrees)
HeadAzAngles    = [0, 30]                                                 # Set azimuth angles (degrees)
GenderPerc      = [-400, -300, -200, -100, -50, 0, 50, 100, 200, 300, 400]   # Set gender levels in % masculinity
GenderProp      = [x/200 for x in GenderPerc]                                # Set gender levels in proportion Shape Key

#Distances       = [-20, 0, 20]                                                   # Set object distance from origin (centimeters)
NoConditions        = (len(HeadElAngles)+len(HeadAzAngles))*len(GenderPerc )   #*len(Scales)        # Calculate total number of conditions                   
    
AverageMonkey = bpy.data.objects["GenderNeutral"]
MaleShape     = AverageMonkey.data.shape_keys.key_blocks["Male_200%"]
Initial_Rot   = AverageMonkey.rotation_euler
#bpy.ops.object.mode_set(mode='POSE')
bpy.context.scene.render.image_settings.file_format = 'PNG' 

#========================== Begin rendering loop
for Mlevel in GenderProp:
    MaleShape.value = Mlevel

    for Hel in HeadElAngles:
        for Haz in HeadAzAngles:
            AverageMonkey.rotation_euler=(Initial_Rot[0]+math.radians(Hel),Initial_Rot[1],Initial_Rot[2]+math.radians(Haz))
            
            #============ Update render and save
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            Filename = "MacaqueMorph_Masculinity%d%%_Haz%d" % (round(Mlevel*200), Haz)
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)

                                
print("Rendering completed!\n")




