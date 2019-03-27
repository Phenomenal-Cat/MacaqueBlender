
#================== AddObjectTrack.py ============================
# Add a rectangular path and make the selected object follow it.

import bpy


#============ Set motion parameters
PathTime    = 8
FPS         = 60




#============ Create rectangular path with rounded corners
bpy.ops.mesh.primitive_plane_add(radius=1.0, location=(0,0,0))              # Create a plane primitive
path                    = bpy.data.objects['Plane']                         # Get plane object handle
path.name               = 'ObjectPath'                                      # Rename object                                     
mod                     = path.modifiers.new(name="Bevel", type='BEVEL')    # Apply a bevel modifier to the plane
mod.use_only_vertices   = True                                              # Adjust bevel parameters
mod.segments            = 5
mod.width               = 0.2
bpy.ops.object.convert(target='CURVE')                                      # Convert mesh to curve

#============ Make object follow path
obj                         = bpy.data.objects['Root']
Follow                      = obj.constraints.new(type='FOLLOW_PATH')
Follow.target               = bpy.data.objects["ObjectPath"]
Follow.forward_axis         = 'FORWARD_X'
Follow.use_curve_follow     = True


#============== Animate object motion
bpy.data.scenes['Scene'].frame_current      = 1									        # First frame
bpy.data.curves["ObjectPath"].eval_time     = 0
bpy.data.curves["ObjectPath"].keyframe_insert(data_path = "eval_time")

bpy.data.scenes['Scene'].frame_current      = PathTime*FPS							   # Repeat for end frame
bpy.data.curves["ObjectPath"].eval_time     = 100
bpy.data.curves["ObjectPath"].keyframe_insert(data_path = "eval_time")

bpy.data.scenes['Scene'].frame_end          = PathTime*FPS
bpy.data.curves["ObjectPath"].animation_data.action.fcurves[0].extrapolation = 'LINEAR'
