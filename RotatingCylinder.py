 # RotatingCylinder.py

import bpy
import numpy as np
import os

# Set SFM stimulus parameters
CylinderRadius  = 0.05
CylinderHeight  = 0.15
CylinderDepths  = [-1, -0.5, -0.25, 0, 0.25, 0.5, 1]
CylinderLoc     = (0, 0, 0)
Orientation     = (0,0,0) 
NoDots          = 100                       # Total number of dots on surface
DotRadius       = 0.001                     # Dot (sphere) radius (m)
FPS             = 30 
RotationDur     = 4                         # Duration of one rotation (seconds)
TotalFrames     = FPS*RotationDur           # Number of frames for one rotation
CylinderLayer   = 2                         # Which render layer to add cylinder object to?

CameraDist      = np.absolute(bpy.data.objects["Camera"].location[1]) + CylinderLoc[1])
DotDegMed       = np.arctan(2*DotRadius / np.absolute(CameraDist))
DotDegMin       = np.arctan(2*DotRadius / np.absolute(CameraDist)-CylinderRadius)
DotDegMax       = np.arctan(2*DotRadius / np.absolute(CameraDist)+CylinderRadius)
DotScaleMin     = 

RenderDir       = '/projects/murphya/Stimuli/Avatarrenders_2018/RotatingCylinders/Frames/';

# Set randmoized dot positions
Zpos            = (np.random.rand(1,NoDots)*CylinderHeight)-CylinderHeight/2
Xpos            = (np.random.rand(1,NoDots)*CylinderRadius*2)-CylinderRadius
Ypos            = np.sin(Xpos)/CylinderRadius
StartPoint      = np.random.rand(1,NoDots)

# Create new material
bpy.ops.cycles.use_shading_nodes
bpy.data.materials.new("DotMat")      # Create new material
mat             = bpy.data.materials["DotMat"] 
mat.use_nodes   = True
nodes           = mat.node_tree.nodes                   # Get nodes

# Create nodes
node_emission   = nodes.new(type='ShaderNodeEmission')
node_emission.inputs[0].default_value = (1,1,1,1)
node_emission.inputs[1].default_value = 1.0
node_emission.location = 0,0

# Create output node
node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_output.location = 400, 0

# Link nodes
links = mat.node_tree.links
link = links.new(node_emission.outputs[0], node_output.inputs[0])

# Draw cylinder dots
for z in range(0, len(Zpos[0])):
    
    bpy.ops.curve.primitive_bezier_circle_add(radius=CylinderRadius, location= ((CylinderLoc[0], CylinderLoc[1], (CylinderLoc[2]+Zpos[0][z]))))              # Create a plane primitive
    bpy.ops.mesh.primitive_uv_sphere_add(size=DotRadius, location = (0,0,0))
    
    #============ Make sphere follow path
    Dot                         = bpy.data.objects['Sphere']
    Dot.name                    = "Sphere %d" % z
    Dot.active_material         = mat
    Dot.layers[CylinderLayer]   = True
    Path                        = bpy.data.objects['BezierCircle']
    Path.name                   = "Path %d" % z
    Path.scale                  = (1, 1, 1)
    #Path.hide                   = True
    Follow                      = Dot.constraints.new(type='FOLLOW_PATH')
    Follow.target               = Path
    Follow.forward_axis         = 'FORWARD_Z'
    Follow.up_axis              = 'UP_Y'
    Follow.use_curve_follow     = False
    
    #============== Animate object motion
    Curve               = bpy.data.curves["BezierCircle"]
    Curve.name          = "Curve %d" % z 
    bpy.data.scenes['Scene'].frame_current      = 1						    # First frame
    Curve.eval_time   = StartPoint[0][z]*TotalFrames                        # Randomize starting point
    Curve.keyframe_insert(data_path = "eval_time")                          # Insert first keyframe

    bpy.data.scenes['Scene'].frame_current      = TotalFrames			    # Repeat for end frame
    Curve.eval_time   = (StartPoint[0][z]*TotalFrames)+TotalFrames	
    Curve.keyframe_insert(data_path = "eval_time")                
    
    #============== Animate object scale
    Dot.scale   = ()                                                        # Set dot scale
    Dot.keyframe_insert(datapath='scale', frame= 1)                         # Insert keyframe
    
    FrontFrame  = StartPoint[0][z]
    Dot.scale   = ()                                                        # Set dot scale
    Dot.keyframe_insert(datapath='scale', frame= FrontFrame)                # Insert keyframe
    
    BackFrame   = FrontFrame + TotalFrames/2
    Dot.scale   = ()                                                        # Set dot scale
    Dot.keyframe_insert(datapath='scale', frame= BackFrame)                 # Insert keyframe

    Dot.Scale   = ()
    Dot.keyframe_insert(datapath='scale', frame= TotalFrames)               # Insert keyframe

    #============== 
    bpy.data.scenes['Scene'].frame_end          = TotalFrames
    Curve.path_duration                         = TotalFrames
    Curve.animation_data.action.fcurves[0].extrapolation = 'LINEAR'
    

#============== Loop through cylinder depths
for d in CylinderDepths:
    
    #========= Rescale paths for all dots
    for z in range(0, len(Zpos[0])):                        # For each dot
        Path            = bpy.data.objects["Path %d" % z]   # Find path name
        Path.scale      = (1, d, 1)                         # Scale path depth
        
    for frame in range(1, TotalFrames):                     # For each frame
        bpy.context.scene.frame_current = frame             # Go to frame
        
        #=========== Render image and save to file
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        RenderFilename = "RotatingCylinder_Depth%f_frame%03d.png" % (d, frame)
        if os.path.isfile(RenderDir + "/" + RenderFilename) == 0:
            print("Now rendering: " + RenderFilename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + RenderFilename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + RenderFilename) == 1:
            print("File " + RenderFilename + " already exists. Skipping . . .\n")
    
    
    
    

