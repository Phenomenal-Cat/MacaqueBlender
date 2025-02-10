#==================== CameraMotionPaths.py =========================
# This script adds motion paths for each camera in the scene
# and adds keyframes for rendering of multiple camera motion trajectories


import bpy
import mathutils as mu
import math
import numpy as np
import socket
import os


CamNames        = ['AI48_001_Cam_01','AI48_001_Cam_02','AI48_001_Cam_03','AI48_001_Cam_04']
CamTargets      = ['AI48_001_Cam_01.Target','AI48_001_Cam_02.Target','AI48_001_Cam_03.Target','AI48_004_Cam_01.Target']
AllCams         = bpy.data.cameras

TestRender      = True                      # Set to True for faster but reduced quality renders (lower resolution and sampling)
Lenses          = ['Fisheye','Standard']    # 
StereoMode      = 0                         # Stereoscopic 3D options: 0 = 2D; 1 = 3D side-by-side; 2 = 3D color anaglyph

MotionTrajectories  = ['Follow','Slide','Elevate','Pan','Tilt','Roll']
MotionType          = ['translation','translation','translation','rotation','rotation','rotation']
MotionAxis          = ['z','x','y','y','x','z']
MotionMagnitude     = [1, 1, 1, 45, 45, 45]             # Magnitude of motion (distance in meters / angle in degrees)
MotionDuration      = [2, 2, 2, 2, 2, 2]                # Duration of motion (seconds)
MotionPathRot       = [[1,0,0],[0,1,0],[0,0,1]]         # Orientation of motion paths (XYZ)

#==== For each virtual camera...
for c in (0:len(CamNames)):                         
    cam     = AllCams[c]
    camObj  = bpy.data.objects[CamNames[c]]
    target  = bpy.data.objects[CamTargets[c]]
    scene   = bpy.data.scenes["Scene"]
    
    #==== Set stereoscopic 3D parameters
    if StereoMode == 0:
        scene.render.use_multiview = False
    elif StereoMode > 0
         scene.render.use_multiview = True
         scene.render.views_format  = 'STEREO_3D'
         scene.render.image_settings.views_format = 'INDIVIDUAL'
    
    #==== Set render quality (/ speed)
    if (TestRender == True):
        scene.render.resolution_percentage  = 25
        scene.cyles.samples                 = 20
    elif (TestRender == False):
        scene.render.resolution_percentage  = 100
        scene.cyles.samples                 = 200
    
    #==== Set lens type for virtual camera
    for l in (0:len(Lenses)):            # Set the lens type
        if Lenses[l] == 'Fisheye':       # 180° fish eye view
            cam.type            = 'PANO'
            cam.panorama_type   = 'FISHEYE_EQUISOLID' 
            cam.fisheye_lens    = 10.5
            cam.fisheye_fov     = np.radians(180)
            scene.render.resolution_x = 2160
            scene.render.resolution_y = 2160
            
        elif Lenses[l] == 'Standard':    # Perspective view
            cam.type            = 'PERS'
            cam.lens_unit       = 'FOV'
            cam.angle           = np.radians(90)
    
    #==== For each motion trajectory...
    for m in (0:len(MotionTrajectories)):
        
        
        if (MotionType[m] == 'translation'):
            path            = bpy.ops.curve.primitive_nurbs_path_add(radius= MotionMagnitude[m], enter_editmode=False, align='WORLD', location=camObj.location, rotation=MotionPathRot[m], scale=(1,1,1))
            path            = bpy.data.objects["Nurbs_path"]
            path.duration   = MotionDuration[m]*FPS
            path.eval_time  = 100
            bpy.ops.object.constraint_add(type='FOLLOW_PATH')       # Add 'follow path' constraint to camera object
            camObj.constraints['Follow Path'].target = path         # Set the nurbs path as the target path
            
        elif (MotionType[m] == 'rotation'):
            
            bpy.ops.object.constraint_add(type='FOLLOW_PATH')       # Add 'follow path' constraint to camera TARGET object
            target.constraints['Follow Path'].target = path