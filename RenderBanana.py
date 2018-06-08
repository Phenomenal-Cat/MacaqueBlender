
import bpy
import mathutils as mu
import math
from GenerateLightArray import GenerateLightArray
import os.path

Azimuths    = [0, 45, 90, 135, 180, 225, 270, 315]
Lamps       = GenerateLightArray('SPOT','circle')  
RenderDir   = '/Volumes/projects/murphya/AdaptationExp/BananaSet/'

for l in Lamps:
    Lamps[l].location[1] = (-0.8)


for az in Azimuths:
    bpy.data.objects['Banana'].rotation_euler = mu.Vector((0, 0, math.radians(az)))
    lon = 1;
    for lon in Lamps:
        for loff in Lamps:
            Lamps[loff].hide_render = True
        Lamps[lon].hide_render = False
        
        #=========== Render image and save to file
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        RenderFilename = "BananaAdapt_Az%d_El0_Lamp%d.png" % (az, lon)
        if os.path.isfile(RenderDir + "/" + RenderFilename) == 0:
            print("Now rendering: " + RenderFilename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + RenderFilename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + RenderFilename) == 1:
            print("File " + RenderFilename + " already exists. Skipping . . .\n")
    
    