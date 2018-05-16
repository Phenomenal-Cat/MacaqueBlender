
%======================== GenerateExpVoxStim.m ============================
% This script loads movie files of monkeys performing various types of 
% vocalization, extracts the audio and video and recombines them in every
% combination for use as experimental stimuli.
%

Mov.DefaultPath  	= '/projects/murphya/MacaqueFace3D/Macaque_video/';
Mov.MonkeyIDs       = {'BE','PH','ST'};
Mov.CallTypes       = {'Coo','Pantthreat','Scream','Bark'};
Mov.InputFormat     = '.mpg';
AudioThreshSDs      = 2;                % Number of SDs sound pressure level must cross
SilenceWindow       = 0.1;              % Number of ms sample to calculate SD from

figure;
for i = 1%:numel(Mov.MonkeyIDs)
    for ct = 1:3%numel(Mov.CallTypes)
        MovFiles = wildcardsearch(Mov.DefaultPath, sprintf('%s_%s*%s', Mov.MonkeyIDs{i}, Mov.CallTypes{ct}, Mov.InputFormat));
        if ~isempty(MovFiles)
            Mov.FullFilename  	= MovFiles{1};                         
            [video, audio]      = mmread(Mov.FullFilename, [],[],[],false);                    % Load movie file and audio
            Data(i,ct).File     = Mov.FullFilename;
            Data(i,ct).Call     = Mov.CallTypes{ct};
            Data(i,ct).ID       = Mov.MonkeyIDs{i};
            Data(i,ct).video    = video;
            Data(i,ct).audio    = audio;
            [~,Filename]        = fileparts(Mov.FullFilename);
            Mov.NoFrames        = numel(video.frames);
            Mov.FPS             = video.rate;
            Mov.FrameTimes     	= linspace(0, Mov.NoFrames/Mov.FPS, Mov.NoFrames);
            Mov.CurrentFrame    = 1;

            %================ Extract vocalization
            SampleTimes         = linspace(0, size(audio.data,1)/audio.rate, size(audio.data,1));
            VolumeThresh        = std(audio.data(1:round(audio.rate*SilenceWindow),1))*AudioThreshSDs;
            VocalOnsetSmp       = find(audio.data(:,1) > VolumeThresh, 1);
            VocalOffsetSmp      = find(audio.data(:,1) > VolumeThresh, 1, 'last');
            VocalOnsetTime      = SampleTimes(VocalOnsetSmp);
            VocalOffsetTime     = SampleTimes(VocalOffsetSmp);
            Data(i,ct).Vox.OnsetSmp  = VocalOnsetSmp;
            Data(i,ct).Vox.OnsetTime = VocalOnsetTime;
            Data(i,ct).Vox.Clip      = audio.data(VocalOnsetSmp:VocalOffsetSmp,:);

            %================ Plot audio
            Fig.axh(ct,1) = subplot(3,2,(ct-1)*2+1);
            ph = plot(SampleTimes, audio.data(:,1));
            grid on;
            box off;
            hold on;
            Ylims = get(gca,'ylim');
            ph = patch([repmat(VocalOnsetTime,[1,2]), repmat(VocalOffsetTime,[1,2])], Ylims([1,2,2,1]), ones(1,4), 'facecolor', [1,0.5,0.5], 'edgecolor','none','facealpha', 0.5);
            title(sprintf('Call type: "%s"', Mov.CallTypes{ct}),'horizontalalignment','left')

            Fig.axh(ct,2) = subplot(3,2,(ct-1)*2+2);
            SegmentLength = audio.rate/50;
            spectrogram(audio.data(:,1), SegmentLength,[],[], audio.rate, 'yaxis');
            hold on;
            plot(repmat(VocalOnsetTime,[1,2]), ylim, '-r','linewidth',2);
            title('Spectrogram','horizontalalignment','left')
            

        else
            fprintf('No %s files found for monkey %s making a %s call!\n', Mov.InputFormat, Mov.MonkeyIDs{i}, Mov.CallTypes{ct});
        end
    end
    
    %=================== Create new movies of all face-voice combinations
    NewDir = fullfile(Mov.DefaultPath, 'FaceVoiceIntegration');
    if ~exist(NewDir,'dir')
        mkdir(NewDir);
    end
    for a = 1:3%numel(Mov.CallTypes)
        for v = 1:3%numel(Mov.CallTypes)
            NewAudio        = zeros(size(Data(i,v).audio.data));                    % Create empty 2 channel audio matrix
            VoxLength       = size(Data(i,a).Vox.Clip, 1);                          % Get number of samples in vocal audio clip
            RemainingSmpl   = size(NewAudio,1)-Data(i,v).Vox.OnsetSmp;              % Calculate number of available samples in new audio from onset
            if VoxLength > RemainingSmpl                                          	% If there aren't enough samples available...
                VocalClip = Data(i,a).Vox.Clip(1:RemainingSmpl);                    % Clip the end off the vocalsample
            else
                VocalClip = Data(i,a).Vox.Clip;
            end
            NewAudio(Data(i,v).Vox.OnsetSmp +(0:(size(VocalClip,1))-1),:) = VocalClip;

            WavFilename         = fullfile(NewDir, sprintf('V_%s_%s_A_%s_%s.wav', Data(i,v).ID, Data(i,v).Call, Data(i,a).ID, Data(i,a).Call));
            audiowrite(WavFilename, NewAudio, audio.rate, 'BitsPerSample', audio.bits);
            
        end
    end
    
    
end


