%========================= GenerateBlendSwarm.m ===========================
% This Matlab script generates a temporary .swarm file for submitting
% multiple frame Blender rendering jobs to the Biowulf swarm system. The
% .blend file should be setup with all desired parameters prior to job
% submission, including:
%       * CPU rendering selected
%       * placeholder file creation selected
%       * overwrite deselected
%


%========= User settings
BlendFile       = 'ShadyBrook_flythrough.blend';
PythonScript    = [];
Frames          = 2:2:600;
OutputFormat    = 'PNG';
FrameNameform   = 'ShadyBrook_V1_frame';
BundleSize      = 10;                               % Bundle jobs with more frames
MemGb           = 128; 
CPUs            = '32';%'${SLURM_CPUS_ON_NODE}';

%========= Check inputs
if ~exist(BlendFile, 'file')
    error('Blend file ''%s'' not found in current directory!', BlendFile);
end
NoJobs      = numel(Frames);
if NoJobs > BundleSize
    BundleCmd = sprintf('-b %d', BundleSize);
else
    BundleCmd = '';
end
if MemGb > 248
    Partition = '--partition largemem';
else
    Partition = '';
end
if ~isempty(PythonScript)
    if exist(PythonScript, 'file')
        PyCmd = sprintf('--python %s', PythonScript);
    else
        error('Python script ''%s'' not found!', PythonScript);
    end
else
    PyCmd = '';
end

%========= Create swarm file
SwarmFile    = 'BlenderSwarm.swarm';
fid         = fopen(SwarmFile, 'w');
fprintf(fid, 'module load blender\n');
for f = 1:numel(Frames)
    fprintf(fid, 'blender -t %s -noaudio --background %s --render-output //run/%s --render-format %s --render-frame %d\n', CPUs, BlendFile, FrameNameform, OutputFormat, Frames(f));
end
54/6
fclose(fid);

%========= Submit swarm job
!module load blender
%eval(sprintf('!swarm -f %s -g %d -t auto %s %s --module blender', SwarmFile, MemGb, Partition, BundleCmd));
eval(sprintf('!swarm -f %s -g %d -t auto %s --module blender', SwarmFile, MemGb, BundleCmd));
pause(2);
!sjobs