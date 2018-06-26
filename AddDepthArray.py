
#=============================== AddDepthArray.py ==================================
# This script adds a pseudo-randomized array of the specified reference objects 
# to a scene in a tunnel-like configuration aligned to the camera's optical axis
# and avoiding occlusion of the central target object(s). This provides a relative 
# binocular disparity reference-frame for stereoscopic rendering of target objects
# without surrounding scene elements, and is important for enhancing psychophysical
# perception of depth.
#
#===================================================================================


import bpy
import sys
import math
import random
import numpy as np
from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath

np.random.seed(0)                                               # Seed numpy's random number generator

IsDefault = 0
if IsDefault==1:
    bpy.data.objects["Camera"].location         =  [0,-1,0]
    bpy.data.objects["Camera"].rotation_euler   = [math.pi/2,0,0]
    bpy.data.objects["Cube"].scale              = [0.1, 0.1, 0.1]
    bpy.data.objects["Cube"].rotation_euler     = [math.pi/4,math.pi/6,math.pi/4]

InitBlendScene(2,1)                 # Initialize scene geomerty
Prefix = GetOSpath()                # Get OS-specific path

#============ Set reference object parameters
RefFrustumNear      = 0.2           # Near clipping-plane for reference objects (metres from world origin)
RefFrustumFar       = 0.2           # Far clipping-plane for reference objects (metres from world origin)
RefFrustumWidth     = 0.5           # Proportion of camera frustum width to fill with reference objects (0-1)
RefFrustumHeight    = 0.3           # Proportion of camera frustum height to fill with reference objects (0-1)
RefObjType          = 'ObjFile'      
RefObjLayout        = 'Grid'        # 'Grid': 3D-grid layout; 'Plane': 2D plane of screen
RefObjColor         = 'random'      # Randomize reference object's color?
RefObjOrient        = 'random'      # Randomize reference object's orientations?
RefObjBW            = 1             # Make reference object colors black and white?
RefObjSize          = []            # Randomize reference object's size?
RefObjRadius        = 0.01          # Scaling to apply to objects
RefObjDensity       = 0.05          # Approximate proportion of available volume to fill with objects
RefObjFile          = Prefix[0] + 'murphya/MacaqueFace3D/GameRenders/Golf_Ball.obj'            # Full path of mesh to use as reference objects
#RefObjFile          = Prefix + 'murphya/MacaqueFace3D/GameRenders/RubiksCube.obj'

#============ Set reference object material properties
if RefObjBW == 0:
    AllColors           = ((1,0,0),(1,0.5,0),(1,1,0),(0.5,1,0),(0,1,0),(0,1,0.5),(0,1,1),(0,0.5,1),(0,0,1),(1,0,1),(1,1,1))
elif RefObjBW == 1:
    AllColors           = ((0,0,0), (1,1,1))



for m in range(0, len(AllColors)):
    if not ("RefObjMat_%d" % m) in bpy.data.materials:
        Material                         = bpy.data.materials.new("RefObjMat_%d" % m)           # Create new material and name it
        Material.diffuse_color           = AllColors[m]                                         # Set material color
        Material.specular_intensity      = 0.4                                                  # Set intensity of specular reflection (0-1)
        Material.emit                    = 0.0                                                  # Set light emission amount
        Material.use_transparency        = False                                                # Set whether to use alpha transparency
        Material.alpha                   = 1.0                                                  # Set how much alpha transparency
        Material.use_cast_shadows        = False                                                # Set whether to cast shadows
        Material.use_shadows             = True                                                 # Set whether to receive shadows
    

#============ Calculate reference object locations
Scene           = bpy.data.scenes["Scene"]
Cam             = bpy.data.cameras["Camera"]
Cam.lens_unit   = 'FOV'
ThetaX          = Cam.angle/2                                                           # Get angle of half of camera's width of field of view (radians)
ThetaZ          = ThetaX*(Scene.render.resolution_y/Scene.render.resolution_x)
Cam             = bpy.data.objects["Camera"]
CamLoc          = Cam.location                                                          # Get camera distance from origin
MinX            = ((1-RefFrustumWidth)/2)*math.tan(ThetaX)*2*abs(CamLoc[1])             # Calculate minimum distance from origin in X-dimension
MinZ            = ((1-RefFrustumHeight)/2)*math.tan(ThetaZ)*2*abs(CamLoc[1])   
Position        = []
Orientation     = []
Scale           = []
indx            = 0
Spacing         = RefObjRadius*3

if RefObjLayout == 'Grid':
    AllYpos     = np.arange(-RefFrustumNear, RefFrustumFar+Spacing, Spacing)            # Set range of object depths (y-axis)
elif RefObjLayout == 'Plane':
    AllYpos     = [0]
AllXpos     = np.zeros([len(AllYpos),10])                                            
AllZpos     = np.zeros([len(AllYpos),10])         
Xpos        = []
Zpos        = []         
AllPos      = []      
              
