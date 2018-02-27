# -*- coding: utf-8 -*-
"""============================ RenderAll.py ==================================

This script sets up the viewing geometry of the virtual scene in Blender appropriate
for the physical viewing geometry of the presentation setup. It then loops through
the stimulus variables, rednering stereoscopic pairs of images for each condition requested.

06/07/2016 - Written by APM (murphyap@mail.nih.gov)
"""

import bpy
import mathutils
import math
import numpy
import socket

if 'STIM_S4' or 'MH01918639MACDT' in socket.gethostname():
    BlenderDir      = "/Volumes/projects/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur.blend"
elif 'AidansMac' in socket.gethostname():
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderFile     = "BlenderFiles/Geocorrect_fur.blend"

RenderDir           = BlenderDir + "Renders"
SetupGeometry       = 1                                                 # Specify which physical setup stimuli will be presented in

#============ Set viewing geometry
if SetupGeometry == 1:                          #============ For setup 3 with ASUS VG278H LCDs in a mirror stereoscope
     ViewingDistance    = 78.0 						       # Set viewing distance (centimeters)
     MonitorSize        = [59.8, 33.5]  				       # Set physical screen dimensions (centimeters)
     Resolution         = [1920, 1080]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 2:                        #============ For setup 3 with LG 55EF9500 OLED 4K TV
	ViewingDistance    = 60.0                                      # Set viewing distance (centimeters)
	MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
	Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 3:                        #============ For setup 1 with Ezio FlexScan LCD
	ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
	MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
	Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)

else:
	print("Unknown setup!")

FOV                     = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)        # Set camera horizontal field of view (radians)

#============ Set rendering variables						
#ElAngles        = [-30, 0, 30]                                                  # Set elevation angles (degrees)
#AzAngles        = [-90, -60, -30, 0, 30, 60, 90]                                #  Set azimuth angles (degrees)
#Distances       = [-20, 0, 20] 						                           # Set object distance from origin (centimeters)
#Scales          = [0.1, 0.12, 0.2]
ElAngles        = [0]                                                  # Set elevation angles (degrees)
AzAngles        = [0]                                #  Set azimuth angles (degrees)
Distances       = [0] 						                           # Set object distance from origin (centimeters)
Scales          = [0.12]

ExpressionStr   = ["neutral","Fear","lipsmack","Threat"]
ExpressionNo    = [0, 1, 2, 3]
NoConditions    = len(ElAngles)*len(AzAngles)*len(Distances)*len(Scales)        # Calculate total number of conditions
msg             = "Total renders = %d" % NoConditions				
print(msg)

#============ Set scene settings
Scene                           = bpy.data.scenes['Scene']
Scene.unit_settings.system      = 'METRIC'
Scene.render.engine             = 'CYCLES'
Scene.render.resolution_x       = Resolution[0]
Scene.render.resolution_y       = Resolution[1]
Scene.render.use_stamp          = False							# Turn render stamps off
Scene.render.display_mode       = 'SCREEN'
Scene.render.views_format       = 'STEREO_3D'
Scene.cycles.film_transparent   = True


Cam                             = bpy.data.objects["Camera"]
Cam.location                    = mathutils.Vector((0, -ViewingDistance/100,0))
Cam2                            = bpy.data.cameras["Camera"]
Cam2.stereo.interocular_distance  = 0.0035
Cam2.stereo.convergence_distance  = ViewingDistance/100
Cam2.stereo.convergence_mode      = 'OFFAXIS'

Scene.camera.data.type          = 'PERSP'
Scene.camera.data.angle         = FOV
Scene.camera.data.ortho_scale   = MonitorSize[0]/100
head                            = bpy.data.objects["HeadGroup"]
head.rotation_mode              = 'XYZ'

#============ Set path tracing
bpy.context.scene.cycles.progressive                = 'PATH'
bpy.context.scene.cycles.samples                    = 50
bpy.context.scene.cycles.use_square_samples         = False
bpy.context.scene.cycles.max_bounces                = 128
bpy.context.scene.cycles.min_bounces                = 3
bpy.context.scene.cycles.glossy_bounces             = 128
bpy.context.scene.cycles.transmission_bounces       = 128
bpy.context.scene.cycles.volume_bounces             = 128
bpy.context.scene.cycles.transparent_max_bounces    = 1
bpy.context.scene.cycles.transparent_min_bounces    = 1
bpy.context.scene.cycles.use_progressive_refine     = True
bpy.context.scene.render.tile_x                     = 64
bpy.context.scene.render.tile_y                     = 64



#============ Begin rendering loop
for exp in ExpressionNo:
    if ExpressionStr[exp].find("neutral")==0:
        for i in [1,2,3]:
            bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[i]].mute = True
    elif ExpressionStr[exp].find("neutral")==-1:
        for i in [1,2,3]:
            bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[i]].mute = True
        bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[exp]].mute  = False

    for s in Scales:
        head.scale = mathutils.Vector((s, s, s))
        
        for d in Distances:
            head.location = mathutils.Vector((0, d/100, 0))

            for el in ElAngles:
                ElevationAngle = math.radians(el)

                for az in AzAngles:
                    AzimuthAngle = math.radians(az)
                    head.rotation_euler = (ElevationAngle, 0, AzimuthAngle)

                    Filename = "Macaque_Id3_%s_az%d_el%d_dist%d_sc%d.png" % (ExpressionStr[exp], az, el, d, s*100)
                    print("Now rendering: " + Filename + " . . .\n")
                    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                    bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering completed!\n")