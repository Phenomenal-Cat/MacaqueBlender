
# Caclulate vertex differences for each expression mesh

import bpy


ExpNames        = ['Threat','fearx','smack']
NeutralMesh     = bpy.data.objects['MacaqueHeadNG_1expressionsNeutral']
TargetMesh      = bpy.data.objects['AverageMesh_N=23']

#for exp in range(0, 1):#len(ExpNames)):
    
exp = 0

NeutralVerts    = NeutralMesh.data.vertices
ExpVerts        = bpy.data.objects['MacaqueHeadNG_1expressions' + ExpNames[exp]].data.vertices
new_obj         = TargetMesh.copy()                             # Create a copy of the target mesh
new_obj.name    = TargetMesh.name + '_' + ExpNames[exp]
new_obj.data    = TargetMesh.data.copy()                        
TargetVerts     = new_obj.data.vertices                         

VertDiffs       = [[]]
print('Neutral verts    = ' + str(len(NeutralVerts)))
print('Target verts     = ' + str(len(TargetVerts)))
for v in range(0, len(NeutralVerts)):                               # For each vertex...
    if v == 0:
        VertDiffs[0]        = NeutralVerts[v].co - ExpVerts[v].co   # Calculate offset distance
    else:
        VertDiffs.append( NeutralVerts[v].co - ExpVerts[v].co )
        
    TargetVerts[v].co   = TargetVerts[v].co + VertDiffs[v]      # Apply this offset to the target mesh

bpy.context.scene.objects.link(new_obj)

bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
TargetMesh.data.vertices[0].select = True
NeutralMesh.data.vertices[0].select = True
bpy.ops.object.mode_set(mode = 'EDIT') 




