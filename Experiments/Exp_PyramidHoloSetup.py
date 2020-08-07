
# Exp_PyramidHoloSeup.py

import bpy
import math
import os

#====== Link all objects in scene A to scene B
def LinkObjects2Scene(DestScene):
    bpy.context.window.scene = DestScene                        # Make destination scene active
    for ob in bpy.data.objects:
        if ob.name in bpy.context.scene.collection.objects:
            print("Object %s already in scene" % ob.name)    
        else:
            if ob.type != 'CAMERA':
                bpy.context.scene.collection.objects.link(ob)       # Link objects to new scene

#====== Create new collection
def make_collection(collection_name, parent_collection):
    if collection_name in bpy.data.collections: # Does the collection already exist?
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection) # Add the new collection under a parent
        return new_collection
    
#====== Add cameras to the scene
def CreateCams():
    for c in range(0, len(CamXY)):
        scn = bpy.data.scenes.new(name='Scene %d' % c)              # Add new scene
        bpy.context.window.scene = scn                              # Make new scene active
        LinkObjects2Scene(scn)
        cam = bpy.data.cameras.new("Camera %d" % c)                 # Create new camera object in scene
        cam.lens_unit = 'FOV'
        cam.lens = CamFOV
        cam_obj = bpy.data.objects.new("Camera %d" % c, cam)
        #collection.objects.link(cam_obj) 
        cam_obj.location = (CamXY[c][0]*CamRadius, CamXY[c][1]*CamRadius, CamZ)
        cam_obj.rotation_euler = (math.radians(CamRot[c][0]), math.radians(CamRot[c][1]), math.radians(CamRot[c][2]))
        scn.collection.objects.link(cam_obj)
 
#====== Add nodes to the compositor
def SetupCompositor():
    
    ImRotate    = [90, 0, -90, 180]
    ImTrans     = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    ImTransScale = 500
    
    #======== Prepare compositing
    bpy.context.scene.use_nodes = True          # Enable nodes
    tree = bpy.context.scene.node_tree          # Get node tree handle
    for node in tree.nodes:                     # Remove current nodes
        tree.nodes.remove(node)
    links = tree.links                          # create link nodes
    composite_node = tree.nodes.new(type='CompositorNodeComposite')
    composite_node.location = 600,400
    sum_node = tree.nodes.new(type='CompositorNodeAlphaOver')
    sum_node.location = 400,400
    viewer_node = tree.nodes.new(type='CompositorNodeViewer')
    viewer_node.location = 600, 200
    link = links.new(sum_node.outputs[0], composite_node.inputs[0])
    link = links.new(sum_node.outputs[0], viewer_node.inputs[0])
    
    #======== Add input nodes
    for c in range(0, len(CamXY)):
        render_node = tree.nodes.new(type='CompositorNodeRLayers')
        render_node.location = -300,200*c
        transform_node = tree.nodes.new(type='CompositorNodeTransform')
        transform_node.location = 0,200*c
        transform_node.inputs[1].default_value = ImTrans[c][0]*ImTransScale
        transform_node.inputs[2].default_value = ImTrans[c][1]*ImTransScale
        transform_node.inputs[3].default_value = math.radians(ImRotate[c])
        link = links.new(render_node.outputs[0], transform_node.inputs[0])
        if c == 0:
            add_node1 = tree.nodes.new(type='CompositorNodeAlphaOver')
            add_node1.location = 200,200
            link = links.new(transform_node.outputs[0], add_node1.inputs[1])
            link = links.new(add_node1.outputs[0], sum_node.inputs[1])
        elif c == 1:
            link = links.new(transform_node.outputs[0], add_node1.inputs[2])
        elif c == 2:
            add_node2 = tree.nodes.new(type='CompositorNodeAlphaOver')
            add_node2.location = 200,600
            link = links.new(transform_node.outputs[0], add_node2.inputs[1])
            link = links.new(add_node2.outputs[0], sum_node.inputs[2])
        elif c == 3:
            link = links.new(transform_node.outputs[0], add_node2.inputs[2])

        
#====== Render from each and composite
def RenderCams():
    for ob in scn.objects:
        if ob.type == 'CAMERA':
            scn.camera = ob
            print('Set camera %s' % ob.name )
            file = os.path.join("C:/tmp", ob.name )
            bpy.context.scene.render.filepath = file
            bpy.ops.render.render( write_still=True )
        

scn = bpy.context.scene

#====== Pyramid dimensions
# based on https://www.youtube.com/watch?v=qNceVquu02o
SmallSquare = 1.5       # cm
LargeSquare = 9.0       # cm
Height      = 5.5       # cm
Depth       = (LargeSquare/2)-(SmallSquare /2)
Angle       = math.degrees(math.atan(Height/Depth))


#====== Camera settings
CamRadius   = 0.80    # Camera distance from origin (meters)
CamZ        = 0.00      # Camera height above ground plane (meters)
CamXY       = [[0,1],[1,0],[0,-1,],[-1,0]] 
CamRot      = [[90, 0, 180], [90, 0, 90], [90, 0, 0], [90, 0, -90]]
CamFOV      = 45

ResX = 1000
ResY = 1000
Stereo = 1

#======= Render settings
for s in bpy.data.scenes:
    s.render.film_transparent = True
    s.render.resolution_x = ResX
    s.render.resolution_y = ResY
    s.render.use_multiview = True
    if Stereo == 1:
        s.render.views_format = 'STEREO_3D'
        s.render.image_settings.views_format = 'STEREO_3D'
        s.render.image_settings.stereo_3d_format.display_mode = 'ANAGLYPH'
        s.render.image_settings.stereo_3d_format.anaglyph_type = 'RED_CYAN'
        
if Stereo == 1:
    for c in bpy.data.cameras:
        c.stereo.convergence_mode = 'OFFAXIS'
        c.stereo.convergence_distance = CamRadius 
        c.stereo.interocular_distance = 0.065
        c.stereo.pivot = 'CENTER'


CreateCams()
#RenderCams()
SetupCompositor()
