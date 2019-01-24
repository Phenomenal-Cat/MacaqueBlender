
%======================= GenerateControlStim.m ============================
% This script loads 3D stimulus images (full color, side-by-side squeezed
% frame .pngs and z-map .exr files) and generates control stimuli
% (random-dot stereograms and phase-scrambled silhouettes) from them.
%==========================================================================

Prefix = [];
if ismac
    Prefix = '/Volumes';
end
addpath(fullfile(Prefix, '/projects/murphya/MacaqueFace3D/MacaqueBlender/MatlabFunctions'));
addpath(fullfile(Prefix, '/projects/murphya/MacaqueFace3D/StimulusGeneration'));
addpath(fullfile(Prefix, '/projects/murphya/Matlab Code/APMSubfunctions/'));
addpath(fullfile(Prefix, '/projects/murphya/Matlab Code/APMSubfunctions/ImageProcessing'));
addpath(genpath(fullfile(Prefix, '/projects/murphya/Toolboxes/SHINEtoolbox')));

ImageDir    = fullfile(Prefix, '/projects/murphya/Stimuli/AvatarRenders_2018/SizeDistance/');
ZmapDir     = fullfile(ImageDir, 'DepthMaps');
RDSdir      = fullfile(ImageDir, 'RDSs');

AllHaz      = -45:15:45;
AllDist     = [-20,0,20];
AllEcc      = -30:15:30;

clear Display
if exist('Screen.m','file')
    Display.VD          = 0.7;
    Display.ScreenID    = 1;
    Display.Rect        = Screen('Rect',1);
    Display.Stereomode  = 0; 
end

Save                = 1;  
Overwrite           = 0; 
AnaglyphMode        = 1;
ZmapFormat          = 'exr';            % 'exr', or 'mat'

AllZmapFiles        = wildcardsearch(ZmapDir, ['*.' ZmapFormat]);

for f = 1:numel(AllZmapFiles)
    ZmapFile        = AllZmapFiles{f};
    [path, file]    = fileparts(ZmapFile);
    ImFile          = fullfile(ImageDir, 'Frames', [file, '.png']);
    RDSfile         = fullfile(RDSdir, [file, '.png']);
    SilFile         = fullfile(ImageDir, 'Silhouettes', [file, '.png']);

    fprintf('Processing image %s...\n', ImFile);

    %=========== Read image
    [im,cmap,ImAlpha] = imread(ImFile);
    if max(im(:)) > 256
        im = im/256;
    end
    img1    = imresize(double(im(:,1:1920,:)), [size(im,1), size(im,2)]);
    img2    = imresize(double(im(:,1921:end,:)), [size(im,1), size(im,2)]);
    alph1   = imresize(double(ImAlpha(:,1:1920)), [size(im,1), size(im,2)]);
    alph2   = imresize(double(ImAlpha(:,1921:end)), [size(im,1), size(im,2)]);

    %=========== Write anaglyph
%     Anaglyph = mkAnaglyph(img1,img2,AnaglyphMode,1,Save);
%     imwrite(Anaglyph, );

    %=========== Save depth map to .mat file
    if ismac && strcmpi(ZmapFormat, 'exr')
        OpenEXRdir  = fullfile(Prefix, '/projects/murphya/Matlab Code/APMSubfunctions/3D_rendering/openexr-matlab-master');
        addpath(OpenEXRdir);
        DepthMap    = exrread(ZmapFile);
        ZmapFile    = fullfile(path, [file, '.mat']);
        save(ZmapFile, 'DepthMap');
    end

    %=========== Write RDS
    if ~exist(RDSfile, 'file') || Overwrite == 1
        if exist('Display','var')==1
        	[RDSFile, Display] = Zmap2RDS(ZmapFile, RDSfile, 1, Display);
        end
    end

    %=========== Write silhouette
%     if ~exist(SilFile, 'file') || Overwrite == 1
%         img1(:,:,4) = alph1;
%         NewImage = GenerateSilhouette(img1);
%         NewImage = imresize(NewImage, [size(im,1), size(im,2)/2]);
%         NewImage(:,1921:3840,:) = NewImage;
%         NewImage(:,:,4) = ImAlpha;
% 
%         imwrite(NewImage(:,:,1:3), SilFile,'Alpha',double(NewImage(:,:,4)));
%     end
            
end