for y in range(0, len(AllYpos)):                                                     # For each depth position... 
    MaxX    = abs(math.tan(ThetaX)*(CamLoc[1]-AllYpos[y]))-RefObjRadius*2            # Calculate maximum width offset (X-axis)
    MaxZ    = abs(math.tan(ThetaZ)*(CamLoc[1]-AllYpos[y]))-RefObjRadius*2            # Calculate maximum height offset (Z-axis)
    Xpos    = np.arange(-MaxX, MaxX, Spacing)
    #Xpos    = np.concatenate( (np.arange(-MaxX, -MinX+Spacing, Spacing), np.arange(MinX, MaxX+Spacing, Spacing)), axis=0)
    for x in range(0, len(Xpos)):
        if abs(Xpos[x]) < MinX:
            Zpos    = np.concatenate( (np.arange(-MaxZ, -MinZ+Spacing, Spacing), np.arange(MinZ, MaxZ+Spacing, Spacing)), axis=0)
        elif abs(Xpos[x]) >= MinX:
            Zpos    = np.arange(-MaxZ, MaxZ+Spacing, Spacing)
        
        for z in range(0, len(Zpos)):
            AllPos.append([Xpos[x], AllYpos[y], Zpos[z]])
            indx = indx+1

NoGridSpaces    = len(AllPos)                                                          # Count total number of grid spaces
RefObjNumber    = round(RefObjDensity*NoGridSpaces)                                    # Calculate number of grid spaces to use      
SpacesToUse     = np.random.choice(NoGridSpaces, RefObjNumber, replace=False)          # Select that number of grid spaces at random                                   

print("Depth array added containing %d reference objects (of %d spaces: %d X x %d Z). Spaces to use = %d." % (RefObjNumber, NoGridSpaces, len(Xpos), len(Zpos), len(SpacesToUse)))   

#============ Generate reference objects
for n in range(0, RefObjNumber):

    #========= Append empty lists
    Position.append([])
    Orientation.append([])
    Scale.append([])

    #========= Randomize reference object location
    Ypos = AllPos[SpacesToUse[n]][1]
    Xpos = AllPos[SpacesToUse[n]][0]
    Zpos = AllPos[SpacesToUse[n]][2]

    Position[n].append(Xpos)
    Position[n].append(Ypos)
    Position[n].append(Zpos)

    #========= Randomize reference object orientation?
    if RefObjOrient == 'random':     
        Orientation[n].append(random.uniform(0, 2*math.pi))
        Orientation[n].append(random.uniform(0, 2*math.pi))
        Orientation[n].append(random.uniform(0, 2*math.pi))
    else :
        Orientation[n] = ([0, 0, 0])
        
    #========= Randomize reference object material?
    if RefObjColor == 'random':     
        MatIndx     = np.random.randint(len(AllColors), size=1)
        RefObjMat   = bpy.data.materials.get("RefObjMat_%d" % MatIndx[0])       # Select random color/ material
    else :
        RefObjMat =  bpy.data.materials.get("RefObjMat_0") 
            
    #========= Randomize reference object size?
    if RefObjSize == 'random':
        Radius      = []
        Scale[n].append(Radius, Radius, Radius)
    else:
        for d in range(3):
            Scale[n].append(RefObjRadius)


    #========= Create new instance of object and apply 
    if n == 0:
        if RefObjType == 'Sphere':
            #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3)
            #RefObj  = bpy.data.objects['Icosphere']
            
            bpy.ops.mesh.primitive_uv_sphere_add()
            RefObj  = bpy.data.objects['Sphere']
            #mesh    = bpy.data.meshes.new('RefObj 000')
            #RefObj  = bpy.data.objects.new('RefObj 000', mesh)

        elif RefObjType == 'ObjFile':
            Import  = bpy.ops.import_scene.obj(filepath=RefObjFile)             # Import target geometry from '.obj' file
            RefObj  = bpy.context.selected_objects[0]                           # Get RefObj object handle

    elif n > 0:
        RefObj = bpy.data.objects['RefObj 000'].copy()                         # Get handle to first RefObj object
        #RefObj  = bpy.data.objects.new("RefObj %03d" % n, CopyObj)              # Create copy with new name         
        bpy.context.scene.objects.link(RefObj)                                  # Link new object to scene

        
    RefObj.name             = "RefObj %03d" % n                                 # Rename object as RefObj ID
    RefObj.scale            = Scale[n]                                          # Set RefObj size
    RefObj.location         = Position[n]                                       # Set RefObj location
    RefObj.rotation_euler   = Orientation[n]                                    # Set RefObj orientation
    #bpy.ops.object.mode_set(mode='OBJECT')                                      # Enter object mode
    RefObj.active_material              = RefObjMat                             
    RefObj.material_slots[0].link       = 'OBJECT'
    RefObj.material_slots[0].material   = RefObjMat
        
    #RefObj.active_material  = RefObjMat
    #RefObj.active_material  = RefObjMat.copy()                                 # Set RefObj material
    
    #bpy.context.active_object.data.materials[0] = RefObjMat
                                      
print("Depth array added containing %d reference objects (of %d space)." % (RefObjNumber, NoGridSpaces))            