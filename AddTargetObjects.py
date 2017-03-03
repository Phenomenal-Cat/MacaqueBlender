
#======= AddTargetObjects.py


SphereDiam  = 0.04
SphereLocs  = [(-0.2,0,0),(0,0.2,0),(0.2,0,0),(0,-0.2,0)];
SphereNum   = [0,1,2,3]

for sph in SphereNum:
    print(SphereLoc[sph])
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions    = 100,
        size            = SphereDiam,
        calc_uvs        = False,
        view_align      = False,
        enter_editmode  = False,
        location        = SphereLoc[sph],
        rotation        = (0,0,0))
    #bpy.data.objects['Icosphere'].name = print("Target %d" % sph)    # Rename sphere as target ID
        
    
    
    