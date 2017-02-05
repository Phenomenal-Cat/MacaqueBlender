# -*- coding: utf-8 -*-
"""============================= InitBlendScene.py ============================
This function is used to initialize scene geometry appropriate for the intended 
viewing environment in which the to-be-rendered content will be presented. This
is especially critical for stereoscopic 3D renders.

Created on Thu Feb  2 22:22:56 2017
@author: aidanmurphy (murphyap@mail.nih.gov)
"""
import bpy
import mathutils
import math
import numpy


def InitBlendScene(SetupGeometry=2, StereoFormat=1):
 
    #============ Set viewing geometry
    HemiProjection          = 0
    SqueezeFrame            = 0
    if SetupGeometry == 1:                          #============ For SCNI setup 3 with ASUS VG278H LCDs in a mirror stereoscope
        ViewingDistance    = 78.0 						            # Set viewing distance (centimeters)
        MonitorSize        = [59.8, 33.5]  				             # Set physical screen dimensions (centimeters)
        Resolution         = [1920, 1080]                              # Set render resolution per eye (pixels)
    
    elif SetupGeometry == 2:                        #============ For SCNI setup 3 with LG 55EF9500 OLED 4K TV
        ViewingDistance    = 60.0                                      # Set viewing distance (centimeters)
        BezelSize          = 0.8*2;                                    # Total monitor bezel (centimeters)
        MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
        MonitorSize        = numpy.subtract(MonitorSize, [BezelSize, BezelSize])       # Adjust for bezel
        Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)
        SqueezeFrame       = 1                                         # Horizontal squeee for SBS
    
    elif SetupGeometry == 3:                        #============ For SCNI setup 1 with Ezio FlexScan LCD
        ViewingDistance    = 40.0                                      # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)
     
    elif SetupGeometry == 4:                        #============ For Epson projectors in NIF 4.7T vertical MRI scanner
        ViewingDistance    = 48.0                                      # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1920, 1200]                              # Set render resolution per eye (pixels)
        
    elif SetupGeometry == 5:                        #============ For SCNI hemispheric dome projection screen
        HemiProjection     = 1
        ViewingDistance    = 100.0                                     # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1920, 1920]                              # Set render resolution per eye (pixels
    
    else:
    	print("Unknown setup!")
    
    FOV                     = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)        # Set camera horizontal field of view (radians)
    
    #============ Set scene settings
    Scene                           = bpy.data.scenes['Scene']
    Scene.unit_settings.system      = 'METRIC'
    Scene.render.engine             = 'CYCLES'
    Scene.render.resolution_x       = Resolution[0]
    Scene.render.resolution_y       = Resolution[1]
    Scene.render.resolution_percentage = 100
    Scene.render.use_stamp          = False							# Turn render stamps off
    Scene.render.display_mode       = 'SCREEN'
    Scene.cycles.film_transparent   = True
    
    #============ Set stereoscopic 3D settings
    StereoSet                                           = bpy.context.scene.render.image_settings
    if StereoFormat == 0:                                                   #=========== 2D rendering
        Scene.render.use_multiview                      = False
        Scene.render.views_format                       = 'INDIVIDUAL'
        StereoSet.views_format                          = 'INDIVIDUAL' 
    elif StereoFormat == 1:                                                 #=========== Side-by-side stereo rendering
        Scene.render.use_multiview                      = True
        Scene.render.views_format                       = 'STEREO_3D'
        StereoSet.views_format                          = 'STEREO_3D'   
        StereoSet.stereo_3d_format.display_mode         = 'SIDEBYSIDE'
        StereoSet.stereo_3d_format.use_sidebyside_crosseyed = False                     # Do not switch eyes
        if SqueezeFrame == 1:
            StereoSet.stereo_3d_format.use_squeezed_frame       = True                  # 
            
    elif StereoFormat == 2:                                                 #=========== Anaglyph rendering
        StereoSet.stereo_3d_format.display_mode         = 'ANAGLYPH'
        StereoSet.stereo_3d_format.anaglyph_type        = 'RED_CYAN'    
        
                
    Cam2                                                = bpy.data.cameras["Camera"]
    Cam2.stereo.interocular_distance                    = 0.0035                        # Set for average Rhesus macaque IPD (meters)
    Cam2.stereo.convergence_distance                    = ViewingDistance/100           # Cameras converge at screen distance from viewer
    Cam2.stereo.convergence_mode                        = 'OFFAXIS'                     # Off-axis frusta are required for physically correct renders
    
    
    #============ Set camera settings
    Cam                                                 = bpy.data.objects["Camera"]
    Cam.location                                        = mathutils.Vector((0, -ViewingDistance/100,0))
    Scene.camera.data.angle                             = FOV
    Scene.camera.data.ortho_scale                       = MonitorSize[0]/100
    Scene.camera.data.type                              = 'PERSP'    
    if HemiProjection ==1:                
        Scene.camera.data.type                          = 'PANO'
        Scene.camera.data.cycles.panorama_type          = 'FISHEYE_EQUISOLID'  
        
    
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


InitBlendScene()
