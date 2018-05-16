
#============= GenerateFaceVoiceMovies.py

import bpy
import mathutils
import math
import numpy
import socket

Identity    = "BE"
CallTypes   = ["Coo","Pantthreat","Scream"]
VideoDir    = '/Users/murphyap/Documents/Macaque_video/Originals/';
AudioDir    = '/Users/murphyap/Documents/Macaque_video/FaceVoiceIntegration/WAV_files/';
OutputDir   = '/Users/murphyap/Documents/Macaque_video/FaceVoiceIntegration/Combined/';
VideoInFormat   = 'mpg'
VideoOutFormat  = 'mp4'
FrameRate       = 29.97

S  = bpy.context.scene
se = bpy.context.scene.sequence_editor_create()

S.render.image_settings.file_format = 'H264'              # Set render format
S.render.ffmpeg.audio_codec         = 'MP3'                 
S.render.ffmpeg.format              = 'MPEG4'

#============= Loop through stimulus conditions
for v in CallTypes:
    
    movieFilePath = VideoDir + "%s_%s_mov52.%s" % (Identity, v, VideoInFormat)
    mc = bpy.data.movieclips.load( movieFilePath )

    #======= Set output parameters to match video clip
    S.render.resolution_x           = mc.size[0]
    S.render.resolution_y           = mc.size[1]
    S.render.resolution_percentage  = 100
    S.render.fps                    = FrameRate
    S.render.fps_base               = 1.0
    S.frame_start                   = 0
    S.frame_end                     = mc.frame_duration 

    se.sequences.new_clip("VideoClip", mc, 0, 0)                        # Load video clip to sequencer

    aindx = 2
    for a in CallTypes:                                                 
        audioFilePath = AudioDir + "V_%s_%s_A_%s_%s.wav" % (Identity, v, Identity, a)
        ac = bpy.data.sounds.load(audioFilePath)
        AudioClipName = "%s_%s" % (Identity, a)
        se.sequences.new_sound(AudioClipName, audioFilePath, aindx, 0)  # Load audio file
        se.sequences_all[AudioClipName].pitch     = 1;                  # Set relative pitch
        se.sequences_all[AudioClipName].volume    = 1;                  # Set volume
        se.sequences_all[AudioClipName].pan       = 0;                  # Set left-right balance
        
        S.render.filepath   = OutputDir + "V_%s_%s_A_%s_%s" % (Identity, v, Identity, a)                     # Set output filename
        bpy.ops.render.render( animation = True, write_still = True)    # Render animation 
        
        se.sequences_all['VideoClip'].select = True                     # Select video track
        se.sequences_all[AudioClipName].select = False                  # Deselect last audio clip
        bpy.ops.sequencer.mute(unselected=True)                         # Mute unselected udio track
        # bpy.ops.sequencer.mute(unselected=False)                      # Mute selected tracks
        aindx = aindx+1                                                 

        