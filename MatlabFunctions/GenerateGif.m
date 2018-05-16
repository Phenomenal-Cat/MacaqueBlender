

% GenerateWigglogram.m

OutputFile      = 'PCAs_1-5.gif';
Axh             = gca;
Fh              = gcf;
NoFrames        = 120;
TotalAngle      = 60;
AnglePerFrame   = TotalAngle*2/NoFrames;
[Az, El]        = view;
Azmuths         = [linspace(Az, Az+TotalAngle-AnglePerFrame, NoFrames/2), linspace(Az+TotalAngle, Az+AnglePerFrame, NoFrames/2)];

for f = 1:NoFrames
	view(Azmuths(f), El);
    Frame = getframe(Fh);
  	[imind,cm]  = rgb2ind(Frame.cdata, 256);

    if f == 1
        imwrite(imind, cm, OutputFile, 'gif', 'Loopcount', inf, 'DelayTime', 0.00);
    else
        imwrite(imind, cm, OutputFile, 'gif','WriteMode','append', 'DelayTime', 0.00);
    end
end


writerObj = VideoWriter(OutputFile, 'MPEG-4');
open(writerObj);
for f = 1:NoFrames
	view(Azmuths(f), El);
    Frame = getframe(Fh);
  	writeVideo(writerObj, Frame.cdata);
end
close(writerObj);


%% ===========
% 
% StimDir     = '/Volumes/PROJECTS/murphya/MacaqueFace3D/GazeExperiments/Renders/EyesOnly';
% OutputFile  = '/Volumes/PROJECTS/murphya/MacaqueFace3D/GazeExperiments/Renders/MacaqueGazeDemoEyes.gif';
% 
% Hazs    = -25:5:25;
% Gazs    = Hazs;
% Imsize  = [1080, 1080];
% nx      = (1920/2)-(1080/2)+1;
% nx2     = 1920 - 420;
% 
% 
% % Hazs = [-25:5:25, 20:-5:-25];
% Hels = [0];%[-20:10:20];
% Gels = Hels;
% 
% TotalFrames = numel(Hazs)*numel(Gazs);
% for Haz = 1:numel(Hazs)
%     for Hel = 1:numel(Hels)
%         fprintf('%.1f %% complete...\n', Haz/numel(Hazs)*100);
%     %     Gazs = -Hazs(Haz);
%         for Gel = 1:numel(Gels)
%             for Gaz = 1:numel(Gazs)
%                 Filename    = sprintf('MacaqueGaze_EYes_Neutral_Haz%d_Hel%d_Gaz%d_Gel%d_dist0.png', Hazs(Haz), Hels(Hel), Gazs(Gaz), Gels(Gel));
%                 im          = imread(fullfile(StimDir, Filename));
%                 im          = im(:, nx:nx2, :);                      % Crop image
%                 [imind,cm]  = rgb2ind(im,256);
% 
%                 if Haz == 1 && Hel == 1 && Gaz == 1 && Gel == 1
%                     imwrite(imind, cm, OutputFile, 'gif', 'Loopcount', inf, 'DelayTime', 0.05);
%                 else
%                     imwrite(imind, cm, OutputFile, 'gif','WriteMode','append', 'DelayTime', 0.05);
%                 end
% 
%             end
%         end
%     end
% end