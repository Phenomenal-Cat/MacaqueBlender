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


def InitBlendScene(SetupGeometry=2, StereoFormat=1, ViewingDistance=100):
 
    #============ Set viewing geometry
    HemiProjection          = 0
    SqueezeFrame            = 0
    AddPDmarker             = 0
    if SetupGeometry == 1:                          #============ For SCNI setup 3 with ASUS VG278H LCDs in a mirror stereoscope
        if not ViewingDistance:
            ViewingDistance    = 78.0 						           # Set viewing distance (centimeters)bpy.data.
        MonitorSize        = [59.8, 33.5]  				               # Set physical screen dimensions (centimeters)
        Resolution         = [1920, 1080]                              # Set render resolution per eye (pixels)
    
    elif SetupGeometry == 2:                        #============ For SCNI neurophys rigs with LG 55" OLED 4K TV
        if not ViewingDistance:
            ViewingDistance    = 90.0                                  # Set viewing distance (centimeters)
        BezelSize          = 0.8*2;                                    # Total monitor bezel (centimeters)
        MonitorSize        = [122.6, 71.8]                             # Set physical screen dimensions (centimeters)
        MonitorSize        = numpy.subtract(MonitorSize, [BezelSize, BezelSize])       # Adjust for bezel
        Resolution         = [3840, 2160]                              # Set render resolution per eye (pixels)
        SqueezeFrame       = 1                                         # Horizontal squeee for SBS
    
    elif SetupGeometry == 3:                        #============ For SCNI setup 2 with Ezio FlexScan LCD
        if not ViewingDistance:
            ViewingDistance    = 40.0                                  # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1280, 1024]                              # Set render resolution per eye (pixels)
     
    elif SetupGeometry == 4:                        #============ For Epson projectors in NIF 4.7T vertical MRI scanner
        if not ViewingDistance:
            ViewingDistance    = 48.0                                  # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1920, 1200]                              # Set render resolution per eye (pixels)
        
    elif SetupGeometry == 5:                        #============ For SCNI hemispheric dome projection screen
        HemiProjection     = 1
        if not ViewingDistance:
            ViewingDistance    = 100.0                                 # Set viewing distance (centimeters)
        MonitorSize        = [34.0, 27.2]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1080, 1080]                              # Set render resolution per eye (pixels)
        
    elif SetupGeometry == 6:                        #============ For Romanski lab use (2D image can be scaled post-hoc)
        if not ViewingDistance:
            ViewingDistance    = 50.0                                  # Set viewing distance (centimeters)
        MonitorSize        = [22.0, 22.0]                              # Set physical screen dimensions (centimeters)
        Resolution         = [1080, 1080]                              # Set render resolution per eye (pixels)
        StereoFormat       = 0
        
    elif SetupGeometry == 7:                        #============ For Murphy & Leopold 2019 stimulus set #1
        ViewingDistance     = 57.0  
        MonitorSize         = [60, 34]
        Resolution          = [3840, 2160]
        SqueezeFrame        = 0    
        
    elif SetupGeometry == 8:                        #============ For Kastner lab 65" LG 65E6
        MonitorSize        = [146.0, 88.0]                              # Set physical screen dimensions (centimeters)
        Resolution         = [3840, 2160]                               # Set render resolution per eye (pixels)
        SqueezeFrame       = 1                                          # Horizontal squeee for SBS
           
    else:
    	print("Unknown setup!")
    
    
    
    #============ Add photodiode marker to scene
    if AddPDmarker == 1:
        MonitorCenter           = numpy.divide(MonitorSize,2)                       # Caclulate physical screen center
        PhotodiodeRadius        = 0.01                                              # Set radius of photodiode marker (meters)
        PhotodiodeOnColor       = [1, 1, 1]                                         # RGB value for photodiode 'on'
        PhotodiodeOffColor      = [0, 0, 0]                                         # RGB value for photodiode 'off'
        PhotodiodeLocation      = ((-MonitorCenter[0]/100 + PhotodiodeRadius, -MonitorCenter[1]/100 +2*PhotodiodeRadius, 0))    # Cacluclate screen position of photodiode (bottom left corner in meters)
        bpy.ops.mesh.primitive_circle_add(                                          # Add marker disk to scene                                  
            vertices    = 100,
            radius      = PhotodiodeRadius, 
            fill_type   = 'TRIFAN',
            view_align  = True,
            location    = (PhotodiodeLocation[0], PhotodiodeLocation[2], PhotodiodeLocation[1]),
            rotation    = (math.radians(90),0,0))
        bpy.data.objects['Circle'].name = 'PDmarker'                                # rename photodiode marker object
        
    
    #============ Set scene settings
    Scene                                       = bpy.data.scenes[0]
    Scene.unit_settings.system                  = 'METRIC'
    Scene.render.engine                         = 'CYCLES'
    Scene.render.resolution_x                   = Resolution[0]
    Scene.render.resolution_y                   = Resolution[1]
    Scene.render.resolution_percentage          = 100
    Scene.render.use_stamp                      = False							# Turn render stamps off
    Scene.render.display_mode                   = 'SCREEN'
    Scene.render.image_settings.color_depth     = '8'                           # Set color bit-depth (8 or 16 for PNG)
    Scene.render.use_placeholder                = True                          
    Scene.cycles.film_transparent               = True
    
    #============ Set stereoscopic 3D settings
    StereoSet                                           = bpy.context.scene.render.image_settings
    if StereoFormat == 0:                                                   #=========== 2D rendering
        Scene.render.use_multiview                      = False
        #Scene.render.views_format                       = 'INDIVIDUAL'
        #StereoSet.views_format                          = 'INDIVIDUAL' 
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
    Cam2.stereo.interocular_distance                    = 0.035                         # Set for average Rhesus macaque IPD (meters)
    Cam2.stereo.convergence_distance                    = ViewingDistance/100           # Cameras converge at screen distance from viewer
    Cam2.stereo.convergence_mode                        = 'OFFAXIS'                     # Off-axis frusta are required for physically correct renders
    
    
    #============ Set camera settings
    FOV                                                 = 2*math.atan((MonitorSize[0]/2)/ViewingDistance)       # Set camera horizontal field of view (radians)
    print(math.degrees(FOV))
    Cam                                                 = bpy.data.objects["Camera"]
    Cam.location                                        = mathutils.Vector((0, -ViewingDistance/100,0))
    Cam.data.lens_unit                                  = 'FOV'
    Cam.data.angle                                      = FOV
    #Cam.data.sensor_width                               = Cam.data.lens
    Cam.data.ortho_scale                                = MonitorSize[0]/100
    Cam.data.type                                       = 'PERSP'    
    if HemiProjection ==1:                
        Cam.data.lens                                   = 5
        Scene.camera.data.type                          = 'PANO'
        Scene.camera.data.cycles.panorama_type          = 'FISHEYE_EQUIDISTANT'  
        Scene.render.resolution_x                       = Resolution[1]
        Scene.render.resolution_y                       = Resolution[1]
        
    
    #============ Set path tracing
    bpy.context.scene.cycles.progressive                = 'PATH'
    bpy.context.scene.cycles.samples                    = 200
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

    return AddPDmarker

InitBlendScene()
