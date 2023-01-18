# -*- coding: utf-8-

import bpy
import mathutils as mu
import math
import numpy as np
import socket
import sys
# import InitBlendScene



#============== Update head angle
def HeadLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*-Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    HeadXYZ = mu.Vector((X, Y, Z))
    return HeadXYZ

def GazeLookAt(El, Az):
    Rad = 1
    Z   = np.cos(math.radians(Az))*np.cos(math.radians(El))*Rad
    X   = np.sin(math.radians(Az))*np.cos(math.radians(El))*Rad
    Y   = np.sin(math.radians(El))*Rad
    GazeXYZ = mu.Vector((X, Y, Z))
    return GazeXYZ   

def ScalePCweights(Weights, Distance):
    
    
    

    return ScaledWeights
    
#sys.path.append(BlenderDir)
SetupGeometry       = 3                                                 # Specify which physical setup stimuli will be presented in
StereoFormat        = 0                                                 # Specify the stereoscopic format to render
#InitBlend(SetupGeometry, StereoFormat)                                  # Initialize the Blender scene to meet requirements


#============ Set craniofacial geometry parameters                        
HeadElAngles        = [0]                                                   # Set elevation angles (degrees)
HeadAzAngles        = np.linspace(-50, 50, 21)                              # Set azimuth angles (degrees)
NoIdentities        = 15
NoPCs               = 5                                                     # How many PCs to use
DistintivenessSD    = 3
Value1inSDs         = 3                                                   # How many SDs does shape key value '1' equal?                         
PCSum               = np.square(DistintivenessSD/Value1inSDs)               # Convert SDs to corresponding shape key values

#============ Set facial texture parameters
Headers         = ['MatDesc','MatName','NodeName','Index','Default','Lims']
MaterialData    = [('Skin redness','Faceskin','Mix Shader.001',0, 0.682, [0,1])]
MaterialData.append(('Skin gloss', 'Faceskin','Mix Shader.003', 0, 0.05, [0,0.15]))
#MaterialData.append(('Skin wrinkles','Faceskin','Math.002',0, 0.07, [0,0.1]))
MaterialData.append(('Skin wrinkles scale', 'Faceskin', 'Displacement',2, 0.3, [0.2, 1]))
MaterialData.append(('Face fur hue', 'furface', 'Hue Saturation Value', 0, 0.5, [0.48, 0.52]))
MaterialData.append(('Face fur sat', 'furface', 'Hue Saturation Value', 1, 1, [0.5, 1.5]))
MaterialData.append(('Body fur hue', 'furbody.001', 'Hue Saturation Value', 0, 0.5, [0.48, 0.52]))
MaterialData.append(('Body fur sat', 'furbody.001', 'Hue Saturation Value', 1, 1, [0.5, 1.5]))
MaterialData.append(('Eye color','Sclera_and_Iris', 'Hue Saturation Value', 0, 0.5, [0.5, 0.5]))
MaterialData.append(('Eye saturation', 'Sclera_and_Iris', 'Hue Saturation Value', 1, 1, [1, 1]))
NewValues    = [[]]


#========== Generate random identity trajectories in face-space and then scale
#IdentityPCs     = np.zeros([NoIdentities, NoPCs])
#IdentityPCs     = (np.random.rand(*IdentityPCs.shape)*2)-1

IdentityPCs = np.array([[1,0,0,0,0],
               [0.71,0.71,0,0,0],
               [0,1,0,0,0],
               [-0.71,0.71,0,0,0],
               [-1,0,0,0,0],
               [-0.71,-0.71,0,0,0],
               [0,-1,0,0,0],
               [0.71,-0.71,0,0,0],
               [0,1,0,0,0],
               [0,0.71,0.71,0,0],
               [0,0,1,0,0],
               [0,-0.71,0.71,0,0],
               [0,-1,0,0,0],
               [0,-0.71,-0.71,0,0],
               [0,0,-1,0,0],
               [0,0.71,-0.71,0,0]])
 
for id in range(0, NoIdentities):
    ScaleFactor = PCSum / np.sum(np.square(IdentityPCs[id]))
    IdentityPCs[id] = IdentityPCs[id]*np.sqrt(ScaleFactor)


#print(IdentityPCs)

#Distances       = [-20, 0, 20]                                         # Set object distance from origin (centimeters)
NoConditions    = (len(HeadElAngles)+len(HeadAzAngles))*NoIdentities    # Calculate total number of conditions                   
    
    
head            = bpy.data.objects["AverageMesh_N=23.001"]
headRig         = bpy.data.objects["HeaDRig"]
PC              = np.array([0,1,2])
#for pc in range(0, NoPCs):
#    print('PC %d\n' % pc)
#    PC[pc] = head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)]

#bpy.ops.object.mode_set(mode='POSE')
bpy.context.scene.render.image_settings.file_format = 'PNG'

SetFrameIndx = 0

#================ Loop through idnetities
for id in range(0, NoIdentities):
    
    # Set all 10 PC values for current identity
    for pc in range(0, len(IdentityPCs[0])):      
        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].value = IdentityPCs[id][pc]
        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value",  frame=SetFrameIndx)
        head.data.shape_keys.key_blocks["PCA_N=23__shape_PC%d_sd3" % (pc+1)].keyframe_insert("value",  frame=SetFrameIndx+len(HeadAzAngles)-1)

    # Set all texture values for current identity
    NewValues = []
    for m in range(0, len(MaterialData)):
        Mat = MaterialData[m]
        if (Mat[0] == 'Face fur hue'):
            FaceFurHueIndx = m
        elif (Mat[0] == 'Face fur sat'):
            FaceFurSatIndx = m
        if (Mat[0] == 'Body fur hue'):
            NewValues.append(NewValues[FaceFurHueIndx])
        elif (Mat[0] == 'Body fur sat'):
            NewValues.append(NewValues[FaceFurSatIndx])
        else: 
            NewValues.append(np.random.uniform(low=Mat[5][0], high=Mat[5][1]))
            
        bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].default_value = NewValues[m]
        bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].keyframe_insert('default_value', frame=SetFrameIndx)
        bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].keyframe_insert('default_value', frame=SetFrameIndx+len(HeadAzAngles)-1)

    print(NewValues)

    #======= Loop through head / eye oreitnations
    for Hel in HeadElAngles:
        for Haz in HeadAzAngles:
            
            HeadXYZ = HeadLookAt(Hel, Haz)
            headRig.pose.bones['HeadTracker'].location = HeadXYZ + headRig.location
            headRig.pose.bones['HeadTracker'].keyframe_insert(data_path="location", frame=SetFrameIndx)
                    
        
            #======= Insert keyframe
            print("Setting keyframe %d...\n" % SetFrameIndx)
            bpy.context.scene.frame_set(SetFrameIndx) 
            #headRig.pose.bones['HeadTracker'].location = HeadXYZ + headRig.location
            #headRig.pose.bones['HeadTracker'].keyframe_insert(data_path="location")  
            #headRig.pose.bones['EyesTracker'].location = GazeXYZ + mu.Vector((0, 0.16 + HeadXYZ[1] + headRig.location[1] + BlinkCorrect, 0))
            #headRig.pose.bones['EyesTracker'].keyframe_insert(data_path="location", index=-1)  
            SetFrameIndx = SetFrameIndx+1
                                    
print("Keyframe animation complete!\n")