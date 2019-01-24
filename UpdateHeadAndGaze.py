# ================== UpdateHeadAndGaze.py ===================
# This function updates the torso, head, and gaze directions
# of the model based on the input spherical coordinates (radians)
# provided in triplet format: radius, theta (elevation), phi (azimuth).
#
#
# 

import bpy


def UpdateHeadAndGaze(BodyRTP, HeadRTP, GazeRTP):

    radius = 1.0                # Set default radius for spherical coordinates to 1m

    BodyBase = bpy.data.objects["Root"]
    HeadBone = bpy.data.objects["HeaDRig"].pose.bones["HeadTracker"]
    GazeBone = bpy.data.objects["HeaDRig"].pose.bones["EyesTracker"]

    #====== Convert spherical coordinates to Cartesian
    HeadYXZ = sph2cart(HeadRTP)
    GazeXYZ = sph2cart(GazeRTP)

    #====== Apply rotations to bones by translating their targets
    BodyBase.rotation_euler = [BodyRTP[1], 0, BodyRTP[2]]
    HeadBone.location = HeadXYZ
    GazeBone.location = GazeXYZ

