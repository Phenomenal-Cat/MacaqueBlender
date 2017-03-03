
# AddTargetObjects.py


SphereDiam  = 0.04

for sph in SphereLocs
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions    = 100,
        size            = SphereDiam
        calc_uvs        = False
        view_align      = False
        enter_editmode  = False
        location        = SphereLoc[sp]
        rotation        = (0,0,0))
    bpy.
    
    
    