  
### **A Python library for parametric control of a 3D rigged macaque face model for visual and social neuroscience**
<img src= "https://user-images.githubusercontent.com/7523776/29430545-cbc198b0-8362-11e7-9826-5d5629ab22f4.gif" width="300" height="300" /> <img src= "https://user-images.githubusercontent.com/7523776/29431817-4fb301dc-8367-11e7-9e3c-4612c579d214.gif" width="300" height="300" /> 

<iframe src="https://player.vimeo.com/video/243763351?autoplay=1&loop=1&autopause=0" width="300" height="300" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

<iframe src="https://player.vimeo.com/video/323447440?autoplay=1&loop=1&autopause=0" width="533" height="300" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

This repository contains Python code for automated control of a Blender (www.blender.org) file containing a fully rigged, realistic 3-dimensional Rhesus macaque avatar. The mesh was generated from a CT scan of a live anesthetized Rhesus macaque, and edited in collaboration with a professional CGI artist (<a href="https://www.artstation.com/ishoop">Julien Duchemin</a>). The code allows quick setup of viewing geometry to match the experimental context, parametric manipulation of body, head and gaze direction, facial expression, skin and fur appearance, environment variables, and offline rendering of images and animations using the Cycles engine. In the future the code will include the ability to continuously morph facial identity based on an empirically-defined PCA "face-space" based on a library of CT data, as well as game engine (Blender/ Unity) control for real-time closed-loop social neuroscience experiments. 

<img src= "https://user-images.githubusercontent.com/7523776/29434998-237ade62-8373-11e7-81b7-451fde4ba5b8.png" width="850" height="500" />

The following parameters of the model can be varied continuously:
* Body position and orientation (Cartesian coordinates relative to world origin)
* Head orientation (spherical coordinates relative to body)
* Gaze direction (spherical coordinates relative to head)
* Eye vergence angle (determined automatically for gaze target distance)
* Eye lid closure (i.e. blink)
* Blend shapes for 4 stereotypical facial expression apexes:
  1) neutral
  2) open-mouthed threat (agressive)
  3) bared teeth display (submissive 'fear grimace')
  4) pursed-lips /coo vocalization (affiliative)
  5) yawn 
  
  <img src= "https://user-images.githubusercontent.com/7523776/36106084-54a84d8c-0fe4-11e8-9330-3e32795f64b4.png" width="850" height="165" />
  
* Additional independent control of brow, ears, and jaw movement.
* Fur length, density, color, texture map
* Skin color, material reflectance (including sub-surbace scattering), and texture
* Lighting direction, intensity, color, and type

## References
For preliminary neural data recorded from macaque inferotemporal cortex during viewing of these stimuli, please see the following Society for Neuroscience poster by <a href="https://www.researchgate.net/publication/323126846_Measuring_neuronal_selectivity_for_facial_features_in_macaque_inferotemporal_cortex_through_adaptive_sampling_of_feature_space">Murphy & Leopold (2017)</a>.
