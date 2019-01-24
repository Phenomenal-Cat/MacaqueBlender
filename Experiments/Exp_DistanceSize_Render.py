#==================== Exp_DistanceSize_1.py =========================
# This script renders stimuli for an experiment investigating how changes
# in two variables that affect the retinal subtense of an image are encoded: 
#   1) distance of the object from the observer,
#   2) the physical size of the object
#

import bpy
import mathutils as mu
import math
import numpy as np
import socket
import os
#import AddDepthArray

from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath
#import OrientAvatar as OA
from SetDepthMapMode import SetDepthMapMode


def RenderFrame(Filename, RenderDir, Render=1, Overwrite=1):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == 1:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")
                

def HeadLookAt(El, Az):
    Rad = 0.7
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*-Rad
    Y   = np.sin(math.radians(El))*Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ

def makeInvisible(ob, reverse):
    for child in ob.children:
        if reverse == 0:
            child.hide = True
            makeInvisible(child, reverse)
        elif reverse == 1:
            child.hide = False
            makeInvisible(child, reverse)
        

#============ Initialize scene
Prefix              = GetOSpath()                                   # Get path prefix for OS
BlenderDir          = Prefix[0] + '/murphya/Stimuli/AvatarRenders_2018/'            
RenderDir           = BlenderDir + "SizeDistance"
SetupGeometry       = 2                                             # Specify which physical setup stimuli will be presented in
StereoFormat        = 1                                             # Render as stereo-pair?


#============ Set animation parameters
bpy.types.UserPreferencesEdit.keyframe_new_interpolation_type = 'LINEAR'    # F-curve interpolation defaults to linear

Objects             = ['Macaque','Banana','Bucket']           
ObjectLabel         = ['Root', 'Banana','OBJ_bucket']                       
Render              = 1                                                     # 0 = test; 1  = perform render
FPS                 = 30                                                    # Frames per second
DurPerCycle         = 2                                                     # How many seconds per cycle?
NoFrames            = FPS*DurPerCycle
Eccentricities      = [0]	                                                
ViewingDistance     = 60                                                    # Distance of subject from screen (cm) 
Scales              = [0.666, 1.0, 1.333]                                   # Physical scale of object (proportion)
Depths              = [-20, 0, 20] 						                    # Set object depth distance from origin (centimeters)
LateralExtent       = [-20, 20]                                             # Set maximum lateral motion (cm)

#=========== Calculate scale and distance per frame
AllScales           = np.linspace(Scales[0], Scales[2], NoFrames)
AllDepths           = np.linspace(Depths[0], Depths[2], NoFrames)
ConstantRetinalSize = 2*math.atan((1/2)/ViewingDistance)
AllScales_CRS       = []
for f in range(0, len(AllScales)): 
    AllScales_CRS.append(math.tan(ConstantRetinalSize)*(ViewingDistance-AllDepths[len(AllDepths)-f-1]))
	
InitBlendScene(SetupGeometry, StereoFormat, ViewingDistance)            # Initialize scene
#AddDepthArray()                                                         # Add depth array?

#============ Other apperance settings
FurLengths          = [0.7]                                             # Set relative length of fur (0-1)
ExpStr              = ["Neutral","Fear","Threat","Coo","Yawn"]          # Expression names   
ExpNo               = 0 #[0, 1, 2, 3, 4]                              # Expression numbers
Haz                 = 0
ExpWeights          = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights     = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp                = 0
ShowBody            = 1;                                            # Turn on/ off body visibility
IncludeEyesOnly     = 0;                                            # Include eyes only condition? 
InfiniteVergence    = 0;                                            # Fixate (vergence) at infinity?
GazeAtCamera        = 0;                                            # Update gaze direction to maintain eye contact with camera?

NoConditions        = len(Objects)*len(Scales)*len(Depths)          # Calculate total number of conditions
if IncludeEyesOnly == 1:
    NoConditions = NoConditions*2;                      
msg                 = "Total renders = %d" % NoConditions				
print(msg)

#============== FOR QUICK TESTS
#Scene                                   = bpy.data.scenes['Scene']  # Quick and dirty render!
#Scene.render.resolution_percentage      = 25
#bpy.context.scene.cycles.samples        = 10


