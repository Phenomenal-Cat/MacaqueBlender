
import bpy
import numpy as np


ObjectNames = ['Root','Root.001','Root.002']
FrameOffsets = [0, 100, 200, 300]

NoFrames        = 480
ScaleRange      = [200, 20]
PositionRange   = [250, -50]
ZPosRange       = [2, -4]
Scales          = np.linspace(ScaleRange[0], ScaleRange[1], NoFrames)
Positions       = np.linspace(PositionRange[0], PositionRange[1], NoFrames)
Zpositions      = np.linspace(ZPosRange[0], ZPosRange[1], NoFrames)

for f in range(0, NoFrames):
    bpy.context.scene.frame_set(f)
    
    for o in range(0, len(ObjectNames)):
        CurrentFrame = f+FrameOffsets[o]
        Obj = bpy.data.objects[ObjectNames[o]]
        Obj.scale = np.tile(Scales[CurrentFrame],[3,1])
        Obj.keyframe_insert(data_path="scale") 
        Obj.location = [0, Positions[CurrentFrame], Zpositions[CurrentFrame]]
        Obj.keyframe_insert(data_path="location") 
        