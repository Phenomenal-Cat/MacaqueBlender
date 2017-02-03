# -*- coding: utf-8 -*-
"""============================ RenderAnimation.py ==================================

This script 

21/07/2016 - Written by APM (murphyap@mail.nih.gov)
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
elif socket.gethostname().find("AidansMac")==0:
    BlenderDir      = "/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/"
    BlenderFile     = "BlenderFiles/Geocorrect_fur.blend"



#================== Set animation parameters
scn                         = bpy.context.scene
scn.frame_start             = 1         
scn.frame_end               = 120       # How many frames in animation?
scn.render.frame_map_old    = 1         
scn.render.frame_map_new    = 1         
scn.render.fps              = 30        # Set frames per second


cf          = scn.frame_current
keyInterp   = context.user_preferences.edit.keyframe_new_interpolation_type
context.user_preferences.edit.keyframe_new_interpolation_type ='LINEAR'


temp_ob.keyframe_insert(data_path='location', frame=(cf))
temp_ob.keyframe_insert(data_path='rotation_euler', frame=(cf))

context.user_preferences.edit.keyframe_new_interpolation_type = keyInterp
