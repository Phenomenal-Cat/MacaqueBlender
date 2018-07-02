
#======================= CompareMeshes.py ======================== 
# This script loads raw and wrapped versions of the same identity
# mesh into a Blender scene for direct comparison.

import os
import glob
import bpy
import math
import mathutils

MeshDirRaw      = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/MF3D_database/CT_meshes"
MeshDirWrap     = "/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/MF3D_database/CT_wrapped_meshes"
MeshDirEdited   = ""

MeshDirRaw      = "/Volumes/rawdata/murphya/CT/CT_RawMeshes/"
MeshDirWrap     = "/Volumes/procdata/murphya/Wrapped_meshes/"
MeshDirEdited   = "/Volumes/procdata/murphya/CT/Edited Ent/"


Identities      = [18]#:30
FileFormatRaw   = ".stl"
FileFormatWrap  = ".obj"
FileFormatEdit  = ".obj"
OpenEyesSuffix  = "01"

for M in Identities:
    
    Filename = "M%02d_*%s" % (M, FileFormatWrap)                            # Specify filename pattern
    MeshFile = glob.glob(MeshDirWrap + "/" + Filename)                      # Find wrapped mesh file
    if MeshFile:                                                            # If a wrapped mesh file was found...
        bpy.ops.import_scene.obj(filepath=MeshFile[0])                      # Import wrapped mesh
        WrappedObj = bpy.context.selected_objects[0]                        # Get name of imported mesh object
        
        Filename = "M%02d_*%s" % (M, FileFormatRaw)                         # Specify filename pattern
        MeshFile = glob.glob(MeshDirRaw + "/" + Filename)                   # Find raw mesh file
        bpy.ops.import_mesh.stl(filepath=MeshFile[0], global_scale=0.01)    # Import raw mesh (scaled down to 1%)
        RawObj = bpy.context.selected_objects[0]                            # Get name of imported mesh object
        RawObj.rotation_euler = mathutils.Vector((math.radians(-90), 0, math.radians(180)))
        RawObj.location = mathutils.Vector((-1,0,0))
    
    