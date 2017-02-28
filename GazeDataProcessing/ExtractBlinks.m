function Blink = ExtractBlinks(EyePos, SampleRate, DoPlot)

%========================== ExtractBlinks.m ===============================
% This function takes filtered, scaled eye position and pupil size (area or 
% diameter) signal (Nx3) and identifies potential blink-related periods. 
%
% INPUTS:
%   EyePos:     an Nx2 or Nx3 matrix of horizontal and vertical eye position (in
%               degrees of visual angle). Missing samples should be represented
%               with NaNs and any filtering of the signals should already have
%               been applied. Optional third column should contain pupil diameter.
%   SampleRate: the sample rate of the EyePos input in Hz.
%   DoPlot:     logical flag for whether to plot summary statistics
%
% OUTPUTS:
%   Sacc.Onset:     sample number of saccade onset
%   Sacc.Peak:      sample number of saccade peak velocity
%   Sacc.Offset:    sample number of saccade offset
%   Sacc.Amp:       amplitude of saccade 
%   Sacc.Micro:     logical vector identifying microsaccades
%   Sacc.Abrupt:    logical vector identifying abrupt saccade onset/offset
%   Sacc.Duration:  duration in seconds
%   Sacc.MeanSpeed: mean speed of saccade
%   Sacc.Clus1:     indices of cluster 1 movements: 'saccades'
%   Sacc.Clus2:     indices of cluster 2 movements: 'other'
%
% REFERENCES:
%   Choe KW, Blake R & Lee SH (2015). Pupil size dynamics duiring fixation
%       impact the accuracy and precision of video-based gaze estimation.
%       Vision Research.
%
% REQUIREMENTS:
%   Statistics Toolbox (optional): for k-means clustering
%   shadedplot.m: 
%
% REVISIONS:
%   05/01/2014 - Written by APM
%     ___  ______  __   __
%    /   ||  __  \|  \ |  \    APM SUBFUNCTIONS
%   / /| || |__/ /|   \|   \   Aidan P. Murphy - murphyap@mail.nih.gov
%  / __  ||  ___/ | |\   |\ \  Section on Cognitive Neurophysiology and Imaging
% /_/  |_||_|     |_| \__| \_\ National Institute of Mental Health
%==========================================================================

%% 
%========= Check input variables
if ~ismember(min(size(EyePos)), [2,3])
    error('Input parameter EyePos must be an Nx2 matric of gaze coordinates!');
end
if ~ismember(size(EyePos,2),[2,3])
    EyePos = EyePos';
end

size(EyePos)
SampleRate = round(SampleRate);
if ~exist('DoPlot','var')
    DoPlot = 0;
end

%%========= Set default blink paramaters
SizeThresh          = -4.5;          
PreBlinkDur         = -0.2;                 % Duration pre-blink to exclude (ms)
PostBlinkDur        = 0.2;                  % Duration post-blink to exclude (ms)
Blink.RateThresh    = 20;                   % Maximum rate of change in pupil size (z/s)

%========== Calculate blinks
Eye.Velocity    = diff(EyePos)*SampleRate;                             	% Find velocities in horizontal and vertical directions (deg/s)
Eye.Speed       = sqrt(Eye.Velocity(:,1).^2 + Eye.Velocity(:,2).^2);   	% Calculate speed magnitude (deg/s)
MissingData     = EyePos(:,3) <= SizeThresh;                          	% Find samples with pupil size < threshold
EyePos(MissingData,3) = nan;                                            % Replace values with NaNs
PupilSize       = EyePos(:,3)-nanmean(EyePos(:,3));                    	% Normalize pupil size measurement
PupilSize       = PupilSize/nanstd(PupilSize);                        	% Convert to z-score
Blink.RateChange = diff(PupilSize)*SampleRate;                          % Calculate rate of change of pupil size

