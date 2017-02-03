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

if socket.gethostname().find("STIM_S4")==0:
    BlenderDir      = "P:/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur3.blend"
elif socket.gethostname().find("MH01918639MACDT")==0 :
    BlenderDir      = "/Volumes/projects/murphya/MacaqueFace3D/BlenderFiles/"
    BlenderFile     = "Geocorrect_fur.blend"
elif socket.gethostname().find("Aidans-Mac")==0:
    #BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/BlenderFiles/"
    BlenderFile     = "BlenderFiles/Geocorrect_fur.blend"

MonkeyID            = 3
RenderDir           = BlenderDir + "Renders/Monkey_%d" % (MonkeyID)
SetupGeometry       = 2                                         # Specify which physical setup stimuli will be presented in

#============ Set viewing geometry
if SetupGeometry == 1:                          #============ For setup 3 with ASUS VG278H LCDs in a mirror stereoscope
     ViewingDistance    = 78.0 						               # Set viewing distance (centimeters)
     MonitorSize        = [59.8, 33.5]  				            # Set physical screen dimensions (centimeters)
     Resolution         = [1920, 1080]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 2:                        #============ For setup 3 with LG 55EF9500 OLED 4K TV
	ViewingDistance    = 60.0                                      # Set viewing distance (centimeters)
    BezelSize          = 0.8*2;
	MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
    MonitorSize        = MonitorSize -[BezelSize, BezelSize]       # Adjust for bezel
	Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 3:                        #============ For setup 1 with Ezio FlexScan LCD
	ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
	MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
	Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)

else:
	print("Unknown setup!")

FOV                     = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)        # Set camera horizontal field of view (radians)

#============ Set rendering parameters						
ElAngles        = [-30, 0, 30]                                                  # Set elevation angles (degrees)
#AzAngles        = [-90, -60, -30, 0, 30, 60, 90]                                #  Set azimuth angles (degrees)
Distances       = [-20, 0, 20] 						                           # Set object distance from origin (centimeters)
#Scales          = [0.1, 0.12, 0.2]
#ElAngles        = [0]                                                  # Set elevation angles (degrees)
AzAngles        = [-30, 0, 30]                                #  Set azimuth angles (degrees)
#Distances       = [0] 						                           # Set object distance from origin (centimeters)
Scales          = [0.12]
#FurLengths      = [0.4]
FurLengths      = [0.7]
ExpressionStr   = ["neutral","Fear","lipsmack","Threat"]
#ExpressionNo    = [0, 1, 2, 3]
ExpressionNo    = [0]
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
for fl in FurLengths:
    bpy.data.particles["fur base.test.001"].path_end = fl

    for exp in ExpressionNo:
        if ExpressionStr[exp].find("neutral")==0:       # For 'neutral' expression, mute shape keys
            for i in [1,2,3]:
                bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[i]].mute = True
                
        elif ExpressionStr[exp].find("neutral")==-1:    # For all other expressions, unmute relevant shape key
            for i in [1,2,3]:
                bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[i]].mute = True
        
            bpy.data.shape_keys["Key.001"].key_blocks[ExpressionStr[exp]].mute  = False
            bpy.data.shape_keys["Key.001"].key_blocks["Threat"].value = 1
            
        if ExpressionStr[exp].find("Threat")==0:        # For 'threat' expression, rotate lower jaw
            bpy.data.objects['Teeth lower'].rotation_euler = (math.radians(24), 0, 0)
        else:
            bpy.data.objects['Teeth lower'].rotation_euler = (0, 0, 0)

        for s in Scales:
            head.scale = mathutils.Vector((s, s, s))
            
            for d in Distances:
                head.location = mathutils.Vector((0, d/100, 0))

                for el in ElAngles:
                    ElevationAngle = math.radians(el)

                    for az in AzAngles:
                        AzimuthAngle = math.radians(az)
                        head.rotation_euler = (ElevationAngle, 0, AzimuthAngle)

                        Filename = "Macaque_Id%d_fur%d_%s_az%d_el%d_dist%d_sc%d.png" % (MonkeyID, fl*100, ExpressionStr[exp], az, el, d, s*100)
                        print("Now rendering: " + Filename + " . . .\n")
                        bpy.context.scene.render.filepath = RenderDir + "/" + Filename
                        bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering completed!\n")