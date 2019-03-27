
#======================== SaveParams.py =============================
# This script reads or writes the settings of the current .blend file
# as a Python dictionary in pickle (.pkl) file format. 

import bpy
import csv
import datetime
import pickle

def save_Params(Params, name):
    with open('Params/'+ name + '.pkl', 'wb') as f:
        pickle.dump(Params, f, pickle.HIGHEST_PROTOCOL)

def load_Params(name):
    with open('Params/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def GetParams(filename):
    
    #============ Get basic info
    Params['BlendFile']         = bpy.data.filepath
    Params['TimeSaved']         = str(datetime.datetime.now())
    Scene                       = bpy.data.scenes[0]
    Cam                         = bpy.data.objects["Camera"]
    Cam2                        = bpy.data.cameras["Camera"]
    StereoSet                   = bpy.context.scene.render.image_settings

    #============ Get render settings
    Params['SceneUnits']        = Scene.unit_settings.system
    Params['RenderEngine']      = Scene.render.engine
    Params['Resolution']        = [Scene.render.resolution_x, Scene.render.resolution_y]
    Params['ResScaling']        = Scene.render.resolution_percentage
    Params['ColorDepth']        = Scene.render.image_settings.color_depth 
    Params['ColorMode']         = Scene.render.image_settings.color_mode
    Params['FileFormat']        = Scene.render.image_settings.file_format       
    Params['Transparency']      = Scene.cycles.film_transparent    

    #============ Get stereo settings
    Params['StereoOn']          = Scene.render.use_multiview                
    Params['StereoMode']        = StereoSet.stereo_3d_format.display_mode 
    Params['StereoSBS_x']       = StereoSet.stereo_3d_format.use_sidebyside_crosseyed
    Params['StereoSBS_sq']      = StereoSet.stereo_3d_format.use_squeezed_frame
    Params['StereoAnaType']     = StereoSet.stereo_3d_format.anaglyph_type
    Params['Stereo_IPD']        = Cam2.stereo.interocular_distance
    Params['Stereo_VD']         = Cam2.stereo.convergence_distance
    Params['Stereo_conv']       = Cam2.stereo.convergence_mode
            
    #============ Get camera settings
    Params['Cam_location']      = Cam.location
    Params['Cam_angle']         = Cam.rotation_euler
    Params['Cam_FOV']           = Scene.camera.data.angle
    Params['Cam_OrthoSc']       = Scene.camera.data.ortho_scale  
    Params['Cam_proj']          = Scene.camera.data.type
    Params['Cam_pano']          = Scene.camera.data.cycles.panorama_type
        
    #============ Get path tracing settings
    Params['Samples']           = bpy.context.scene.cycles.samples
    Params['Samples_sq ']       = bpy.context.scene.cycles.use_square_samples

    #============ Write variables to .pkl file
    save_Params(Params, filename)
    
    
def SetParams(filename):
    
    load_Params(name)
    if bpy.data.filepath ~= Params['BlendFile']:        # Check filename matches...
         
    #============ Get basic info
    Scene                       = bpy.data.scenes[0]
    Cam                         = bpy.data.objects["Camera"]
    Cam2                        = bpy.data.cameras["Camera"]
    StereoSet                   = bpy.context.scene.render.image_settings

    #============ Get render settings
    Scene.unit_settings.system                  = Params['SceneUnits'] 
    Scene.render.engine                         = Params['RenderEngine']
    Scene.render.resolution_x                   = Params['Resolution'][0]
    Scene.render.resolution_y                   = Params['Resolution'][1]
    Scene.render.resolution_percentage          = Params['ResScaling']
    Scene.render.image_settings.color_depth     = Params['ColorDepth'] 
    Scene.render.image_settings.color_mode      = Params['ColorMode'] 
    Scene.render.image_settings.file_format     = Params['FileFormat']      
    Scene.cycles.film_transparent               = Params['Transparency'] 

    #============ Get stereo settings
    Scene.render.use_multiview                          = Params['StereoOn']              
    StereoSet.stereo_3d_format.display_mode             = Params['StereoMode']
    StereoSet.stereo_3d_format.use_sidebyside_crosseyed = Params['StereoSBS_x']
    StereoSet.stereo_3d_format.use_squeezed_frame       = Params['StereoSBS_sq'] 
    tereoSet.stereo_3d_format.anaglyph_type             = Params['StereoAnaType'] 
    Cam2.stereo.interocular_distance                    = Params['Stereo_IPD'] 
    Cam2.stereo.convergence_distance                    = Params['Stereo_VD'] 
    Cam2.stereo.convergence_mode                        = Params['Stereo_conv']
            
    #============ Get camera settings
    Cam.location                            = Params['Cam_location'] 
    Cam.rotation_euler                      = Params['Cam_angle'] 
    Scene.camera.data.angle                 = Params['Cam_FOV']
    Scene.camera.data.ortho_scale           = Params['Cam_OrthoSc'] 
    Scene.camera.data.type                  = Params['Cam_proj'] 
    Scene.camera.data.cycles.panorama_type  = Params['Cam_pano']
        
    #============ Get path tracing settings
    bpy.context.scene.cycles.samples                = Params['Samples'] 
    bpy.context.scene.cycles.use_square_samples     = Params['Samples_sq ']
    
    