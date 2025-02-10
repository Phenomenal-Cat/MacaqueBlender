import bpy
import numpy as np
import csv
import os

#============ Load facial texture parameters from file
Dir = '/Volumes/NIFVAULT/projects/murphyap_NIF/NIF_Code/MacaqueBlender/MF3D_R1'
csvfile = os.path.join(Dir, 'TextureParams.csv')
with open(csvfile, newline='', encoding="utf-8-sig") as csvfile:
    reader          = csv.reader(csvfile,  delimiter=',', quotechar='|')
    MaterialData    = list(reader)
    
#===== Find parameter groups
Headers         = MaterialData.pop(0)
ParamCol        = Headers.index('ParamName')
ParamList       = [i[ParamCol] for i in  MaterialData]
ParamNames      = list(set(ParamList))
ParamIndx       = [[]]
for p in range(0, len(ParamNames)):
    ParamIndx[p]    = []
    ParamIndx[p]    = [i for i, x in enumerate(ParamList) if x == ParamNames[p]]






Head = bpy.data.objects["MacaqueHeadNG_1expressions1"]
Body = bpy.data.objects["BodyZremesh2"]

HeadHair    = Head.particle_systems['poilbase']
HairLength  = bpy.data.particles["ParticleSettings.003"].hair_length


NoLevels    = 5
FrameIndx   = 1
NewValues   = []


# For each Parameter group....
for p in range(0, len(ParamNames)):
    Materials = MaterialData[ParamIndx[p]]

    # For each material....
    for m in range(0, len(Materials)):
        Mat         = MaterialData[ParamIndx[p][m]]
        ParamRange  = Mat[5]
        ParamValues = np.linspace(ParamRange[0], ParamRange[1], NoLevels)
        

        for p in range(0, NoLevels):        # For each value...
        
            #if (Mat[0] == 'Face fur hue'):
            #    FaceFurHueIndx = m
            #elif (Mat[0] == 'Face fur sat'):
            #    FaceFurSatIndx = m
                
            #if (Mat[0] == 'Body fur hue'):
            #    NewValues.append(NewValues[FaceFurHueIndx])
            #elif (Mat[0] == 'Body fur sat'):
            #    NewValues.append(NewValues[FaceFurSatIndx])
            #else: 
            #    NewValues.append(np.random.uniform(low=Mat[5][0], high=Mat[5][1]))
            
            bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].default_value = ParamValues[p]
            bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].keyframe_insert('default_value', frame=FrameIndx)
            #bpy.data.materials[Mat[1]].node_tree.nodes[Mat[2]].inputs[Mat[3]].keyframe_insert('default_value', frame=FrameIndx+len(HeadAzAngles)-1)
            FrameIndx = FrameIndx+1



print(NewValues)