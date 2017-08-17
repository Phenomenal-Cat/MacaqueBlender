# **A Python library for parametric control of a 3D rigged macaque face model for visual and social neuroscience**
<img src= "https://user-images.githubusercontent.com/7523776/29430545-cbc198b0-8362-11e7-9826-5d5629ab22f4.gif" width="400" height="400" /> <img src= "https://user-images.githubusercontent.com/7523776/29431817-4fb301dc-8367-11e7-9e3c-4612c579d214.gif" width="400" height="400" /> 

This repository contains Python code for automated control of a Blender (www.blender.org) file containing a fully rigged, realistic 3-dimensional Rhesus macaque avatar. The mesh was generated from a CT scan of a live anesthetized Rhesus macaque, and edited in collaboration with a professional CGI artist (<a href="https://www.artstation.com/ishoop">Julien Duchemin</a>). The code allows quick setup of viewing geometry to match the experimental context, parametric manipulation of body, head and gaze direction, facial expression, skin and fur appearance, environment variables, and offline rendering of images and animations using the Cycles engine. In the future the code will include the ability to continuously morph facial identity based on an empirically-defined PCA "face-space", as well as game engine control for real-time closed-loop social neuroscience experiments. 

<img src= "https://user-images.githubusercontent.com/7523776/29434998-237ade62-8373-11e7-81b7-451fde4ba5b8.png" width="850" height="500" />

The following parmaters of the model can be varied continuously:
* Body position and orientation (3D world coordinates)
* Head orientation (spherical coordinates relative to body)
* Gaze direction (spherical coordinates relative to head direction)
* Eye vergence angle
* Eye lid closure (i.e. blink)
* 4 stereotypical facial expression trajectories (starting from neutral):
  * bared teeth display (submissive 'fear grimace')
  * open-mouthed threat (agressive)
  * pursed-lips (coo vocalization)
  * yawn
* Additional independent control of brow, ears, and jaw movement.
* Fur length, density, color, texture map
* Skin color, material reflectance (including sub-surbace scattering), and texture
* Lighting direction, intensity, color, and type
