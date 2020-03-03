# **A Python library for parametric control of a 3D rigged macaque face model for visual and social neuroscience**
<img src= "https://user-images.githubusercontent.com/7523776/29430545-cbc198b0-8362-11e7-9826-5d5629ab22f4.gif" width="300" height="300" /> <img src= "https://user-images.githubusercontent.com/7523776/29431817-4fb301dc-8367-11e7-9e3c-4612c579d214.gif" width="300" height="300" /> 

This repository contains Python code for automated control of a Blender (www.blender.org) file containing a fully rigged, realistic 3-dimensional Rhesus macaque avatar, as described in [Murphy & Leopold, 2019](https://doi.org/10.1016/j.jneumeth.2019.06.001). The mesh surfaces were generated from CT scans of live anesthetized Rhesus macaques, and edited in collaboration with a professional CGI artist (<a href="https://www.artstation.com/ishoop">Julien Duchemin</a>). The code allows quick setup of viewing geometry to match the experimental context, parametric manipulation of body, head and gaze direction, facial expression, facial identity, skin and fur appearance, environment variables, and offline rendering of images and animations using the Cycles engine. Continuous morphing of facial identity is acheived based on an empirically-defined PCA "face-space" representation.

<img src= "https://user-images.githubusercontent.com/7523776/29434998-237ade62-8373-11e7-81b7-451fde4ba5b8.png" width="850" height="500" />

The following parameters of the model can be varied continuously:
* Body position and orientation (Cartesian coordinates relative to world origin)
* Head orientation (spherical coordinates relative to body)
* Gaze direction (spherical coordinates relative to head) + eye vergence angle (determined automatically for gaze target distance)
* Pupil dilation and blinks
* Blend shapes for stereotypical facial expressions (besdides the default 'neutral'):
  1) open-mouthed threat (aggressive)
  2) bared teeth display (submissive or fearful)
  3) pursed-lips /coo vocalization (affiliative)
  4) lip-smack (affiliative)
  5) yawn (anxious)
  6) chewing (ingestive)
  7) tongue protrusion (disgust)
* Additional independent control of brow, ears, and jaw movement.
* Fur length, density, color, texture map
* Skin color, material reflectance (including sub-surface scattering), and texture
* Lighting direction, intensity, color, and type

# Access
Please note that the .Blend files are not yet in the public domain. Pre-rendered stimulus sets containing a large quantity of high quality static and animated renders can be downloaded from [Figshare.com](https://figshare.com/projects/MF3D_Release_1_A_visual_stimulus_set_of_parametrically_controlled_CGI_macaque_faces_for_research/64544) and further details are provided on the [MF3D-Tools](https://github.com/MonkeyGone2Heaven/MF3D-Tools) repository.
