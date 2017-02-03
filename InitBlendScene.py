# -*- coding: utf-8 -*-
"""============================= InitBlendScene.py ============================
This script is used to set up scene geometry appropriate for the intended viewing
environment in which 
Created on Thu Feb  2 22:22:56 2017

@author: aidanmurphy (murphyap@mail.nih.gov)
"""

import bpy
import mathutils
import math
import numpy


#============ Set viewing geometry
if SetupGeometry == 1:                          #============ For setup 3 with ASUS VG278H LCDs in a mirror stereoscope
    ViewingDistance    = 78.0 						      # Set viewing distance (centimeters)
    MonitorSize        = [59.8, 33.5]  				      # Set physical screen dimensions (centimeters)
    Resolution         = [1920, 1080]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 2:                        #============ For setup 3 with LG 55EF9500 OLED 4K TV
    ViewingDistance    = 60.0                                      # Set viewing distance (centimeters)
    BezelSize          = 0.8*2;                                    # Total monitor bezel (centimeters)
    MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
    MonitorSize        = MonitorSize -[BezelSize, BezelSize]       # Adjust for bezel
    Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)

elif SetupGeometry == 3:                        #============ For setup 1 with Ezio FlexScan LCD
    ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
    MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
    Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)
 
elif SetupGeometry == 4:                       #============ For Epson projectors in NIF 4.7T vertical MRI scanner
    ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
    MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
    Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels

else:
	print("Unknown setup!")

FOV                     = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)        # Set camera horizontal field of view (radians)


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

#============ Set camera settings
Cam                             = bpy.data.objects["Camera"]
Cam.location                    = mathutils.Vector((0, -ViewingDistance/100,0))
Cam2                            = bpy.data.cameras["Camera"]
Cam2.stereo.interocular_distance  = 0.0035
Cam2.stereo.convergence_distance  = ViewingDistance/100
Cam2.stereo.convergence_mode    = 'OFFAXIS'
Scene.camera.data.type          = 'PERSP'
Scene.camera.data.angle         = FOV
Scene.camera.data.ortho_scale   = MonitorSize[0]/100

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