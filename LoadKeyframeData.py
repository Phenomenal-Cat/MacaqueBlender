# LoadKeyframes.py

import bpy
import csv

CoordsFile = '/projects/murphya/MacaqueFace3D/Methods Manuscript/Figures/Movies/IdentityMorphDemo/PC1-3_AnimCoords.csv'
RenderDir = '/projects/murphya/MacaqueFace3D/Methods Manuscript/Figures/Movies/IdentityMorphDemo/IdentityMorph_Circ'

with open(CoordsFile, "rt") as csvfile:
    reader = csv.reader(csvfile)    
    AllData = list(reader)
    
csvfile.close()

StartFrame = 331
HeadMesh = bpy.data.objects["AverageMesh_N=23.001"]

for f in range(0, len(AllData)):
    frameIndx = StartFrame+f
    bpy.context.scene.frame_set(frameIndx)
    for pc in range(0, 3):
        HeadMesh.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = float(AllData[f][pc])/2
        HeadMesh.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value")
        
    
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)          
    Filename = "IdentityMorphyCirc_Frame%d" % (f)
    print("Now rendering: " + Filename + " . . .\n")
    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
    bpy.ops.render.render(write_still=True, use_viewport=True)