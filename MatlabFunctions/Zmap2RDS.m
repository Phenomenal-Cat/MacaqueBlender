function [RDSFile, Display] = Zmap2RDS(ZmapFile, RDSFile, ScaleDepth, Display)

%============================== Zmap2RDS.m ================================
% This script loads a 'Z buffer' depth map of a 3D scene and creates a 
% random dot steregoram (RDS) image. The depth map can be in the following
% image formats:
%       - ILM OpenEXR (.exr):   recommended. Lossless 32-bit float
%       - Radiance HDR (.hdr): 	
%
% INPUTS:   ZmapFile:   full path of a depth map file (.exr; .hdr) from
%                       to create RDS of.
%         	RDSFile:    full path filename to save RDS image to. 
%           ScaleDepth: scalar specifying proportion of veridical depth to
%                       scale depth to (e.g. 1 = veridical, -1 = inverted)
%           Display:    display settings from previous call of Zmap2RDS
%
% RESOURCES: OpenEXR for Matlab: https://github.com/skycaptain/openexr-matlab
%
% REVISIONS:
%   25/04/2015 - Created by Aidan Murphy
%   01/07/2016 - Updated to read HDR formats
%   22/06/2018 - Added instructions for installing OpenEXR exrread.m
%     ___  ______  __   __
%    /   ||  __  \|  \ |  \    APM SUBFUNCTIONS
%   / /| || |__/ /|   \|   \   Aidan P. Murphy - murphyap@mail.nih.gov
%  / __  ||  ___/ | |\   |\ \  Section on Cognitive Neurophysiology and Imaging
% /_/  |_||_|     |_| \__| \_\ National Institute of Mental Health
%==========================================================================

if nargin == 0
    ZmapFile  	= '/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/Renders/DepthMaps/Macaque_Zmap_neutral_az0_el0_dist0_sc12.hdr';
    OutputDir   = '/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/Renders/RDS/';
end
if nargin < 2
    ScaleDepth  = 1;
end

%============== LOAD DEPTH MAP
[path, filename, ext] = fileparts(ZmapFile);
switch ext
    case '.hdr'
        DepthMap = hdrread(ZmapFile);
    case '.exr'
        OpenEXDdir = '/Volumes/projects/murphya/Matlab Code/APMSubfunctions/3D_rendering/openexr-matlab-master';
        addpath(OpenEXRdir);
        DepthMap = exrread(ZmapFile);
    otherwise
        frpintf('WARNING: non-HDR image formats do no suppport metric depth!\n');
        DepthMap = imread(ZmapFile);        
end
if ~exist('RDSFile','var')
    [~,filename] = fileparts(ZmapFile);
    RDSFile = fullfile(OutputDir, sprintf('RDS_%s_scale%d.png',filename, ScaleDepth*100));
end
if exist('Display','var') 
    LeavePTBopen = 1;
    if isempty(Display)
        clear Display;
    end
elseif ~ exist('Display','var')
    LeavePTBopen = 0;
end

%============== SET PARAMETERS
InvertDepth = ScaleDepth/abs(ScaleDepth);       
PlotData    = 0;
IPD         = 3.5;                              % Interpupillary distance of subject (cm)
VD          = 78;                            	% Viewing distance of subject (cm)
DisplayRes  = [size(DepthMap,2), size(DepthMap,1)];       	% Display resolution (pixels) [w, h]
MapLims     = [size(DepthMap,1), size(DepthMap,2)];
DisplaySize = [50, 30];                       	% Physical size of display (cm) [w, h]
DotDensity  = 0.5;                             	% Density of dots
DotDiam   	= 2;                               	% Dot diameter (pixels)
DotType     = 1;                              	% 1 = circles; 2 = Anti-aliased circles
DotBackground  = 0;

%============== PLOT DATA
if PlotData == 1
    fh = figure;
    axh(1)  = subplot(1,3,1);
    imh     = imagesc(DepthMap(:,:,1));
    axis equal tight
    colorbar
    axh(2) = subplot(1,3,2);
    hist(DepthMap(DepthMap(:)<9*10^9),100);
    xlabel('Pixel values/ Distance (cm)')
    ylabel('Frequency')
    grid on
    set(axh(1),'clim',get(axh(2),'xlim'));
