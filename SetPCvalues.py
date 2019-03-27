
# Set PC values

import bpy
import numpy as np

PCvals    = np.zeros(shape=(4,10))
PCvals[0] = [-0.3198, 0.0971, 0.0791, 0.0222, -0.1431, 0.0771, 0.0501, -0.0821, 0.0058, 0.0001] # Female
PCvals[1] = [0.1649, 0.2166, 0.1418,-0.1503, 0.0696, -0.0410, -0.0268, 0.0664, -0.0362, 0.0047] # Male
PCvals[2] = [-0.1796, -0.1389, -0.0077, 0.0395, 0.0715, -0.0350, 0.0282, 0.0007, 0.0599, 0.0105]# Young
PCvals[3] = [0.0575, -0.2382,-0.1314,-0.0610,-0.0097,-0.0034,0.0036, 0.0932, -0.0064, -0.0634]  # Old

RenderDir = '/Volumes/Seagate Backup 1/NIH_Postdoc/MacaqueFace3D/Methods Manuscript/Figures/Renders'

HeadMesh   = bpy.data.objects["AverageMesh_N=23.001"]
for n in range(len(PCvals)):
    for pc in range(0, 10):
        HeadMesh.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = PCvals[n][pc]
        HeadMesh.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value")
    
    #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)          
    Filename = "Fig1E_Frame%d" % (n)
    print("Now rendering: " + Filename + " . . .\n")
    bpy.context.scene.render.filepath = RenderDir + "/" + Filename
    #bpy.ops.render.render(write_still=True, use_viewport=True)