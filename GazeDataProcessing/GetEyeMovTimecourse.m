% function GetEyeMovTimecourse(EyeFile)

%====================== GetEyeMovTimecourse.m =============================
% Loads TDT recorded eye tracking data from the specified .mat file and
% converts it into a format suitable for animating eye movements in
% Blender. The transformed data is saved as 5 channels of N samples, where
% each sample corresponds to one frame:
%   1) X position of target (cm from origin)
%   2) Y position of target (cm from origin)
%   3) Z position of target (cm from origin)
%   4) Normalized pupil dilation (range 0-1)
%   5) Normalized upper lid retraction (range 0-1)
%
%
%==========================================================================

 
% if nargin == 0
    EyeFile = '/Volumes/APM_02/NeuroData/Physio/TDT_converted/Dexter/20160502/20160502-Movie-1/Dexter-20160502-Movie-1-eyeSignal.mat';
% end
load(EyeFile);

%============ SET PARAMETERS
LidDownMean = 50;           % Mean duration (ms) for macaque lid closing during blink (Fuchs et al., 1992)
LidClosed   = 20;         	
LidUpMean   = 130;       	% Mean duration (ms) for macaque lid opening during blink (Fuchs et al., 1992)

ViewingDist = 100;          % Viewing distance (eye to screen) that data was collected at (cm)
VideoFPS    = 60;           % Frame rate of output data



%============= GET SCALING FACTOR
QNXpath = fullfile('/Volumes/APM_02/NeuroData/Physio/QNX/Dexter/20160502',Subject,Date);
DGZfile = wildcardsearch(QNXpath, '*Movie*.dgz');
DG      = dg_read(DGZfile{1});
ADCdeg 	= DG.e_params{1}{2};
DegPerV = repmat(204.8,[1,2])./ADCdeg';

%============= FORMAT EYE DATA
[EyeCh,EyeSig,SigPerSample] = size(eyeCodesAll);                                                 	% Check matrix dimensions
EyeSignal = nan(EyeCh, EyeSig*SigPerSample);
for n = 1:EyeCh                                                                                  	% For each channel...
    EyeSignal(n,:) = reshape(permute(eyeCodesAll(n,:,:),[3,2,1]),[1,numel(eyeCodesAll(n,:,:))]);   	% Reshape eye signal
end
EyeSignal       = EyeSignal([2,1,3],:);                                                           	% Reorder channels to: x, y, pupil
Eye.Signal(1,:) = EyeSignal(1,:)*DegPerV(1);                                                        % Convert horizontal position from voltage to degrees
Eye.Signal(2,:) = EyeSignal(2,:)*DegPerV(2);                                                        % repeat for vertical position
Eye.Signal(3,:) = EyeSignal(3,:);
Eye.Times       = linspace(0, numel(Eye.Signal(1,:))/eyeSampleRate, numel(Eye.Signal(1,:)));        % Create time stamps   


%========= FIND MISSING DATA
SaturationV = [mode(EyeSignal(1,:)), mode(EyeSignal(2,:)), -4.5];                                   % Find saturation voltage
MissingSamples = zeros(size(EyeSignal));                                                            % Create matrix of zeros
for Ch = 1:3
    MissingSamples(Ch, find(EyeSignal(Ch,:)<= SaturationV(Ch))) = 1;                                % Mark samples at saturation as ones
%     MissingSamplesDecimated(Ch,:) = decimate(MissingSamples(Ch,:), DecimateFactor);  	% Decimate missing sample vector
%     MissingSamplesDecimated(Ch,:) = round(MissingSamplesDecimated(Ch,:));               % Round values after 'decimate.m' filtering (0 or 1)
    MissingSampleIndices{Ch} = find(MissingSamples(Ch,:)==1);                                       % Find indices of samples 
    Eye.Signal(Ch, MissingSampleIndices{Ch}) = nan;                                                 % Replace staurated data with NaNs
end

%============= EXTRACT BLINKS
Blinks = ExtractBlinks(Eye.Signal, eyeSampleRate, 1);



%============= FILTER & INTERPOLATE EYE SIGNALS
Interp          = [];
% Filt            = filter()
DecimateFactor  = round(eyeSampleRate/VideoFPS);
for Ch = 1:3
%     Eye.Signal(ch,:) = interp2(Eye.Signal(ch,:), );                 % Interpolate
    Eye.Signal(ch,:) = filtfilt(Eye.Signal(ch,:), Filt);            % Filter
    Eye.Signal(ch,:) = decimate(Eye.Signal(ch,:), DecimateFactor);  % Decimate / downsample
end

%============= SAVE NEW EYE SIGNAL