function ExtractParamsGUI

%========================= ExtractParamsGUI.m =============================
% This simple GUI is designed for loading short movie clips of animals
% making vocalizations, and manually tracking frame-by-frame kinematics of
% specific anatomical structures.
%
% 02/20/2018 - Written by Aidan Murphy
%==========================================================================

global Mov Fig video audio Params

LoadMovieClip;  % User selects movie clip to load

SampleTimes     = linspace(0, size(audio.data,1)/audio.rate, size(audio.data,1));
VolumeThresh    = 0.05;
VocalOnsetSmp   = find(audio.data(:,1) > VolumeThresh, 1);
VocalOffsetSmp  = find(audio.data(:,1) > VolumeThresh, 1, 'last');
VocalOnsetTime  = SampleTimes(VocalOnsetSmp);
VocalOffsetTime = SampleTimes(VocalOffsetSmp);

ParamNames  = {'Jaw opening','Expression amount','Ear flap','Brow raise', 'Blink', 'Head Elevation'};
Fig.Headers	= {'Time','blink','Kiss','jaw','ears','Fear','yawn','eyebrow','HeadTracker'};
for n = 1:numel(ParamNames)
    Params(n).Name          = ParamNames{n};
    Params(n).Timecourse    = zeros(1, Mov.NoFrames);
    StartPos = [(video.width/2)-50,(video.width/2)+50, (video.height/2)-(10*n),(video.height/2)-(10*n)]';
    Params(n).LinePoints    = repmat(StartPos,[1, Mov.NoFrames]);
end


%================== Open figure
ScreenRes   = get(0,'screensize');
Fig.fh      = figure('position',ScreenRes-[0,0,0,200],'units','pixels');
Fig.axh(1)  = subplot(4,2,1:2:5);
Fig.imh     = image(video.frames(1).cdata);
axis equal tight off
Fig.fn = title(sprintf('%s', strrep(Mov.Filename,'_',' ')),'fontsize',14);
Fig.th = text(10,10,sprintf('Frame %d', 1),'color',[1 1 1],'fontsize', 16);


%================= Plot audio waveform and spectrogram
Fig.axh(2) = subplot(numel(ParamNames)+2,2,2);
ph = plot(SampleTimes, audio.data(:,1));
grid on;
box off;
hold on;
Ylims = get(gca,'ylim');
ph = patch([repmat(VocalOnsetTime,[1,2]), repmat(VocalOffsetTime,[1,2])], Ylims([1,2,2,1]), ones(1,4), 'facecolor', [1,0.5,0.5], 'edgecolor','none','facealpha', 0.5);
title('Audio waveform','horizontalalignment','left')
set(gca,'xticklabel',[]);

Fig.axh(3) = subplot(numel(ParamNames)+2,2,4);
SegmentLength = audio.rate/20;
spectrogram(audio.data(:,1), SegmentLength,[],[], audio.rate, 'yaxis');
hold on;
plot(repmat(VocalOnsetTime,[1,2]), ylim, '-r','linewidth',2);
title('Spectrogram','horizontalalignment','left')
set(Fig.axh([2]),'xlim',[0, SampleTimes(end)]);
xlabel('Time (ms)');

%================= Plot parameter time-courses
Fig.ActiveParam = 1;
Fig.LineColors  = [1,0,0;0,1,0;0,0,1;0,1,1; 1,1,0; 1,0,1; 1,0.5,0];
Fig.XtickLabels = {[],[],[],[]};
Fig.ParamSmoothing = zeros(1,numel(Params));
for f = 1:ceil(numel(Mov.FrameNumbers)/5)
    Fig.XtickLabels = [Fig.XtickLabels, {f*5,[],[],[],[]}];
end
for n = 1:numel(Params)
    
    %======= Plot timecourse
    Fig.axh(n+3)        = subplot(numel(ParamNames)+2,2,4+2*n);
    Fig.ParamsH(n+3)    = plot(Mov.FrameNumbers, Params(n).Timecourse,'.-k','color',Fig.LineColors(n,:),'markersize',15);
    hold on;
    grid on
    title(Params(n).Name,'horizontalalignment','left');
  	set(Fig.axh(n+3),'buttondownfcn',{@SelectParam,n},'xlim',[1,Mov.NoFrames], 'xtick', Mov.FrameNumbers, 'xticklabel', Fig.XtickLabels);
    Fig.plh(n)          = plot([0,0], [0,1], '-g', 'linewidth', 2);
    axis tight;
    box off;
    if n == numel(Params)
        xlabel('Frame number');
    else
        set(gca,'xticklabel',[]);
    end
    
    %======= Plot interactive points on image
    axes(Fig.axh(1));
    Fig.LineH(n)    = imline(Fig.axh(1), [Params(n).LinePoints(1:2,Mov.CurrentFrame), Params(n).LinePoints(3:4,Mov.CurrentFrame)]);
    setColor(Fig.LineH(n),Fig.LineColors(n,:));
    Fig.Cb(n)       = addNewPositionCallback(Fig.LineH(n), @(pos)UpdateLine(pos));
