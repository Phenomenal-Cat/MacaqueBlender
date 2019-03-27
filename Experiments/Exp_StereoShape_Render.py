#==================== Exp_StereoShape_Render.py =========================
# This script renders stimuli for an experiment investigating how changes
# in stereocopically defined 3D shape affect neural responses.


import bpy
import mathutils as mu
import math
import numpy as np
import socket
import os
import fnmatch

from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath
from SetDepthMapMode import SetDepthMapMode


def RenderFrame(Filename, RenderDir, Render=1, Overwrite=0):
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    if Render == 1:
        #Filename = Filename[0:-4] + '_L.png'
        #if FileExists == 0:
        if os.path.isfile(RenderDir + "/" + Filename) == 0:
            print("Now rendering: " + Filename + " . . .\n")
            bpy.context.scene.render.filepath = RenderDir + "/" + Filename
            bpy.ops.render.render(write_still=True, use_viewport=True)
        elif os.path.isfile(RenderDir + "/" + Filename) == 1:
            print("File " + Filename + " already exists. Skipping . . .\n")

def find_files(base, pattern):
    return [n for n in fnmatch.filter(os.listdir(base), pattern) if
        os.path.isfile(os.path.join(base, n))]

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
RenderDir           = BlenderDir + "StereoShape/StereoPairs/Apple" 
SetupGeometry       = 2                                             # Specify which physical setup stimuli will be presented in
StereoFormat        = 1                                             # Render as stereo-pair?

#============ Set animation parameters
bpy.types.UserPreferencesEdit.keyframe_new_interpolation_type = 'LINEAR'    # F-curve interpolation defaults to linear

Objects             = ['Apple','Banana','Macaque','Human']           
ObjectLabel         = ['Apple','Banana','Root','Male03_Neutral']                       
Render              = 1                                                     # 0 = test; 1  = perform render                     
ob                  = 0             

ViewingDistance     = 60                                                    # Distance of subject from screen (cm) 
Depths              = [-20, 0, 20] 						                    # Set object depth distance from origin (centimeters)
ShapeDepthsProp     = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]
VirtualIPDs         = [[-4.3652,-3.0116,-1.5602,0,1.6818,3.5,5.4718], [-4.64, -3.167, -1.622, 0, 1.705, 3.5, 5.39], [-4.7840,-3.2470,-1.6534,0,1.7166,3.5,5.3543]]

InitBlendScene(SetupGeometry, StereoFormat, ViewingDistance)            # Initialize scene
#AddDepthArray()                                                         # Add depth array?

#============ Other apperance settings
FurLengths          = [0.7]                                             # Set relative length of fur (0-1)
ExpStr              = ["Neutral","Fear","Threat","Coo","Yawn"]          # Expression names   
ExpNo               = 0 #[0, 1, 2, 3, 4]                              # Expression numbers
HeadAzimuths        = [-30, 0, 30] 
HeadElevations      = [-30, 0, 30]
ExpWeights          = np.matrix([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
ExpMicroWeights     = np.matrix([[0,0,0,0.5],[1,0,0,0.5],[0,1,0,0.5],[0,0,1,0.5]])
mexp                = 0
ShowBody            = 1;                                            # Turn on/ off body visibility
IncludeEyesOnly     = 0;                                            # Include eyes only condition? 
InfiniteVergence    = 0;                                            # Fixate (vergence) at infinity?
GazeAtCamera        = 0;                                            # Update gaze direction to maintain eye contact with camera?

NoConditions = len(Depths)*len(ShapeDepthsProp)*len(HeadAzimuths)*len(HeadElevations)
if IncludeEyesOnly == 1:
    NoConditions = NoConditions*2;                      
msg                 = "Total renders = %d" % NoConditions				
print(msg)

#============== FOR QUICK TESTS
#Scene                                   = bpy.data.scenes['Scene']  # Quick and dirty render!
#Scene.render.resolution_percentage      = 25
#bpy.context.scene.cycles.samples        = 10


#=============== Set cyclopean eye as avatar origin point?
if ObjectLabel[ob] == "Root":
    head                = bpy.data.objects["HeaDRig"]
    body                = bpy.data.objects["Root"]
    body.rotation_mode  = 'XYZ'
    
    StereoSet           = bpy.context.scene.render.image_settings
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

Scene = bpy.data.scenes["Scene"]
#Scene.render.image_settings.file_format     = 'HDR'        # TEMPORARY FIX <<<<<<<<<<
#FileFormat                                  = '.hdr'
Scene.render.use_multiview                  = False
FileFormat                                  = '.png'
Scene.render.views_format                   = 'STEREO_3D'

StereoSet                                       = bpy.context.scene.render.image_settings

#========================== Begin rendering loop
for Haz in HeadAzimuths:
    for Hel in HeadElevations:
        
        if ObjectLabel[ob] == 'Root':
            HeadXYZ = HeadLookAt(Hel, Haz)
            head.pose.bones['HeadTracker'].location  = HeadXYZ
        else:
            bpy.data.objects[ObjectLabel[ob]].rotation_euler = ((np.radians(Hel), 0, np.radians(Haz)))
        
        for d in [0,2]:

            if ObjectLabel[ob] == 'Root':
                body.location = ((0, Depths[d]/100, 0))                 # Move avatar to specified depth
            else:
                bpy.data.objects[ObjectLabel[ob]].location = ((0, Depths[d]/100, 0))
            
            if Depths[d] == 0:
                Scene.render.image_settings.views_format        = 'STEREO_3D'
            else:
                Scene.render.image_settings.views_format        = 'INDIVIDUAL'
                
        	#======= Render depth map
            #FileFormat = SetDepthMapMode(1)							# Switch to Z-buffer rendering
            #Filename = "%sDepth_Haz%d_Hel%d_Depth%d_DepthMap%s" % (Objects[ob], Haz, Hel, Depths[d], FileFormat)
            #RenderFrame(Filename, RenderDir, Render)
    #            FileFormat = SetDepthMapMode(0) 						# Switch off z-buffer rendering
    	
	        #======= Render stereo pairs
            for ipd in range(0, len(VirtualIPDs[d])):
                bpy.data.cameras["Camera"].stereo.interocular_distance = abs(VirtualIPDs[d][ipd]/100)           # Set interaxial distance
                bpy.data.cameras["Camera"].stereo.convergence_distance = (ViewingDistance + Depths[d])/100      # Set distance of convergence plane

                if VirtualIPDs[d][ipd] < 0:
                    StereoSet.stereo_3d_format.use_sidebyside_crosseyed = True
                else:  
                    StereoSet.stereo_3d_format.use_sidebyside_crosseyed = False
                        
                Filename = "%sDepth_Haz%d_Hel%d_PID%d_DepthScale%.1f%s" % (Objects[ob], Haz, Hel, Depths[d], ShapeDepthsProp[ipd], FileFormat)
                RenderFrame(Filename, RenderDir, Render)
                
print('Rendering comleted!')