end 
ObjectPixels    = DepthMap(DepthMap(:)<9*10^9);
DepthLims       = [min(ObjectPixels), max(ObjectPixels)];
FilenameDist    = str2double(ZmapFile((strfind(ZmapFile, 'dist')+4): (strfind(ZmapFile, '_sc')-1)));
MeanDistance    = VD + FilenameDist;


if ~exist('Display','var')
    Display = DisplaySettings(1);
    Screen('Preference', 'SkipSyncTests', 1);
end
    
if any(Display.Rect([3,4]) ~= DisplayRes)
%     fprintf('Resizing depth map (%d x %d) to fit screen resolution (%d x %d)...\n', DisplayRes, Display.Rect([3,4]));
%     DepthMap    = imresize(DepthMap, Display.Rect([4,3]));
%     MapLims     = [size(DepthMap,1), size(DepthMap,2)];
    fprintf('Cropping depth map (%d x %d) to fit screen resolution (%d x %d)...\n', DisplayRes, Display.Rect([3,4]));
    Ydiff       = abs(Display.Rect(4)-DisplayRes(2))/2;
    Yindx       = (Ydiff+1):(DisplayRes(2)-Ydiff);
    Xdiff       = abs(Display.Rect(3)-DisplayRes(1))/2;
    Xindx       = (Xdiff+1):(DisplayRes(1)-Xdiff);
    DepthMap    = DepthMap(Yindx,Xindx,:); 
    MapLims     = [size(DepthMap,1), size(DepthMap,2)];
end

%============== GENERATE DOT POSITIONS
DotArea     = pi*(DotDiam/2)^2;
NoDots      = round(((MapLims(1)*MapLims(2))/DotArea)*DotDensity);                  % Calculate number of dots
Xpos        = round(rand([NoDots,1])*(MapLims(2)-1)+1);                          	% Generate random pixel indices for each dot
Ypos        = round(rand([NoDots,1])*(MapLims(1)-1)+1);                          	% Generate random pixel indices for each dot
for n = 1:NoDots                                                                    % For each dot...
    if DepthMap(Ypos(n), Xpos(n)) < DepthLims(2)+10                              	% If dot position is on object surface...
      	Zpos(n) = VD-(DepthMap(Ypos(n), Xpos(n),1)*100);                            % Find depth (distance from fixation plane in cm)
        if ScaleDepth ~= 1
            Zpos(n) = ((Zpos(n)-FilenameDist)*ScaleDepth)+FilenameDist;             % Scale surface depth (not position in depth)
        end
        
    elseif DepthMap(Ypos(n), Xpos(n)) >= DepthLims(2)+10                           	% If dot position is on background...
        if DotBackground == 1
            Zpos(n) = 0;                                                            % Set to zero disparity (fixation plane)
        elseif DotBackground == 0
            Zpos(n) = NaN;                                                        	% Don't plot background dots (fixation plane)
        end
    end
    TanTheta(n) 	= (IPD/2)/(VD-Zpos(n));
    Xdiff(n)        = TanTheta(n)*Zpos(n)*Display.Pixels_per_m(1)/100;                              
    XposDisp{1}(n)  = Xpos(n)+Xdiff(n);
    XposDisp{2}(n)  = Xpos(n)-Xdiff(n);
end
DotColors = repmat(round(rand([NoDots, 1]))*255,[1,3]);

if PlotData == 1
    axh(3) = subplot(1,3,3);
    hist(Xdiff, 100);
    xlabel('Horizontal disparity (pixels)');
end

%============== CREATE RDS
if ~isfield(Display,'win')
    PsychImaging('PrepareConfiguration');
    [Display.win, Display.rect] = PsychImaging('OpenWindow', Display.ScreenID, 127, [], [], [], Display.Stereomode);
    Screen('BlendFunction', Display.win, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);                 % Enable alpha channel
    SetAnaglyphStereoParameters('FullColorAnaglyphMode', Display.win);
end
TextureBackground = ones(MapLims(1:2))*0.5;
for eye = 1:2
    currentbuffer = Screen('SelectStereoDrawBuffer', Display.win, eye-1); 
    Screen('DrawDots', Display.win, [XposDisp{eye}; Ypos'], DotDiam, DotColors', [], DotType);
end
[VBL StimOn] = Screen('Flip', Display.win);
RDScapture = Screen('GetImage', Display.win, CenterRect([0 0 1000 1000], Display.rect));
WaitSecs(1);
imwrite(RDScapture, RDSFile);

if LeavePTBopen == 0
    sca;
end