%     Fig.CgCtx(n,:)  = get(Fig.LineH(n), 'UIContextMenu')
end

set(Fig.axh(Fig.ActiveParam+3),'color',[1,0.5,0.5]);

%================= Add timecourse GUI control elements
Fig.ParamLabels     = {'Enabled','Use image?','Scale max.','Smooth curve', 'Interpolate'};
Fig.ParamType     	= {'CheckBox','CheckBox', 'Edit','ToggleButton','PushButton'};
Fig.ParamValues     = [ones(numel(Params),3), zeros(numel(Params),2)];
set(Fig.axh(2:end), 'units', 'pixels');
for n = 1:numel(Params)
    TCpos = get(Fig.axh(n+3), 'position');
    Xpos  = TCpos(1)+TCpos(3)+10;
    for i = 1:numel(Fig.ParamLabels)
        Fig.ParamsInputPos{i}       = [Xpos, TCpos(2)+((i-1)*20), 100, 20];
        Fig.GUI.ParamInputH(n,i)    = uicontrol('Style', Fig.ParamType{i}, 'String', Fig.ParamLabels{i}, 'value', Fig.ParamValues(n,i), 'HorizontalAlignment','Left','pos',Fig.ParamsInputPos{i},'parent',Fig.fh,'Callback',{@ParamsSelect,n,i});
    end
end

%================= Add GUI control elements
Fig.Slider.Step     = [1/(Mov.NoFrames-1), 10/(Mov.NoFrames-1)];
set(Fig.axh(1), 'units','pixels');
FramePos            =  get(Fig.axh(1),'position');
Fig.Slider.Pos      = [FramePos([1,2,3]),20]-[0 20 0 0];
Fig.SliderHandle    = uicontrol('Style','slider','SliderStep',Fig.Slider.Step,'HorizontalAlignment','Left','pos',Fig.Slider.Pos,'Callback',{@NextFrame},'parent',Fig.fh);
Fig.GUI.BoxPos      = [50,50,800, 100];
Fig.GUI.LabelDim    = [100 25];
Fig.GUI.Labels      = {'Load movie','Load parameters','Save movie','Save audio','Save parameters','Copy prev.'};
Fig.GUI.InputStyles = {'pushbutton','pushbutton', 'pushbutton', 'pushbutton','pushbutton','pushbutton'};
Fig.GUI.handle      = uibuttongroup('Title','Options','FontSize',16,'Units','pixels','Position',Fig.GUI.BoxPos);
for i = 1:numel(Fig.GUI.Labels)
 	Fig.GUI.InputPos{i}     = [20+(i-1)*(Fig.GUI.LabelDim(1)+10), 20, Fig.GUI.LabelDim];
    Fig.GUI.InputHandle(i)  = uicontrol('Style',Fig.GUI.InputStyles{i},'String',Fig.GUI.Labels{i},'HorizontalAlignment','Left','pos',Fig.GUI.InputPos{i},'parent',Fig.GUI.handle,'Callback',{@GUISelect,i});
end





end

%================== GUI input controls
function GUISelect(hObj, Evnt, Indx)
    switch Indx
        case 1
            LoadMovieClip;
        case 2
            LoadParams;
        case 3
            SaveMovie;
        case 4
            SaveWavFile;
        case 5
            SaveParams;
        case 6
            CopyLastFrame;
    end
end

%================== Param timecourse GUI controls
function ParamsSelect(hObj, Evnt, Indx1, Indx2)
global Fig Params

