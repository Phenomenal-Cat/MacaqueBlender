
#============================= LoadVocalParams.py =============================


import scipy.io
import bpy
import os
import math

MovieName   = 'BE_coo_mov52'
MovieDir    = '/Users/murphyap/Documents/Macaque_video/Originals/'
MatFile     = '/Volumes/projects/murphya/MacaqueFace3D/Macaque_video/'

mat = scipy.io.loadmat(MatFile)

#============== Load reference movie to 3D plane
MovieFile = MovieDir + MovieName + '.mpg'
bpy.ops.import_image.to_plane(files=[{'name': os.path.basename(MovieFile)}],
        directory=os.path.dirname(MovieFile))
bpy.data.objects[MovieName].rotation_euler  = math.vector(math.rad(90), 0, 0)
bpy.data.objects[MovieName].location        = math.vector(-0.2, 0, 0)
bpy.data.objects[MovieName].scale           = ((0.15, 0.15, 0.15))   

#============== Load audio data to sequence


#============== Apply keyframes to blendshapes




#======= Set primary expression
#bpy.ops.object.mode_set(mode='POSE')
head.pose.bones['yawn'].location    = mu.Vector((0,0,0.02*ExpWeights[exp,3]))           # Wide mouthed 'yawn' expression
head.pose.bones['Kiss'].location    = mu.Vector((0,0.02*ExpWeights[exp,2],0))           # Pursed lip 'coo' expression
head.pose.bones['jaw'].location     = mu.Vector((0,0,0.02*ExpWeights[exp,1]))           # Open-mouthed 'threat' expression
head.pose.bones['Fear'].location    = mu.Vector((0,-0.02*ExpWeights[exp,0],0))          # Bared-teeth 'fear' grimace

#======= Set micro expression
head.pose.bones['blink'].location   = mu.Vector((0,0,0.007*ExpMicroWeights[mexp, 0]))   # Close eye lids (blink)
head.pose.bones['ears'].location    = mu.Vector((0,0.04*ExpMicroWeights[mexp, 1],0))    # Retract ears
head.pose.bones['eyebrow'].location = mu.Vector((0,0,-0.02*ExpMicroWeights[mexp, 2]))   # Raise brow
head.pose.bones['EyesTracker'].scale = mu.Vector((0, 1*ExpMicroWeights[mexp, 3], 0))    # Pupil dilation/ constriction

