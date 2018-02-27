"""============================ MorphVertices.py ==================================
This script updates the coordinates of all vertices in the specified mesh to match 
the specified weighted average of two or more meshes.

06/21/2017 - Writen by APM
"""

import bpy
from mathutils import Vector, Matrix

#==================== Calculate vertex destinations
Proportion = 0.5                            # Proportion mix between mesh A and mesh B


#==================== Get vertex data
obj     = bpy.data.objects['Cube1']         # Handle to mesh object
mesh    = obj.data                          # mesh data
vert    = mesh.vertices[0]                  # Vertex 1


mat_world = obj.matrix_world
vec      = Vector((0.0, 0.0, 0.1))  
mat_edit = mat_world.inverted() * Matrix.Translate(vec) * mat_world
vert.co  = mat_edit * vert.co
