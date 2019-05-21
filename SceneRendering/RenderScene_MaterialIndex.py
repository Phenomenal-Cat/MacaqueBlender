# RenderScene_MaterialIndex.py

import bpy

#====== Turn on material index pass
Scene = bpy.data.scenes["Scene"]
Scene.render.layers["RenderLayer"].use_pass_material_index = True
Scene.render.use_multiview                  = False
Scene.render.image_settings.file_format     = 'HDR'
Scene.cycles.samples                        = 1

#====== Assign unique index to each material
AllMats = bpy.data.materials
for n in range(0, len(AllMats)):
    AllMats[n].pass_index = n


