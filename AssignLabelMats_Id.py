
#=================== AssignLabelMats_Id.py ======================
# This script assigns a different color material to each part of 
# the avatar's face and body and sets the scene to render flat 
# (i.e shaderless) as an indexed image. The rendered images can 
# be used for analysis of subject's gaze during free viewing of 
# the full color stimulus.


import bpy

#========== Set vertex group and fur material assignments
AllColors       = [[0,0,0.3],[0,0,1],[0,1,1],[0,1,0],[0.5,1,0],[1,1,0],[1,0.5,0],[1,0,0],[0.3,0,0]]
AllLabels       = ["Eyes","InnerEye","OuterEye","Head","Ears","Body","Nose","OuterMouth","InnerMouth"]
AllIndices      = [1,2,3,4,5,6,7,8,9]

HeadObj         = bpy.data.objects["AverageMesh_N=23.001"]
NonFaceObjs     = [["CorneaL", "CorneaR"], ["BodyZremesh2"]]
NonFaceNames    = ["Eyes","Body"]
NonFaceIndx     = [0,5]

MatNames        = ["Head","Ears","InnerEye","OuterEye","Nose","OuterMouth","InnerMouth"]
VertGrpNames    = [["cou"],["oreillefur"],["24846", "6523"],["5405"], ["32211"], ["42027"],["49904"]]                           
GrpIndx         = [3, 4, 1, 2, 6, 7, 8]

AllMats         = [mat for mat in bpy.data.materials if mat.name.startswith("Label_")]                      # Check whether label materials exist
FurGroups       = [["HeadHair","EyeBrows"], ["Ears"], ["EyeLashes"],[],[],["Mouth", "UpperLip"]]
FurGrpIndx      = [[3,3], [4], [1], [], [], [7,7]]
ParticleIndx    = [[0, 4], [6], [5], [], [], [7,2]]

#========== Hide short face hair
TurnOffFur      = ["ParticleSystem 4"]
for t in range(0, len(TurnOffFur)):
    HeadObj.modifiers[TurnOffFur[t]].show_render = False
    HeadObj.modifiers[TurnOffFur[t]].show_viewport = False

#========== Create all new label materials
for m in range(0,len(AllColors)):
    MatName                     = "Label_%s" % AllLabels[m]                                 # Get material name
    if not MatName in bpy.data.materials:                                                   # If material doesn't exist
        mat                         = bpy.data.materials.new(MatName)                       # Create new material
        mat.emit                    = 1                                                     # Set material emission value
        mat.diffuse_color           = AllColors[m]                                          # Set material color
        mat.specular_intensity      = 0                                                     # Set intensity of specular reflection (0-1)
        mat.pass_index              = AllIndices[m]                                         # Set Material Index
    else:
        mat = bpy.data.materials[MatName]                                                   # Get material handle
        
#========== Assign materials to non-face objects
for m in range(0, len(NonFaceObjs)):
    MatName   = "Label_%s" % AllLabels[NonFaceIndx[m]]
    mat       = bpy.data.materials[MatName]
    for ob in range(0, len(NonFaceObjs[m])):                                        # For each object in part group
        CurrentObj = bpy.data.objects[NonFaceObjs[m][ob]]
        bpy.context.scene.objects.active = CurrentObj                               # Select object
        CurrentObj.hide            = False
        CurrentObj.select          = True
        bpy.ops.object.mode_set(mode='EDIT')                                        # Ender edit mode
        bpy.ops.object.mode_set(mode='EDIT')                                        # Ender edit mode
        CurrentObj.data.materials.append(mat)                                       # Add material to object
        CurrentObj.active_material  = bpy.data.materials[MatName]
        bpy.ops.mesh.select_all(action='SELECT')                                    # Select all of mesh
        bpy.ops.object.material_slot_assign()                                       # Assign material to selection
        CurrentObj.select           = False                                         # Deselect object

#========== Assign materials to body fur
CurrentObj = NonFaceObjs[1][0]
bpy.context.scene.objects.active    = bpy.data.objects[CurrentObj]
bpy.data.particles[1].material_slot = "Label_Body"

#========== Add material slots to head object
bpy.context.scene.objects.active = HeadObj
#HeadObj.active_material  = bpy.data.materials['Label_Head']     # <<< Experimental
if all(AllMats):
    for m in range(0,len(VertGrpNames)):
        mat                         = bpy.data.materials.new("Label_%s" % MatNames[m])  # Create new material
        mat.emit                    = 1                                                 # Set material emission value
        mat.diffuse_color           = AllColors[GrpIndx[m]]                             # Set material color
        mat.specular_intensity      = 0                                                 # Set intensity of specular reflection (0-1)
        mat.pass_index              = AllIndices[GrpIndx[m]]                            # Set material pass index
        if "Label_%s" % AllLabels[GrpIndx[m]] in HeadObj.data.materials:                # If material is not assigned to object
            print("Material %s exists" % AllLabels[GrpIndx[m]])
        else:
            HeadObj.data.materials.append(mat)                                          # Add material to object
                
elif not(all(AllMats)):
    mat = AllMats[0]
    
#========== Assign materials to vertex groups
bpy.ops.object.mode_set(mode='EDIT')                                                    # Ender edit mode
bpy.ops.object.mode_set(mode='EDIT')  
for m in range(0, len(VertGrpNames)):
    bpy.ops.mesh.select_all(action='DESELECT')                                             
    #bpy.ops.object.material_slot_select("Label_%s" % MatNames[m])                      # Select current material
    HeadObj.active_material_index = m+3                                                 # Skip the pre-existing materials (skin, fur, eyelash)
    for v in range(len(VertGrpNames[m])):
        bpy.ops.object.vertex_group_set_active(group=VertGrpNames[m][v])                # Make vertex group active
        bpy.ops.object.vertex_group_select()                                            # Assign material to vertex group
        bpy.ops.object.material_slot_assign()                                           # Assign material to vertex group

    #HeadObj.particle_systems[FurGroups[m]]                                             # Get corresponding pasrticle system
    
#========== Assign materials to particle systems
for f in range(len(FurGroups)):
    for m in range(len(FurGroups[f])):
        for ma in bpy.data.materials:
            if ma.name.startswith("Label_%s" % AllLabels[FurGrpIndx[f][m]]):
                mat = ma.name
                matindx = bpy.data.materials[:].index(bpy.data.materials[ma.name])
        #bpy.data.particles[FurGrpIndx[m][f]].material_slot = mat                        # REMOVED > Assign material to particles
        bpy.data.particles[ParticleIndx[f][m]].material_slot = mat

bpy.data.scenes['Scene'].render.layers['RenderLayer'].use_pass_material_index = True    # Turn on material index pass rendering
bpy.data.scenes['Scene'].render.image_settings.file_format = 'OPEN_EXR'