Blinks          = find(isnan(PupilSize))';                             	% Find samples with missing pupil size
Blink.Starts    = [Blinks(1), Blinks(find(diff(Blinks)>1)+1)];        	% Find first sample missing for each blink period
Blink.Ends      = [Blinks(find(diff(Blinks)>1)), Blinks(end)];         	% Find last sample missing for each blink
PreBlink        = Blink.Starts+round(PreBlinkDur*SampleRate);          	% Define pre-blink start
PostBlink       = Blink.Starts+round(PostBlinkDur*SampleRate);         	% Define post-blink end
for B = 1:numel(Blink.Starts)-1                                        	% For each blink...
    BlinkPosDataX(B,:)  = EyePos(PreBlink(B):PostBlink(B),1);          	% Get eye position
    BlinkPosDataY(B,:)  = EyePos(PreBlink(B):PostBlink(B),2);          	%
    BlinkSpeed(B,:)     = Eye.Speed(PreBlink(B):PostBlink(B));              
end
Blink.Duration  = (Blink.Ends-Blink.Starts)/SampleRate;
BlinkTime       = linspace(PreBlinkDur, PostBlinkDur, size(Blink.RateChange,1));     



%% ========================= PLOT DATA ====================================
if DoPlot
    scnsize = get(0,'ScreenSize');                                  % Get screen resolution
    FigRect = [0 0 scnsize(3) scnsize(4)]*0.5;
    figure('name','Pupil Summary','OuterPosition',FigRect);
    
    axh(1) = subplot(2,3,1);
    hist(PupilSize,100);
    hold on;
    xlabel('Pupil size (z-score)');
    ylabel('frequency');
    
	axh(2) = subplot(2,3,2);
    Blink.RateChange(abs(Blink.RateChange)>Blink.RateThresh) = [];
	hist(Blink.RateChange,100);
    hold on;
    xlabel('Rate of pupil size change (z-score/s)');
    ylabel('frequency');
    
    axh(3) = subplot(2,3,3);
    plot(BlinkTime, nanmean(Blink.RateChange'), '-b');  
    xlabel('Time (ms)')
	ylabel('Eye speed (deg/s)');
    
    axh(4) = subplot(2,3,4);
    MaxDur = 500;
    hist(Blink.Duration(Blink.Duration<MaxDur)*1000,100);
 	xlabel('Duration (ms)')
	ylabel('Frequency');
    set(gca,'xlim',[0 MaxDur]);
   
    axh(5) = subplot(2,3,5);
    cloudPlot(reshape(BlinkPosDataX,[1,numel(BlinkPosDataX)]), reshape(BlinkPosDataY,[1,numel(BlinkPosDataY)]),[],[],[200,200]);
    hold on;
    ScreenSize = [37.5, 23.25];
    ScreenCenter = ScreenSize/2;
    rectangle('Position',[-ScreenCenter,ScreenSize], 'edgecolor','r', 'linewidth',2);
    axis xy equal tight;
    xlabel(sprintf('Horizontal (%c)',char(176)));
    ylabel(sprintf('Vertical (%c)',char(176)));
    Xlims = xlim;
    Xlims = max([max(abs(Xlims)), ScreenCenter(1)+1])*[-1,1];
    Ylims = ylim;
    Ylims = max([max(abs(Ylims)), ScreenCenter(2)+1])*[-1,1];
    set(gca, 'xlim', Xlims, 'ylim', Ylims);
    plot([0 0],ylim, '--w');
    plot(xlim,[0 0], '--w');
    cm = colormap;
    set(gca,'color',cm(1,:));
    colorbar;
    
    %========== Print summary stats
    PercentBlinkSamples = (numel(find(MissingData==1))/numel(EyePos(:,3)))*100;
    fprintf('Number of blinks detected = %d\n', numel(Blink.Starts));
    fprintf('Percentage samples excluded = %.2f %%\n', PercentBlinkSamples);
    fprintf('Blink durations = %.2f - %.2f ms\n', min(Blink.Duration), max(Blink.Duration));
end
