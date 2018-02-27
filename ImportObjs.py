
#==================== ImportObjs.py ==========================

import glob
import bpy
import os

Directory   = '/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/MF3D_database/CT_Edited/'
FileFormet  = '.obj'
AllFiles    = glob.glob(Directory + '*' + FileFormat)

for f in AllFiles:
    path, filename = os.path.split(AllFiles[f])
    ID      = filename[0:3]
    objh    = bpy.ops.import_scene.obj(filepath=AllFiles[f])
    obpy.context.selected_objects[0].name = ID
    