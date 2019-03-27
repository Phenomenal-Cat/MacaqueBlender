
# SetLabelMapMode.py

import bpy


Scene = bpy.data.scenes['Scene']
Scene.render.layers['RenderLayer'].use_pass_object_index    = True
Scene.render.layers['RenderLayer'].use_pass_material_index  = True

