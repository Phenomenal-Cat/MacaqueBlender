
#============================= LoadVocalParams.py =============================
# This script loads video and audio data, as well as extracted motion timecourses
# that are used to animate bone movements of teh avatar.

# import scipy.io
import bpy
import os
import mathutils as mu
import math

Prefix              = 'P:/'
MovieName           = 'BE_scream_mov59'
MovieFormat         = '.mpg'
MovieDir            = Prefix + 'murphya/MacaqueFace3D/Macaque_video/Originals/'
MatFile             = Prefix + 'murphya/MacaqueFace3D/Macaque_video/'

AudioChannel        = 1;
AudioStartFrame     = 1;
MovieFPS            = 25;
MovieNoFrames       = 20;

# mat = scipy.io.loadmat(MatFile)

#============== Load reference movie to 3D plane
MovieFile = MovieDir + MovieName + MovieFormat
mc = bpy.data.movieclips.load(MovieFile)
bpy.ops.import_image.to_plane(files=[{'name': os.path.basename(MovieFile)}],
        directory=os.path.dirname(MovieFile))
bpy.data.objects[MovieName].rotation_euler  = mu.Vector((math.radians(90), 0, 0))
bpy.data.objects[MovieName].location        = mu.Vector((-0.2, 0, 0))
bpy.data.objects[MovieName].scale           = ((0.15, 0.15, 0.15))   

#============== Load audio data to sequence
AudioFile = MovieDir + MovieName + '.wav'
sc = bpy.data.sounds.load(AudioFile)
se = bpy.context.scene.sequence_editor_create()
se.sequences.new_sound(MovieName, AudioFile, AudioChannel, AudioStartFrame);


#============== Apply keyframes to blendshapes


