

import bpy
import mathutils
import math
import numpy
import socket

NFrames = 10;
GazeXYZ = [0, 0, 0];
GazeInc = [0.01, 0.01, 0];


# move to frame 0
bpy.context.scene.frame_current = 0;

bpy.ops.anim.change_frame(frame = 0)
bpy.data.objects["HeadRig"].pose.bones["EyesLookAt"].location = GazeXYZ

# move to frame 60
bpy.ops.anim.change_frame(frame = 60)
bpy.data.objects["HeadRig"].pose.bones["EyesLookAt"].location = GazeXYZ

    
    
    
    