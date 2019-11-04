%function Bones = ReadFiducials(DataFile)

%=========================== ReadFiducials.m ==============================
% Reads in 3D-coordinates of bone/ joint fiducials saved in Slicer's .fcsv 
% format, and calculates bone lengths. Fiducial naming convention must be
% as described:
%
%==========================================================================

if nargin == 0
    DataDir     = '/Volumes/Kastner/aidan/MacaqueBodies/UCD_Data/Fiducials/';
    DataFile	= uigetfile([DataDir, '*.fcsv'], 'Select Slicer fiducial data file');
end

fid         = fopen(fullfile(DataDir, DataFile));
A           = textscan(fid, '%s%f%f%f%f%f%f%f%f%f%f%s%s%s', 'delimiter',',','Headerlines',3);
for f = 1:numel(A{1})
    Coords(f).Name          = A{12}{f};
    Coords(f).Description   = A{13}{f};
    Coords(f).XYZ_RAS       = [A{2}(f),A{3}(f),A{4}(f)];
end

AxialSkeleton   = {'Cranium', 'Spine_Cervical', 'Spine_Thoracic', 'Spine_Lumbar','Spine_Sacrum','Tail_Proximal','Tail_Trans','Tail_Distal'};
ArmBones        = {'Scapula','Humerus','Ulna','Carpal','Metacarpal','Phalanges_Prox','Phalanges_Int','Phalages_Dist'};
LegBones        = {'Femur','Tibia','Tarsal','Metatarsal','Phalanges_Prox','Phalanges_Int','Phalages_Dist'};

JointNames  	= {{'','Spine_C1'}, {'Spine_C1','Spine_C7'}, {'Spine_C7','Spine_T12'}, {'Spine_T12','Spine_L5'}, {'Spine_L5', 'Spine_S3'}, ...
                    {'Spine_S3',''}};