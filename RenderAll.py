# -*- coding: utf-8 -*-
"""

"""

import bpy
import mathutils
import math
import numpy

BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
BlenderFile     = "BlenderFiles/Geocorrect_fur.blend"
RenderDir       = BlenderDir + "Renders"
Setup           = 1

#============ Set viewing geometry
if Setup == 1:							#============ For setup 3 with ASUS VG278H LCDs in mirror stereoscope
     ViewingDistance    = 78.0 						       # Set viewing distance (centimeters)
     MonitorSize        = [59.8, 33.5]  				       # Set physical screen dimensions (centimeters)
     Resolution         = [1920, 1080]				             # Set render resolution per eye (pixels)

elif Setup == 2:						#============ For setup 3 with LG 55EF9500 OLED 4K TV
	ViewingDistance    = 60.0                                      # Set viewing distance (centimeters)
	MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
	Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)

elif Setup == 3:						#============ For setup 1 with Ezio FlexScan LCD
	ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
	MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
	Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)

else:
	print("Unknown setup!")

FOV = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)               # Set camera horizontal field of view (radians)


#============ Set rendering variables						
ElAngles        = [-30, 0, 30]                                      # Set elevation angles (degrees)
AzAngles        = [-90, -45, 0, 45, 90]                             # Set azimuth angles (degrees)
Distances       = [-20, 0, 20]                                      # Set object distance from origin (centimeters)
NoConditions    = len(ElAngles)*len(AzAngles)*len(Distances)        # Calculate total number of conditions
msg             = "Total renders = %d" % NoConditions				
print(msg)

#============ Set scene settings
Scene                       = bpy.data.scenes['Scene']
Scene.unit_settings.system  = 'METRIC'
Scene.render.engine         = 'CYCLES'
Scene.render.resolution_x   = Resolution[0]
Scene.render.resolution_y   = Resolution[1]
Scene.render.use_stamp      = False							# Turn render stamps off
Scene.render.display_mode   = 'SCREEN'
Scene.render.views_format   = 'STEREO_3D'

bpy.data.objects["Camera"].location                     = mathutils.Vector((0, -ViewingDistance/100,0))
bpy.data.cameras["Camera"].stereo.interocular_distance  = 0.0035
bpy.data.cameras["Camera"].stereo.convergence_distance  = ViewingDistance/100
bpy.data.cameras["Camera"].stereo.convergence_mode      = 'OFFAXIS'
Scene.camera.data.type      = 'PERSP'
Scene.camera.data.angle     = FOV
head                        = bpy.data.objects["HeadGroup"]
head.rotation_mode          = 'XYZ'

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
for d in Distances:
    head.location = mathutils.Vector((0, d/100, 0))

    for el in ElAngles:
        ElevationAngle = math.radians(el)

        for az in AzAngles:
            AzimuthAngle = math.radians(az)
            head.rotation_euler = (ElevationAngle, 0, AzimuthAngle)

            Filename = "Macaque_neutral_az%d_el%d_dist%d.png" % (az, el, d)
            print("Now rendering" + Filename + "…\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)

print("Rendering complete!\n")
