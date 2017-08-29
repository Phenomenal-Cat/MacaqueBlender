
"""===================== GenerateLightArray.py ======================
This function is used to initialize an array of lamp objects in the scene.
By default, all lamps are splotlights pointed at the world origin and are
initially turned off.


@author: aidanmurphy (murphyap@mail.nih.gov)
"""

import bpy
import numpy as np
import mathutils as mu
import math


def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz, np.zeros(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2])  # for elevation angle defined from Z-axis down
    #ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew


def GenerateLightArray(LampType='SPOT', LampArrangement='hemi'):
    
    # LampType = 'POINT'; 'SUN'; 'SPOT'; 'HEMI'; 
    # LampArrangement = 'circle'; 'hemi'; 'sphere'
    # 
    
    #=============== Set lamp array parameters
    FlipArray           = 1                     # 0 = pole is Y-axis; 1 = pole is Z-axis          
    LampNoAzAngles      = 8                     # Default number of azimuth angles
    LampNoElAngles      = 3                     # Default number of elevation angles
    LampArrayRadius     = 1.5                   # Radius of array of lamps
    LampCircleHeight    = 1                     # Lamp height (meters) for circular lamp arrangement

    #=============== Generate spherical coordinates for each lamp
    if LampArrangement == 'circle':
        LampAzAngles        = np.linspace(0,2*math.pi, LampNoAzAngles+1)
        LampElAngles        = np.tile(math.atan(LampCircleHeight/LampArrayRadius), 3)
        
    elif LampArrangement == 'sphere':
        LampAzAngles        = np.linspace(0,2*math.pi, LampNoAzAngles+1)
        LampElAngles        = np.linspace(0,math.pi, LampNoElAngles+2)
        
    elif LampArrangement == 'hemi':
        LampAzAngles        = np.linspace(0,2*math.pi, LampNoAzAngles+1)
        LampElAngles        = np.linspace(0,math.pi, LampNoElAngles+2)
        LampElAngles        = LampElAngles[:-np.floor(LampNoElAngles/2)] 
        
    LampAzAngles = LampAzAngles[:-1]                # Remove last angle from list (2*pi == 0)
    LampElAngles = LampElAngles[1:-1]               # Remove first and last angle from list

    #============== Loop through array locations
    LampLocs   = np.zeros((LampNoAzAngles*LampNoElAngles,3))
    LampRot    = np.zeros((LampNoAzAngles*LampNoElAngles,3))
    LampObjects = {}
    li = 0
    for el in LampElAngles:

        for az in LampAzAngles:

            LampLocs[li][0] = LampArrayRadius*math.sin(el)*math.sin(az)
            LampLocs[li][1] = LampArrayRadius*math.sin(el)*math.cos(az)
            LampLocs[li][2] = LampArrayRadius*math.cos(el)
            LampRot[li][0] = -el
            LampRot[li][1] = 0
            LampRot[li][2] = -az
            if FlipArray == 1:
                LampLocs[li] = [LampLocs[li][i] for i in [0,2,1]]
                LampRot[li]  = [LampRot[li][i] for i in [0,2,1]]
                LampLocs[li][1] = -LampLocs[li][1]
                LampRot[li][1] = -LampRot[li][1]
                LampRot[li][0] = -LampRot[li][0]
            
            #============== Add lamp
            lamp_data       = bpy.data.lamps.new(name='Lamp_%d' % (li), type=LampType)  # Create new lamp data block
            lamp_object     = bpy.data.objects.new(name='Lamp_%d' % (li), object_data=lamp_data)    # Create new lamp
            bpy.data.scenes[0].objects.link(lamp_object)                                      # Link new lamp to scene
            
            lamp_object.location        = mu.Vector((LampLocs[li]))                                 # Position lamp
            lamp_object.rotation_euler  = mu.Vector((LampRot[li]))                                  # Rotate lamp
            lamp_object.hide_render     = True                                                      # Turn lamp off by default
            print('Lamp %d of %d added to scene...' % (li+1, LampNoAzAngles*LampNoElAngles))       
            LampObjects[li] = lamp_object            
            li = li+1;
    return LampObjects
  
  