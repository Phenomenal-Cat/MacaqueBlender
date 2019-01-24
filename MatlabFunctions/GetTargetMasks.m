function Params = LoadGazeFollowingFrames(Params)

%======================= LoadGazeFollowingFrames.m ========================


TargetDir       = '/projects/murphya/Blender/Renders/CuedAttention/AnimationFrames_D=30cm/';
TargetsRGBFile  = fullfile(TargetDir, 'Targets_RGBA_Neutral.png');
TargetsIndxFile = fullfile(TargetDir, 'TargetIndexMap.png');

%========= Load images
IndxIm                      = imread(TargetsIndxFile);
[ColorIm, cmap, AlphaIm]  	= imread(TargetsRGBFile);

%========= Set parameters
NoTargets           = 24;
FramesPerTarget     = 8;
Conditions          = {'Eyes','Head','EyesClosed','EyesOnly'};
FileFormat          = 'png';

for t = 1:NoTargets
	MaskIm      = IndxIm == t;
    NewMask 	= double(AlphaIm).*double(MaskIm);
    NewColorIm  = ColorIm;
    NewColorIm(:,:,4) = NewMask;
    Params.GF.TargetTex(t) = Screen('MakeTexture', Params.Display.win, NewColorIm);
    
    % Find target centroid (screen pixel coordinates)
    ExpIm = imresize(MaskIm(:,1:size(MaskIm,2)/2), [size(MaskIm,1), size(MaskIm,2)]);   
    [Y,X] = find(ExpIm==1);
    TargetCentroid(t,:) = [mean(X), mean(Y)];
    
    
    for f = 1:FramesPerTarget
        Filename = fullfile(TargetDir, sprintf('LookAtLocation_%s_Target%d_Frame%03d.%s', Conditions{1}, t, f, FileFormat));
        [img, cmap, alpha] = imread(Filename);
        img(:,:,4) = alpha;
        Params.GF.CondTex(t, f) = Screen('MakeTexture', Params.Display.win, img);
    end
end