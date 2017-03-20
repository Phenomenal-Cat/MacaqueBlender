
#=================== EditTargetObjects.py =======================
# These functions are used to add or remove target objects to or 
# from the scene. 
#

import bpy
import math
import numpy as np
import mathutils as mu
import socket

def AddTargetObjects():
    
    #================= Set target appearance
    AddTex          = 0
    SphereRad       = 0.01                                              # Set sphere radius (meters)
    SphereDepth     = -0.2
    SphereEcc       = 0.12
    SphereNumber    = 8
    SpherePolAng    = np.linspace(0,2*math.pi, SphereNumber+1)
    SphereLocs      = np.zeros((SphereNumber,3))
    for sph in range(0,SphereNumber):
        SphereLocs[sph][0] = SphereEcc*math.sin(SpherePolAng[sph])
        SphereLocs[sph][2] = SphereEcc*math.cos(SpherePolAng[sph])
        SphereLocs[sph][1] = SphereDepth
        
    SphereColor    = (0,0,1)                # Set target colors (RGB)

    #================= Create material
    AllMats = [mat for mat in bpy.data.materials if mat.name.startswith("Target")]
    if all(AllMats):
        mat                     = bpy.data.materials.new("TargetMat")       # Create new material
        mat.diffuse_color       = SphereColor                               # Set material color
        mat.specular_intensity  = 0                                         # Set intensity of specular reflection (0-1)
    elif not(all(AllMats)):
        mat = AllMats[0]
        
    #============ Add texture to target surfaces
    if AddTex == 1:
        heightTex           = bpy.data.textures.new('TargetTex', type = 'CLOUDS')
        heightTex.noise_scale = 0.002


    #================= Create targets
    bpy.ops.group.create(name="Targets")
    #bpy.ops.object.group_link(group="Targets")
    for sph in range(0, len(SphereLocs)):
        if sph == 0:
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions    = 100,
                size            = SphereRad,
                calc_uvs        = False,
                view_align      = False,
                enter_editmode  = False,
                location        = SphereLocs[sph],
                rotation        = (0,0,0))
            bpy.data.objects['Icosphere'].active_material   = mat                           # Set target color
            bpy.data.objects['Icosphere'].name              = "Target %d" % sph             # Rename object as target ID
            if AddTex == 1:
                dispMod             = bpy.context.scene.objects["Target 0"].modifiers.new("Displace", type='DISPLACE')
                dispMod.texture     = heightTex
                dispMod.strength    = 0.001
        elif sph  > 0:
            d = bpy.data.objects['Target 0'].copy()
            bpy.context.scene.objects.link(d)
            d.location      = SphereLocs[sph]
            d.name          = "Target %d" % sph  
            
            
    bpy.context.scene.objects["Target %d" % sph].select = True
    bpy.ops.object.group_link(group="Targets")    
    bpy.context.scene.objects["Target %d"  % sph].select = False
    #bpy.context.scene.objects.active = d
    #bpy.ops.group.objects_add_active(group = "Targets")
    return SphereLocs
        
        
def RemoveTargetObjects():
    scene        = bpy.context.scene
    AllTargets   = [obj for obj in scene.objects if obj.name.startswith("Target")]  # Find all objects in scene with 'Target' in name
    for t in range(0,len(AllTargets)):
        AllTargets[t].select = True         # Select next target object
        bpy.ops.object.delete()             # Delete target object
        

def EditTargetObjects(Add):
    
    if Add == 1:
        Locs = AddTargetObjects()
    elif Add == 0:
        RemoveTargetObjects()
        
def MonkeyLookAt(HeadLoc, GazeLoc):
    bpy.data.objects["HeaDRig"].pose.bones['EyesTracker'].location = mu.Vector((GazeLoc)) 
    bpy.data.objects["HeaDRig"].pose.bones['HeadTracker'].location = mu.Vector((HeadLoc[0],HeadLoc[2],HeadLoc[1]))

        
