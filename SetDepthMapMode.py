# ============================ SetDepthMapMode.py =============================
# This function toggles the Macaque Avatar .blend scene between regular colour
# rendering mode and Z-pass buffer rendering mode. The output of the Z-buffer
# can be saved to HRD image formats for generating random-dot stereograms (RDSs)
# or kinematograms (RDKs), for depth-cue control conditions in vision experiments.
#
# ZmapOn = 0:   renders are saved as 8-bit RGBA image matrices where pixel
#               values correspond to luminance and are saved to .png file.
# ZmapOn = 1:   renders are saved as HDR images in a 2D matrix where pixel 
#               values correspond to object distance from camera in meters, 
#               and are saved to .exr file.
# =============================================================================

import bpy

def SetDepthMapMode(ZmapOn=0):
    
    Scene = bpy.data.scenes["Scene"]
    if bpy.context.scene.node_tree is None:                                 # If no scene nodes exist
        Scene.use_nodes = True                                              # Turn scene nodes on
    Nodes = bpy.context.scene.node_tree.nodes                               
    Scene.render.layers["RenderLayer"].use_pass_z   = True                  

    AvatarObjs = ['CorneaR','CorneaL']
    if ZmapOn == 1:
        for obj in AvatarObjs:
            if bpy.data.objects.get(obj) is not None:
                bpy.data.objects[obj].hide_render     = True                  # Hide corneas from rendering (cause issues with Z map)
                                                   
        #Scene.render.image_settings.file_format     = 'OPEN_EXR'
        Scene.render.image_settings.file_format     = 'HDR'
        Scene.render.image_settings.use_zbuffer     = True
        Scene.render.use_multiview                  = False             
        if bpy.app.version < (2, 79, 0):                                    # Thanks a lot Blender devs!
            RenderNode  = Nodes['Render Layers'].outputs['Z']  
        else:
            RenderNode  = Nodes['Render Layers'].outputs['Depth']   
        #FileFormat  = '.exr'
        FileFormat  = '.hdr'
        
    elif ZmapOn == 0:
        for obj in AvatarObjs:
            if bpy.data.objects.get(obj) is not None:
                bpy.data.objects[obj].hide_render     = False                 # Unhide corneas
                 
        Scene.render.image_settings.file_format     = 'PNG'
        Scene.render.image_settings.color_depth     = '8'                       # Reset to default 8-bit color depth
        Scene.render.image_settings.use_zbuffer     = False
        Scene.render.use_multiview                  = True
        RenderNode  = Nodes['Render Layers'].outputs['Image']  
        FileFormat  = '.png' 
        
    
    CompNode    = Nodes['Composite'].inputs['Image']                
    Links       = bpy.context.scene.node_tree.links.new(RenderNode, CompNode)
    return FileFormat