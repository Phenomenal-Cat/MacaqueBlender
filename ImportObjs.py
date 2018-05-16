
#==================== ImportObjs.py ==========================

import glob
import bpy
import os

Directory   = '/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/MF3D_database/CT_Edited/'
RenderDir   = '/Volumes/PROJECTS/murphya/MacaqueFace3D/Documents/Feedback/'
FileFormat  = '.obj'
AllFiles    = glob.glob(Directory + '*' + FileFormat)
RenderEach  = 0

BaseMesh    = bpy.data.objects['MBase1']                # Base mesh object
SkinMat     = BaseMesh.active_material                  # Skin material (diffuse)


for f in AllFiles:
    print('Importing mesh file ' + f)
    path, filename = os.path.split(f)
    ID      = filename[0:3]
    objh    = bpy.ops.import_scene.obj(filepath=f)
    bpy.context.selected_objects[0].name = ID
    obj     = bpy.data.objects[ID]                              # Get new object
    for i in range(len(obj.material_slots)):                    # For each material of this object...
        bpy.ops.object.material_slot_remove({'object': obj})    # Remove existing materials
    obj.active_material = SkinMat                               # Apply existing skin material to new mesh
    
    
    if RenderEach == 1:
        BaseMesh.hde_render = True
        bpy.context.scene.render.filepath = RenderDir + "/" + ID
        bpy.ops.render.render(write_still=True, use_viewport=True)
    
    bpy.data.objects[ID].hide           = True          # Make mesh invisible in preview
    bpy.data.objects[ID].hide_render    = True          # Make mesh invisible in render output
    
    #bpy.ops.object.material_slot_copy                   