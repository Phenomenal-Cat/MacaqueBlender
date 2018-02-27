
%============================== Zmap2RDS.m ================================
% This script loads a 'Z buffer' depth map of a 3D scene and creates a 
% random dot steregoram (RDS) image. The depth map can be in the following
% image formats:
%       - ILM OpenEXR (.exr):   recommended. Lossless 32-bit float
%       - Radiance HDR (.hdr): 	
%
%
% REVISIONS:
% 25/04/2015 - Created by Aidan Murphy
%     ___  ______  __   __
%    /   ||  __  \|  \ |  \    APM SUBFUNCTIONS
%   / /| || |__/ /|   \|   \   Aidan P. Murphy - murphyap@mail.nih.gov
%  / __  ||  ___/ | |\   |\ \  Section on Cognitive Neurophysiology and Imaging
% /_/  |_||_|     |_| \__| \_\ National Institute of Mental Health
%==========================================================================

% if nargin == 0
    File = '/Volumes/Seagate Backup 1/NIH_Postdoc/DisparitySelectivity/Stim10K3D/Renders/Macaque_Id3_neutral_az0_el0_dist0_sc12.hdr';
% end

%============== LOAD DEPTH MAP
[path, filename, ext] = fileparts(File);
switch ext
    case '.hdr'
        DepthMap = hdrread(File);
    case '.exr'
        
    otherwise
        frpintf('WARNING: non-HDR image formats do no suppport metric depth!\n');
        
end

%============== SET PARAMETERS
InvertDepth = 0;
PlotData    = 0;
IPD         = 3.5;                              % Interpupillary distance of subject (cm)
VD          = 78;                            	% Viewing distance of subject (cm)
DisplayRes  = [size(DepthMap,2), size(DepthMap,1)];       	% Display resolution (pixels) [w, h]
MapLims     = [size(DepthMap,1), size(DepthMap,2)];
DisplaySize = [50, 30];                       	% Physical size of display (cm) [w, h]
DotDensity  = 0.5;                             	% Density of dots
DotDiam   	= 2;                               	% Dot diameter (pixels)
DotType     = 1;                              	% 1 = circles; 2 = Anti-aliased circles
DotBackground   = 0;

%============== PLOT DATA
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
set(axh(1),'clim',get(axh(2),'xlim'))
DepthLims = get(axh(2),'xlim');
if PlotData == 0
    close(fh);
end


Display = DisplaySettings(1);
Screen('Preference', 'SkipSyncTests', 1);
if any(Display.Rect([3,4]) ~= DisplayRes)
    fprintf('Resizing depth map to fit screen resolution (%d x %d)...\n',Display.Rect([3,4]));
    DepthMap    = imresize(DepthMap, DisplayRes([2,1]));
    MapLims     = [size(DepthMap,1), size(DepthMap,2)];
end

%============== GENERATE DOT POSITIONS
DotArea     = pi*(DotDiam/2)^2;
NoDots      = round(((MapLims(1)*MapLims(2))/DotArea)*DotDensity);                  % Calculate number of dots
Xpos        = round(rand([NoDots,1])*(MapLims(2)-1)+1);                          	% Generate random pixel indices for each dot
Ypos        = round(rand([NoDots,1])*(MapLims(1)-1)+1);                          	% Generate random pixel indices for each dot
for n = 1:NoDots                                                                    % For each dot...
    if DepthMap(Ypos(n), Xpos(n)) < DepthLims(2)                                 	% If dot position is on object surface...
        if InvertDepth == 0
            Zpos(n) = VD-(DepthMap(Ypos(n), Xpos(n),1)*100);                      	% Find depth (distance from fixation plane in cm)
        elseif InvertDepth == 1
            Zpos(n) = (DepthMap(Ypos(n), Xpos(n),1)*100)-VD;                      	% Find depth (distance from fixation plane in cm)
        end
    elseif DepthMap(Ypos(n), Xpos(n)) >= DepthLims(2)                             	% If dot position is on background...
        if DotBackground == 1
            Zpos(n) = 0;                                                            % Set to zero disparity (fixation plane)
        elseif DotBackground == 0
            Zpos(n) = NaN;                                                        	% Don't plot background dots (fixation plane)
        end
    end
    TanTheta(n) 	= (IPD/2)/(VD-Zpos(n));
    Xdiff(n)       = TanTheta(n)*Zpos(n)*Display.Pixels_per_m(1)/100;                              
    XposDisp{1}(n) = Xpos(n)+Xdiff(n);
    XposDisp{2}(n) = Xpos(n)-Xdiff(n);
end
DotColors = repmat(round(rand([NoDots, 1]))*255,[1,3]);

if PlotData == 1
    axh(3) = subplot(1,3,3);
    hist(Xdiff, 100);
    xlabel('Horizontal disparity (pixels)')
end

%============== CREATE RDS
PsychImaging('PrepareConfiguration');
[Display.win, rect] = PsychImaging('OpenWindow', Display.ScreenID, 127, [], [], [], Display.Stereomode);
Screen('BlendFunction', Display.win, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);                 % Enable alpha channel
SetAnaglyphStereoParameters('FullColorAnaglyphMode', Display.win);
TextureBackground = ones(MapLims(1:2))*0.5;
for eye = 1:2
    currentbuffer = Screen('SelectStereoDrawBuffer', Display.win, eye-1); 
    Screen('DrawDots', Display.win, [XposDisp{eye}; Ypos'], DotDiam, DotColors', [], DotType);
end
[VBL StimOn] = Screen('Flip', Display.win);
RDScapture = Screen('GetImage', Display.win, CenterRect([0 0 1000 1000], rect));
WaitSecs(1);
imwrite(RDScapture, sprintf('%s_RDS_inv%d.png',filename, InvertDepth))
sca;