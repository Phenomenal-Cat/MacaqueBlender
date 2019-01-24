
#================================== RenderFruits.py ===================================

import bpy
import mathutils as mu
import math
from GenerateLightArray import GenerateLightArray
from InitBlendScene import InitBlendeScene
from SetDepthMapMode import SetDepthMapMode
import os.path

Fruits      = ['Apple','Banana','Orange','Pear']
Azimuths    = [0, 45, 90, 135, 180, 225, 270, 315]
Elevations  = [0, 45, -45]
Locations   = [[-0.1,0,0], [0,0,0], [0.1,0,0]]


InitBlendScene(2, 1, 97)
Lamps       = GenerateLightArray('SPOT','circle')  
RenderDir   = '/Volumes/projects/murphya/MacaqueFace3D/PreferredLooking/VirtualObject/'

for l in Lamps:
    Lamps[l].location[1] = (-0.8)

#========== Loop through objects
for f in Fruits:
    for az in Azimuths:
        for el in Elevations:
            for loc in Locations:
                bpy.data.objects[f].rotation_euler  = mu.Vector((0, 0, math.radians(az)))   # Set object rotation
                bpy.data.objects[f].location        = loc                                   # set object location
                
                lon = 1;
                for lon in Lamps:
                    for loff in Lamps:
                        Lamps[loff].hide_render = True
                    Lamps[lon].hide_render = False
                    
                    #=========== Render image and save to file
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    
                    for Zmap in range(0,1)
                        SetDepthMapMode(Zmap)   # Toggle between color image .png and Z-map .exr
                    
                        RenderFilename = "%s_Az%d_El%d_Lamp%d.png" % (f, az, el, lon)
                        if os.path.isfile(RenderDir + "/" + RenderFilename) == 0:
                            print("Now rendering: " + RenderFilename + " . . .\n")
                            bpy.context.scene.render.filepath = RenderDir + "/" + RenderFilename
                            bpy.ops.render.render(write_still=True, use_viewport=True)
                        elif os.path.isfile(RenderDir + "/" + RenderFilename) == 1:
                            print("File " + RenderFilename + " already exists. Skipping . . .\n")
        
    