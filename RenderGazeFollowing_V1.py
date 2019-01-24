
#========================== RenderGazeFollowing_V1.py =============================
# 
#===================================================================================


import bpy
import sys
import math
import random
import numpy as np
from InitBlendScene import InitBlendScene
from GetOSpath import GetOSpath
from AddTargetObjects import AddTargetObjects

SetupGeometry   = 2 
StereoFormat    = 1 
ViewingDistance = 97


InitBlendScene(SetupGeometry, StereoFormat, ViewingDistance)
AddTargetObjects()


