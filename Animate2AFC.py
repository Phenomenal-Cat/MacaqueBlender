
# Animate2AFC.py

import os


Prefix          = '/Volumes/projects' 
TargetObject    = Prefix + '/murphya/MacaqueFace3D/GameRenders/Golf_Ball.obj'

Import          = bpy.ops.import_scene.obj(filepath=TargetObject)
Target          = bpy.context.selected_objects[0]


Target.scale        = ((0.01, 0.01, 0.01))
Target.location     = 