switch Indx2
    case 1 %============ Enable/ disable param
        Fig.ParamValues(Indx1, Indx2) = get(hObj, 'value');
        if Fig.ParamValues(Indx1, Indx2) == 1
            set(Fig.axh(Indx1+3), 'color', [1,1,1]);
            set(Fig.ParamsH(Indx1+3), 'visible', 'on');
                         
        elseif Fig.ParamValues(Indx1, Indx2) == 0
            set(Fig.axh(Indx1+3), 'color', [0.5,0.5,0.5]);
            set(Fig.ParamsH(Indx1+3), 'visible', 'off');
        end
        
    case 2 %============ Enable/ disable param from image 
         Fig.ParamValues(Indx1, Indx2) = get(hObj, 'value'); 
         if Fig.ParamValues(Indx1, Indx2) == 0
             set(Fig.LineH(Indx1), 'visible', 'off');
             
         elseif Fig.ParamValues(Indx1, Indx2) == 1
             set(Fig.LineH(Indx1), 'visible', 'on');
             
         end
        
    case 3 %============ Set scaling factor
         Fig.ParamValues(Indx1, Indx2) = str2num(get(hObj, 'string'));
         set(Fig.ParamsH(Indx1+3), 'ydata', Params(Indx1).Timecourse*Fig.ParamValues(Indx1, Indx2));
         set(Fig.axh(Indx1+3), 'ylim', [0, Fig.ParamValues(Indx1, Indx2)]);
         
    case 4 %============ Smooth curve
        Fig.ParamSmoothing(Indx1) = get(hObj, 'value');
        if Fig.ParamSmoothing(Indx1) == 1
            FilterWidth = 7;
            %Params(Indx1).SmoothedTimecourse = smooth(Params(Indx1).Timecourse', FilterWidth, 'rloess')';
            Params(Indx1).SmoothedTimecourse = smoothdata(Params(Indx1).Timecourse, 'gaussian', FilterWidth);
            set(Fig.ParamsH(Indx1+3), 'ydata', Params(Indx1).SmoothedTimecourse);
        elseif Fig.ParamSmoothing(Indx1) == 0
            set(Fig.ParamsH(Indx1+3), 'ydata', Params(Indx1).Timecourse);
        end
        
end
    
end


%================== Load parameters from file (.mat or .csv)
function LoadParams
    global Params Fig Mov video
    DefaultPath   	= '/projects/murphya/MacaqueFace3D/Macaque_video/';
    [file, path]    = uigetfile({'*.csv;*.mat'}, 'Select parameters file', DefaultPath);
    if file == 0
        return;
    end
    [~,~,ext]     	= fileparts(file);
    switch ext
        case '.csv'
            Temp = csvread(fullfile(path, file), 1, 0); 
            if size(Temp, 1) ~= numel(video.frames)
                msgbox(sprintf('Warning: number of frames in parameters file (%d) does not match number of frames in current movie clip (%d)!', size(Temp, 1), numel(video.frames)));
            end
            if size(Temp, 1) < numel(video.frames)
                Temp(end+1:numel(video.frames), :) = 0;
            end
            FrameIndx = 1:numel(video.frames);
            for n = 1:size(Temp, 1)
                Params(n).Timecourse = Temp(FrameIndx,1+n);
                Params(n).LinePoints = Temp(FrameIndx,1+n);
                set(Fig.ParamsH(n+3), 'ydata', Params(n).Timecourse);
                setPosition(Fig.LineH(n), [Params(n).LinePoints(1:2,Mov.CurrentFrame), Params(n).LinePoints(3:4,Mov.CurrentFrame)]);
            end
            
        case '.mat'
            Temp    = load(fullfile(path, file));
            if ~strcmp(Mov.Filename, Temp.Mov.Filename)
                msgbox(sprintf('Movie name of selected parameters (%s) does not match current movie file (%s)! Aborting parameter import.', Temp.Mov.Filename, Mov.Filename));
                return
            end
            Params  = Temp.Params;
            
    end
    
end

%==================
function CopyLastFrame
    global Fig Params Mov
    if Mov.CurrentFrame > 1
        Fig.ActiveParam
        Params(Fig.ActiveParam).LinePoints(:,Mov.CurrentFrame) = Params(Fig.ActiveParam).LinePoints(:,Mov.CurrentFrame-1);
        Params(Fig.ActiveParam).Timecourse(Mov.CurrentFrame) = Params(Fig.ActiveParam).Timecourse(Mov.CurrentFrame-1);
        setPosition(Fig.LineH(Fig.ActiveParam), [Params(Fig.ActiveParam).LinePoints(1:2,Mov.CurrentFrame), Params(Fig.ActiveParam).LinePoints(3:4,Mov.CurrentFrame)]);
    end
end

%================== 
function UpdateLine(LinePos)
    global Params Fig Mov

    n = Fig.ActiveParam;
    if Fig.ParamValues(n,2) == 1
        Params(n).LinePoints(:,Mov.CurrentFrame) = reshape(getPosition(Fig.LineH(n)),[4,1]);
        Params(n).Timecourse = vectordiff(Params(n).LinePoints);
    end
    set(Fig.ParamsH(n+3), 'ydata', Params(n).Timecourse);

% 	n = find(get(gca,'uicontextmenu')==Fig.CgCtx)
%     n = Indx;
%     LinePos = getPosition(Fig.LineH(n))
%     Params(n).LinePoints(1:2,Mov.CurrentFrame) = LinePos(:,1);
%     Params(n).LinePoints(3:4,Mov.CurrentFrame) = LinePos(:,2);

end

%================== Calculate distance between two points
function out = vectordiff(LinePoints)
    out = sqrt((LinePoints(1,:)-LinePoints(2,:)).^2 + (LinePoints(3,:)-LinePoints(4,:)).^2);
    out = (out-min(out))/range(out);
end

%================== Load movie clip
function LoadMovieClip()
    global Mov Fig Params audio video
    if ismac Prefix = '/Volumes'; else Prefix = []; end
    Mov.DefaultPath  	= fullfile(Prefix, '/projects/murphya/MacaqueFace3D/ExpressionDynamics/');
    [file, path, ext]   = uigetfile('*.avi;*.mov;*.mp4;*.mpg;*.wmv', 'Select movie clip', [Mov.DefaultPath,'OriginalMovies/']);
    Mov.FullFilename  	= fullfile(path, file);  
  	[~,Mov.Filename]   	= fileparts(Mov.FullFilename);
    
    try	 %=============== Try method 1: mmread.m
    	[video, audio]      = mmread(Mov.FullFilename, [],[],[],false);                    % Load movie file and audio
        Mov.NoFrames        = numel(video.frames);
        Mov.FPS             = video.rate;
        
    catch %=============== Try method 2: videoreader.m
        videoobj          	= VideoReader(Mov.FullFilename);
        AudioFilename       = fullfile(Mov.DefaultPath, 'OriginalWAVs', [Mov.Filename,'.wav']);
        if ~exist(AudioFilename, 'file')
            error('Audio file ''%s'' does not exist!', AudioFilename);
        end
      	aud                 = audioread(AudioFilename);                     % < Only works for .mp4 movie files
        audio.data          = aud;
        audio.rate          = round(size(audio.data,1)/videoobj.Duration);
        Mov.FPS             = videoobj.FrameRate;
        video.width         = videoobj.width;
        video.height        = videoobj.height;
        f = 1;
        while hasFrame(videoobj)
            video.frames(f).cdata = readFrame(videoobj);
            f = f+1;
        end
        Mov.NoFrames        = numel(video.frames);
    end
    Mov.FrameTimes     	= linspace(0, (Mov.NoFrames-1)/Mov.FPS, Mov.NoFrames);
    Mov.FrameNumbers    = 1:1:Mov.NoFrames;
    Mov.CurrentFrame    = 1;
    for n = 1:numel(Params)
        Params(n).Timecourse   = nan(1, Mov.NoFrames);
    end

    if exist('Fig','var') && isfield(Fig,'fh') && ishandle(Fig.fh)
        set(Fig.imh, 'cdata', video.frames(1).cdata);
        set(Fig.th,'string',sprintf('Frame %d', 1));
        set(Fig.fn,'string',sprintf('%s', strrep(Mov.Filename,'_',' ')));
    end
end

%================== Save parameters for Python import in Blender
function SaveParams(hObj, Evnt, Indx)
    global Params Mov Fig
%     Default = fullfile(Mov.DefaultPath, [Mov.Filename, '.mat']);
%     [file, path]   = uiputfile('*.mat','Save parameters', Default);
%     save(fullfile(path,file), 'Params','Mov');
    FileTypes       = {'.mat','.csv'};
   	Default         = fullfile(Mov.DefaultPath, 'ExtractedParams', [Mov.Filename, '.csv']);
    [file, path]    = uiputfile({'*.csv';'*.mat'},'Save parameters', Default);
    if file == 0
        return;
    end
    [~,file,ext]       = fileparts(file);
    for f = 1:numel(FileTypes)  %=========== Save in all requested formats
        ext = FileTypes{f};
        switch ext
            case '.csv'         %=============== Write to .csv file (read by Python)
                CsvData         = zeros(Mov.NoFrames, numel(Fig.Headers));
                CsvData(:,1)    = Mov.FrameTimes;
                CvsColumns      = [4,6,5,8,2,9];
                for n = [1,3,4,5,6]
                    if Fig.ParamSmoothing(n) == 1
                        TC = Params(n).SmoothedTimecourse;
                    elseif Fig.ParamSmoothing(n) == 0
                        TC = Params(n).Timecourse;
                    end
                    if Fig.ParamValues(n,1) == 1
                        CsvData(:,CvsColumns(n))    = TC*Fig.ParamValues(n,3); % Jaw
                    end
                end
                if Fig.ParamSmoothing(2) == 1
                    TC = Params(2).SmoothedTimecourse;
                elseif Fig.ParamSmoothing(2) == 0
                    TC = Params(2).Timecourse;
                end
                if ~isempty(strfind(lower(Mov.Filename), 'scream'))                 % Scream = Fear
                    CsvData(:,6)    = TC*Fig.ParamValues(2,3);
                elseif ~isempty(strfind(lower(Mov.Filename), 'coo'))                % Coo = Kiss
                    CsvData(:,3)    = TC*Fig.ParamValues(2,3);
                else                                                                % Pant/ Grunt = Fear
                    CsvData(:,6)    = TC*Fig.ParamValues(2,3);
                end
                writetable(cell2table([Fig.Headers; num2cell(CsvData)]), fullfile(path,[file,'.csv']), 'writevariablenames', 0);

            case '.mat'     %=============== Write to .mat file (for re-use in Matlab)
                save(fullfile(path,[file,'.mat']), 'Mov','Params');

        end
    end
end

%================== SelectParam
function SelectParam(hObj, Evnt, Indx)
    global Fig Params Mov
    
    set(Fig.axh(3+find(Fig.ParamValues(:, 1))), 'color', [1,1,1]);
    set(Fig.axh(3+find(Fig.ParamValues(:, 1)==0)), 'color', [0.5,0.5,0.5]);
    set(Fig.axh(Indx+3), 'color', [1,0.5,0.5]);
    Fig.ActiveParam = Indx;
    for n = 1:numel(Params)
        setColor(Fig.LineH(n), Fig.LineColors(n,:));
    end
    setColor(Fig.LineH(Fig.ActiveParam), Fig.LineColors(Fig.ActiveParam,:));
    
    if Fig.ParamValues(Indx, 2) == 0                                % If image tracking is disabled...
        CP = get(Fig.axh(Indx+3), 'CurrentPoint');                  % Get mouse click coordinates
        NearestFrame = round(CP(1,1));                             
        Params(Indx).Timecourse(NearestFrame) = CP(1,2);            % Assign y-value to nearest frame
        set(Fig.ParamsH(Indx+3), 'ydata', Params(Indx).Timecourse*Fig.ParamValues(Indx, 3));
    end
end

%================== Export audio as .wav file
function SaveWavFile(hObj, Evnt, Indx)
    global Mov audio
    WavFilename     = fullfile(Mov.DefaultPath, 'OriginalWAVs', [Mov.Filename, '.wav']);
    [file, path]   = uiputfile('*.wav','Save audio', WavFilename);
    audiowrite(fullfile(path, file), audio.data, audio.rate, 'BitsPerSample', audio.bits);
end

%================== Advance frame
function NextFrame(hObj, Evnt, Indx)
    global Fig video Mov Params
    Mov.CurrentFrame = round(get(hObj, 'value')*(Mov.NoFrames-1)+1);
    set(Fig.imh, 'cdata', video.frames(Mov.CurrentFrame).cdata);
    set(Fig.th, 'string', sprintf('Frame %d', Mov.CurrentFrame));
    set(Fig.plh, 'xdata', repmat((Mov.CurrentFrame),[1,2]));
    for n = 1:numel(Params)
        setPosition(Fig.LineH(n), [Params(n).LinePoints(1:2,Mov.CurrentFrame), Params(n).LinePoints(3:4,Mov.CurrentFrame)]);
    end
    set(Fig.axh(4:end),'xlim', [1,Mov.NoFrames]);
end

%================== Render summary movie file
function SaveMovie(hObj, Evnt, Indx)
    global video Fig Params Mov
    Fig.OutputFilename = fullfile(Mov.DefaultPath, [Mov.Filename, '_Summary']);
    [file,path] = uiputfile('*.avi', 'Save movie render', Fig.OutputFilename);
    Fig.OutputMovFilename = fullfile(path,file);
    vidObj = VideoWriter(Fig.OutputMovFilename, 'MOTION JPEG AVI');
    vidObj.FrameRate = video.rate;
    open(vidObj);
    for F = 1:numel(video.frames)
        set(Fig.imh, 'cdata', video.frames(F).cdata);
        set(Fig.th, 'string', sprintf('Frame %d', F));
        set(Fig.plh, 'xdata', repmat(F,[1,2]));
        for n = 1:numel(Params)
            setPosition(Fig.LineH(n), [Params(n).LinePoints(1:2,F), Params(n).LinePoints(3:4,F)]);
        end
        drawnow;
        frame = getframe(Fig.fh);
        writeVideo(vidObj, frame);
    end
    close(vidObj);
end