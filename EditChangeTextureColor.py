#ChangeTextureColor
import bpy

#Load Image for Texture and Give Name
ImageFile = "/Volumes/PROJECTS/esche/MacaqueBlender/textures/faceskinRed2.jpg" #Selects image
img = bpy.data.images.load(ImageFile)
#bpy.ops.material.new()  #Create new material 
NewMat = bpy.data.materials.new(name = "OrigText") #Create and name new material
#NewMat = bpy.data.materials[-1]
#NewMat.name = "OrigText"

#Load Node Types
NewMat.use_nodes = True 
#nodes = NewMat.node_tree.nodes
TextNode = NewMat.node_tree.nodes.new("ShaderNodeTexImage")
TextNode.image = img
diffuse1 = NewMat.node_tree.nodes.new(type = 'ShaderNodeBsdfDiffuse')
diffuse2 = NewMat.node_tree.nodes.new(type = 'ShaderNodeBsdfDiffuse')
bright = NewMat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
outmat = NewMat.node_tree.nodes.new(type = 'ShaderNodeOutputMaterial')
rgb = NewMat.node_tree.nodes.new(type = 'ShaderNodeRGB')
huesat = NewMat.node_tree.nodes.new(type = 'ShaderNodeHueSaturation')
mxshade = NewMat.node_tree.nodes.new(type = 'ShaderNodeMixShader')

#Top portion of tree
NewMat.node_tree.links.new(TextNode.outputs['Color'], bright.inputs['Color'])
NewMat.node_tree.links.new(bright.outputs['Color'], diffuse1.inputs['Color'])
NewMat.node_tree.links.new(diffuse1.outputs['BSDF'], mxshade.inputs[1])
NewMat.node_tree.links.new(mxshade.outputs['Shader'], outmat.inputs['Surface'])

#Bottom portion of tree
NewMat.node_tree.links.new(rgb.outputs['Color'], huesat.inputs['Color'])
NewMat.node_tree.links.new(huesat.outputs['Color'], diffuse2.inputs['Color'])
NewMat.node_tree.links.new(diffuse2.outputs['BSDF'], mxshade.inputs[2])

#Parameters
huesat.inputs['Saturation'].default_value = 0.5
huesat.inputs['Hue'].default_value = 0.5
huesat.inputs['Value'].default_value = 0.5

