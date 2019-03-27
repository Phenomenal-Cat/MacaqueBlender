
#=================== ReorderVertices.py ====================
# After editing in other software, a meshes vertex order may 
# have changed. This script checks the vertices of mesh A
# and re-arranges the order of vertices of mash B to match. 
# A and B must be identical meshes (same vertices, just different
# orders).

import bpy
import bmesh
import numpy as np
import csv

TestDir         = '/Volumes/projects/murphya/MacaqueFace3D/MeshMorphing/ObjExportTest/'
ObjectNames     = ['Macaque09_BaseMesh_KeepVertex', 'MBase1']

for o in range(len(Objectnames):
    #======== Read from object
#    obj      = bpy.data.objects[ObjectNames[o]]
#    bm      = bmesh.from_edit_mesh(obj.data)
#    verts   = [vert.co for vert in bm.verts]
    
    #======== Read polygon vert indx from mesh
    data            = bpy.data.meshes[ObjectNames[o]]
    FaceIndices     = np.empty((len(data.polygons),4))
    for f in range(len(data.polygons)):
        for v in range(len(data.polygons[f].vertices)):
            FaceIndices[f][v] = data.polygons[f].vertices[v]

    #========== Write face indices to file
    CSVfile = TestDir + 'CompareFaceIndx_' + ObjectNames[o] + '.csv'
    with open(CSVfile, mode='w') as verts_file:
        vert_writer = csv.writer(verts_file, delimiter=',')
        for f in range(len(FaceIndices)):
            vert_writer.writerow(FaceIndices[f])
            
    #========== Write vertex data to file
    CSVfile = TestDir + 'CompareVerts_' + ObjectNames[o] + '.csv'
    with open(CSVfile, mode='w') as verts_file:
        vert_writer = csv.writer(verts_file, delimiter=',')
        for v in range(len(data.vertices)):
            vert_writer.writerow(data.vertices[v].co)




verts2   = [vert.co for vert in bm2.verts]


if len(verts1) -= len(verts2):
    print('These meshes have different number of vertices!')
    
if np.allclose(verts1, verts2):
    print('These meshes have identical vertices!')

#========== Write vertices to file
CSVfile = '/Volumes/projects/murphya/MacaqueFace3D/MeshMorphing/ObjExportTest/CompareVerts_M02_Edited.csv'
with open(CSVfile, mode='w') as verts_file:
    vert_writer = csv.writer(verts_file, delimiter=',')
    bm         = bmesh.from_edit_mesh(obj.data)
    for f in bm2.faces:
        for v in f.verts:
            vert_writer.writerow(v.co)
        
#    for v1 in range(len(verts1)):
#        vert_writer.writerow(verts1[v1])
    

#========== Find vertex matches
NewOrder = np.empty
for v1 in range(len(verts1)):
    for v2 in range(len(verts2)):
        if verts1[v1] == verts2[v2]:
            NewOrder[v1] = v2
            break
    if not NewOrder[v1]:
        printf('No matching vertices found for vertex!')

            