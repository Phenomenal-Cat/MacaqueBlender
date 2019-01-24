
#===================== GazeTrackObject.py ========================
# Set macaque avatar gaze and/or head position to track to follow
# the specified object as it moves through teh scene. 

import bpy
import math
import numpy as np

def makeInvisible(ob, reverse):
    for child in ob.children:
        if reverse == 0:
            child.hide = True
            makeInvisible(child, reverse)
        elif reverse == 1:
            child.hide = False
            makeInvisible(child, reverse)

def RenderFrame(Filename, RenderDir, Render=1, Overwrite=1):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == 1:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")
                        
def RenderAnimation(RenderDir, FilenamePrefix):
    sc = bpy.data.scenes[0]
    for f in range(sc.frame_start, sc.frame_end):
        Filename = FilenamePrefix + "_frame03%d" % (f)
        RenderFrame(Filename, RenderDir)

            
bpy.types.UserPreferencesEdit.keyframe_new_interpolation_type = 'LINEAR'    # F-curve interpolation defaults to linear

#============= Create empty object
obj = bpy.data.objects.new("empty", None)
bpy.context.scene.objects.link(obj)
obj.name = "TrackedObject"

#============= Make empty parent to target object
bpy.data.objects["Banana"].parent = obj

#============= Make gaze follow target by updating constraints
AllBones    = bpy.data.objects["HeaDRig"].pose.bones
EyeBones    = ["eyeL","eyeR"]
for e in EyeBones:
    AllBones[e].constraints["Track To"].target = obj
    
#AllBones["Head"].constraints["IK"].target = obj

#============== Create circular opbject motion path
#PathData    = bpy.data.curves.new('PathData', type='CURVE')
#PathData..dimensions = '2D'         # '2D' or '3D' ?
#PathObj     = bpy.data.objects.new('PathObj', PathData)
#bpy.context.scene.objects.link(PathObj)                         
PathRadius          = 0.15                           # path radius (m)
PathCenter          = (0, -0.2, 0)                  # origin of path (m)
PathOrientation     = np.radians([90, 0, 0])        # rotation of path from horizontal plane (degrees)
PathTime            = 4                             # Time (seconds) for object to complete path
FPS                 = 30                            # Frame rate (Hz)

bpy.ops.curve.primitive_bezier_circle_add(radius=PathRadius, location=PathCenter, rotation=(PathOrientation[0], PathOrientation[1], PathOrientation[2]))

Follow                      = obj.constraints.new(type='FOLLOW_PATH')
Follow.target               = bpy.data.objects["BezierCircle"]
Follow.forward_axis         = 'FORWARD_X'
Follow.use_curve_follow     = False


#============== Animate object motion
bpy.data.scenes['Scene'].frame_current      = 1									        # First frame
bpy.data.curves["BezierCircle"].eval_time   = 0
bpy.data.curves["BezierCircle"].keyframe_insert(data_path = "eval_time")

bpy.data.scenes['Scene'].frame_current      = PathTime*FPS							   # Repeat for end frame
bpy.data.curves["BezierCircle"].eval_time   = 100
bpy.data.curves["BezierCircle"].keyframe_insert(data_path = "eval_time")

bpy.data.scenes['Scene'].frame_end          = PathTime*FPS
bpy.data.curves["BezierCircle"].animation_data.action.fcurves[0].extrapolation = 'LINEAR'

FilenamePrefix = ["Macaque_eyes_gazefollow_", "Macaque_head_gazefollow_", "Object_"]

#============== Loop through rendering
for loop in range(0, 3):
    
    if loop == 0:
        makeInvisible(bpy.data.objects["Root"],1)           # Unhide avatar
        makeInvisible(obj,0)                                # Hide tracked object
    elif loop == 1:
        AllBones["Head"].constraints["IK"].target = obj     # Add head motion
    elif loop == 3:
        makeInvisible(bpy.data.objects["Root"],0)           # Hide avatar
        makeInvisible(obj,1)                                # Unhide tracked object 
        
    RenderAnimation(RenderDir, FilenamePrefix[loop])