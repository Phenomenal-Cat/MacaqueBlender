# -*- coding: utf-8 -*-
"""========================== RenderTranslations.py ===========================
This script renders a series of short animations in which a specified object 
translates in each of a specified number of directions.

Created on Thu Feb  2 22:36:44 2017
@author: aidanmurphy
"""
import numpy

#============ Initialize scene
SetupGeometry = 3
StereoFormat  = 1
InitBlendScene(SetupGeometry, StereoFormat)

RenderDir       = "/Volumes/Seagate Backup 1/Stimuli/Movies/MF3D/Translations/"

#============ Set motion parameters
ClipDurations           = 2                         # Clip duration (seconds)
ClipFPS                 = 60                        # frames per second
ClipDurationFrames      = ClipDurations*ClipFPS     # total frames per clip
TranslationSpeed        = 0.25                      # Speed (meters/second)
TranslationSpeedFrames  = TranslationSpeed/ClipFPS
TranslationAzimuths     = numpy.arange(0, 360, 45)
TranslationElevations   = numpy.arange(-90, 91, 45)

#============ Apply parameters to .blend file
Scene                   = bpy.data.scenes["Scene"]
Scene.frame_start       = 1
Scene.frame_end         = ClipDurationFrames
Scene.frame_step        = 1
Scene.render.fps        = ClipFPS


Root = bpy.data.objects['Root']


#============ Begin rendering loop
for Az in TranslationAzimuths:

    for El in TranslationElevations:

        Filename = "Macaque_Translation%d_az%d_el%d_exp%d.png" % (Az, El, Exp)
        print("Now rendering: " + Filename + " . . . (" + ClipDurationFrames + " frames)\n")
        bpy.context.scene.render.filepath = RenderDir + "/" + Filename
        bpy.ops.render.render(write_still=True, use_viewport=True)
                        
        for Frame in range(0, ClipDurationFrames):
            bpy.context.scene.frame_set(Frame)

            Distance = TranslationSpeedFrames*Frame                 # Calculate current distance from origin
            
            Root.location = mathutils.Vector((PosX, PosY, PosZ))    # Move root object

    


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