def RenderAllViewsStill(Locs):
    Congruent = 0
    if socket.gethostname().find("Aidans-Mac")==0:
        RenderDir = '/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/Renders/CuedLocations'
    elif socket.gethostname().find("DESKTOP-5PBDLG6")==0:
        RenderDir = 'P:\murphya\Blender\Renders\CuedAttention'
    elif socket.gethostname().find("MH01918639MACDT")==0:
        RenderDir = 'P:\murphya\Blender\Renders\CuedAttention'
        
    for l in range(0, len(Locs)):
        if Congruent == 1:
            GazeLoc = (0, 0.03, 0.2)
            MonkeyLookAt(Locs[l], GazeLoc)
        elif Congruent == 0:
            bpy.data.objects["HeaDRig"].pose.bones['blink'].location = mu.Vector((0,0,0))   # Open eye lids 
            MonkeyLookAt((0,-0.2,0), (Locs[l][0], Locs[l][2], 0.1) )
            
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        Filename = "CuedLocation_V2_headLoc%s.png" % (l)
        print("Now rendering: " + Filename + " . . .\n")
        bpy.context.scene.render.filepath = RenderDir + "/" + Filename
        bpy.ops.render.render(write_still=True, use_viewport=True)
    
        
        
def RenderAllViewsAnimated(Locs):
    
    #================ Set animation parameters
    Congruent                               = 1
    ClipDuration                            = 2                 # Duration of each animation (seconds)   
    bpy.data.scenes["Scene"].render.fps     = 60                # Set frame rate (Hz)  
    bpy.data.scenes["Scene"].frame_start    = 1
    bpy.data.scenes["Scene"].frame_end      = (ClipDuration*bpy.data.scenes["Scene"].render.fps)+1
    bpy.data.scenes["Scene"].frame_step     = 1
    bpy.data.scenes["Scene"].render.image_settings.file_format = 'PNG' 

    
    #================ Set save directory
    if socket.gethostname().find("Aidans-Mac")==0:
        RenderDir = '/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/Renders/CuedLocations'
    elif socket.gethostname().find("DESKTOP-5PBDLG6")==0:
        RenderDir = 'P:\murphya\Blender\Renders\CuedAttention\AnimationFrames'
    elif socket.gethostname().find("MH01918639MACDT")==0:
        RenderDir = 'P:\murphya\Blender\Renders\CuedAttention\AnimationFrames'
        
    #================ Loop through targets    
    for l in range(0, len(Locs)):
        
        #============ Set default gaze/head position for frame 1
        bpy.context.scene.frame_set(1)
        GazeLoc         = (0, 0.03, 0.2)
        DefaultHeadLoc  = (0, 0, 0)
        MonkeyLookAt(DefaultHeadLoc, GazeLoc)
        bpy.data.objects["HeaDRig"].pose.bones['EyesTracker'].keyframe_insert(data_path = "location")
        bpy.data.objects["HeaDRig"].pose.bones['HeadTracker'].keyframe_insert(data_path = "location")
        
        #============ Set target gaze/head position
        bpy.context.scene.frame_set(np.round(bpy.data.scenes["Scene"].frame_end/2))
        if Congruent == 1:
            MonkeyLookAt(Locs[l], GazeLoc)
            bpy.data.objects["HeaDRig"].pose.bones['EyesTracker'].keyframe_insert(data_path = "location")
            bpy.data.objects["HeaDRig"].pose.bones['HeadTracker'].keyframe_insert(data_path = "location")
            
        elif Congruent == 0:
            bpy.data.objects["HeaDRig"].pose.bones['blink'].location = mu.Vector((0,0,0))   # Open eye lids 
            MonkeyLookAt(Locs[l], GazeLoc)
            bpy.data.objects["HeaDRig"].pose.bones['EyesTracker'].keyframe_insert(data_path = "location")
            bpy.data.objects["HeaDRig"].pose.bones['HeadTracker'].keyframe_insert(data_path = "location")

        #============ Return to default gaze/head position for final frame
        bpy.context.scene.frame_set(bpy.data.scenes["Scene"].frame_end)
        MonkeyLookAt(DefaultHeadLoc, GazeLoc)
        bpy.data.objects["HeaDRig"].pose.bones['EyesTracker'].keyframe_insert(data_path = "location")
        bpy.data.objects["HeaDRig"].pose.bones['HeadTracker'].keyframe_insert(data_path = "location")
        
        #============ Render keyframe sequence
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        for f in range(1, bpy.data.scenes["Scene"].frame_end):
            bpy.context.scene.frame_set( f )                                # Set current frame
            Filename = "LookAtLocation_Target%s_Frame%03d.png" % (l, f)
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        
        
#RemoveTargetObjects()
Locs = AddTargetObjects()

#bpy.data.objects["HeaDRig"].pose.bones['blink'].location = mu.Vector((0,0,0.007))   # Close eye lids (blink)
#MonkeyLookAt(Locs[7], Locs[1])


#RenderAllViewsStill(Locs)
RenderAllViewsAnimated(Locs)

#Loc = [0.15,0.2,0]
#MonkeyLookAt(Locs[3], Locs[3])
    



    
    
    
