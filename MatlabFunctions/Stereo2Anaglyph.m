function Stereo2Anaglyph

%============================= Stereo2Anaglyph.m ==========================

InputStereoFormats  = {'SBS','SBSsq','TB'};
InputStereFormat    = 2; 
InputArrangement    = {};

AnaglyphColors      = {'red-cyan','red-green','green-magenta'};
AnaglyphModes       = {'Optimized anaglyph', 'Color anaglyph', 'Half-color anaglyph'};
AnaglyphMode        = 1;
AnaglyphColors      = 1;

%================ 
if ismac
    Prefix = '/Volumes';
else
    Prefix = [];
end
DefaultOutDir   = fullfile(Prefix,'/projects/murphya/');
DefaultStimDir  = fullfile(Prefix,'/projects/murphya/Stimuli/AvatarRenders_2018/StereoShape/SBS/');
InputFiles      = uipickfiles('FilterSpec', DefaultStimDir, 'type', {'*.png','PNGs';'*.jpg', 'JPEGs'},'prompt','Select stereo input images');
OutputDir       = uigetdir(DefaultOutDir, 'Select directory to save anaglyph images to');

%================ Convert images and save
wbh = waitbar(0);
for f = 1:numel(InputFiles)
    waitbar(f/numel(InputFiles), wbh, sprintf('Converting stereo image %d of %d...', f,numel(InputFiles)));
    [im,c,alpha] = imread(InputFiles{f});
    ImSize      = size(im);
    HalfSize    = ImSize/2;
    if InputStereFormat >= 2                % Side-by-side stereo image input
        imgL    = im(:,1:HalfSize(2),:);
        imgR    = im(:,(HalfSize(2)+1):end,:);
        if InputStereFormat == 2            % Side-by-side squeezed frame format
            imgL = imresize(imgL, ImSize([1,2]));
            imgR = imresize(imgR, ImSize([1,2]));
        end
    elseif InputStereFormat == 3            % Top-bottom stereo format
        imgL    = im(1:HalfSize(1),:,:);
        imgR    = im((HalfSize(1)+1):end,:,:);
        imgL    = imresize(imgL, ImSize([1,2]));
        imgR = imresize(imgR, ImSize([1,2]));
    end
    oimg = mkAnaglyph(imgL, imgR, AnaglyphMode, AnaglyphColors);
    [~,Filepart] 	= fileparts(InputFiles{f});
    OutputFile      = fullfile(OutputDir, sprintf('%s_Ana.png', Filepart));
    imwrite(oimg, OutputFile);
end
delete(wbh);



end


%================ Generate single color anaglyph image
function oimg = mkAnaglyph(imL, imR, mode, colors)

switch mode
    case 1      %========= optimized anaglyph
        trfmtx1 = [0,0.7,0.3;0,0,0;0,0,0];
        trfmtx2 = [0,0,0;0,1,0;0,0,1];
    case 2      %========= half color anaglyph
        trfmtx1 = [1,0,0;0,0,0;0,0,0];
        trfmtx2 = [0,0,0;0,1,0;0,0,1];
    case 3      %========= color anaglyph
        trfmtx1 = [0.299,0.587,0.114;0,0,0;0,0,0];
        trfmtx2 = [0,0,0;0,1,0;0,0,1];
    otherwise
        error('mode should be one of 1 (optimized), 2 (color), or 3 (half-color). Check input.');
end

if colors == 1      % For red-cyan anaglyphs...
    trfmtx1 = [0,0.45,1.0;0,0,0;0,0,0];
    trfmtx2 = [0,0,0;0,1.0,0;0,0,1.0];
end

oimg = zeros(size(imL));
imL = double(imL);
imR = double(imR);
for ii=1:1:size(imL,1)
    for jj=1:1:size(imL,2)
        oimg(ii,jj,:) = trfmtx1*[imL(ii,jj,1);imL(ii,jj,2);imL(ii,jj,3)]+...
                        trfmtx2*[imR(ii,jj,1);imR(ii,jj,2);imR(ii,jj,3)];
    end
end
oimg = uint8(oimg);

end