#=============== Set cyclopean eye as avatar origin point?
head                = bpy.data.objects["HeaDRig"]
body                = bpy.data.objects["Root"]
body.rotation_mode  = 'XYZ'
OffsetCyclopean     = 0                                         # Translate whole avatar so that cyclopean eye is always in the same position?
CyclopeanOrigin     = ((0,0,0))                                 # World coordinate to move cyclopean eye to (if OffsetCyclopean = 1)

bpy.context.scene.cursor_location   = CyclopeanOrigin           # Set current cursor position to cyclopean eye coordinates
bpy.context.scene.objects.active    = body                      # Set avatar rig as active object
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')                 # Set origin of avatar to cyclopean eye                                   

OrigBodyLoc         = body.location 
OrigBodyScale       = body.scale

if ShowBody == 0:
    bpy.data.objects['BodyZremesh2'].hide_render = True                         # Hide body from rendering
    
# bpy.data.particles["ParticleSettings.003"].path_end           = fl            # Set fur length (0-1)
# head.pose.bones['Head'].constraints['IK'].mute                = True          # Turn off constraints on head orientation
# head.pose.bones['HeadTracker'].constraints['IK'].influence    = 0             

#========================== Begin rendering loop
for ob in range(0, len(Objects)):                                               # Loop through object types
    
    for obj in ObjectLabel:
        makeInvisible(bpy.data.objects[obj], 0)                                 # Hide all objects
    makeInvisible(bpy.data.objects[ObjectLabel[ob]], 1)                         # Un-hide current object
    
    #=========== Render depth movies
    for s in Scales:                                                            # Loop through selected fixed scales
        bpy.data.objects[ObjectLabel[ob]].scale = mu.Vector((s, s, s))          # Set FIXED scale
        for f in range(0, NoFrames ):                                           # Loop through distances
            bpy.data.objects[ObjectLabel[ob]].location = mu.Vector((0, AllDepths[f]/100, 0)) 

            for z in [0,1]:
                FileFormat = SetDepthMapMode(z)
                Filename = "%s_%s_Haz%d_Scale%.2f_frame%03d%s" % (Objects[ob], ExpStr[ExpNo], Haz, s, f+1, FileFormat)
                RenderFrame(Filename, RenderDir, Render)
        
    #=========== Render scaling movies
    for d in Depths:                                                    # Loop through selected fixed distances
        bpy.data.objects[ObjectLabel[ob]].location = mu.Vector((0, d/100, 0))    # Set FIXED distance
        for f in range(0, NoFrames):                                    # Loop through scales
            bpy.data.objects[ObjectLabel[ob]].scale = mu.Vector((AllScales[f], AllScales[f], AllScales[f]))
        
            for z in [0,1]:
                FileFormat = SetDepthMapMode(z)
                Filename = "%s_%s_Haz%d_Dist%d_frame%03d%s" % (Objects[ob], ExpStr[ExpNo], Haz, d, f+1, FileFormat)
                RenderFrame(Filename, RenderDir, Render)
    
    #============ Render CONSTANT RETINAL SIZE conditions
    for f in range(0, NoFrames):                   
        bpy.data.objects[ObjectLabel[ob]].scale      = mu.Vector((AllScales_CRS[f], AllScales_CRS[f], AllScales_CRS[f]))
        bpy.data.objects[ObjectLabel[ob]].location   = mu.Vector((0, AllDepths[f]/100, 0)) 
        
        for z in [0,1]:
            FileFormat = SetDepthMapMode(z)
            Filename = "%s_%s_Haz%d_ConstantRetinalSize_frame%03d%s" % (Objects[ob], ExpStr[ExpNo], Haz, f+1, FileFormat)
            RenderFrame(Filename, RenderDir, Render)

    #============ Render LATERAL motion conditions
    bpy.data.objects[ObjectLabel[ob]].scale      = mu.Vector((1, 1, 1))
    
    for f in range(0, NoFrames):          
        bpy.data.objects[ObjectLabel[ob]].location   = mu.Vector((AllDepths[f]/100, 0, 0)) 
        
        for z in [0,1]:
            FileFormat = SetDepthMapMode(z)
            Filename = "%s_%s_Haz%d_LateralMotion_Dist%d_Scale%.2f_frame%03d%s" % (Objects[ob], ExpStr[ExpNo], Haz, 0, 1, f+1, FileFormat)
            RenderFrame(Filename, RenderDir, Render)
            
print('Rendering comleted!')