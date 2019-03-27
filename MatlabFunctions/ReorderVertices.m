
%========================== ReorderVertices.m =============================
% Load mesh surfaces and re-order the vertices to correspond with the face
% index structure of an original target mesh.

addpath('/Volumes/PROJECTS/murphya/Matlab Code/APMSubfunctions')
addpath(genpath('/Volumes/PROJECTS/murphya/Matlab Code/APMSubfunctions/3D_rendering'))
addpath(genpath('/Volumes/PROJECTS/murphya/MacaqueFace3D/MacaqueBlender'))
MeshDir     = '/Volumes/Seagate Backup 1/NIH_Postdoc/MF3D database/CT_7_EditedMeshes';
OutputDir   = '/Volumes/Seagate Backup 1/NIH_Postdoc/MF3D database/CT_8_ReorderedMeshes';
MeshFiles   = wildcardsearch(MeshDir, 'M*_02.obj');
TargetMesh  = '/Volumes/PROJECTS/murphya/MacaqueFace3D/MeshMorphing/ObjExportTest/Macaque09_BaseMesh_KeepVertex_Translated.obj';
TargetObj  	= LoadOBJFile(TargetMesh);

load('/Volumes/PROJECTS/murphya/MacaqueFace3D/MeshMorphing/ObjExportTest/VertexOrder.mat');
PlotMeshes = 0;
for M = 1:numel(MeshFiles)
    OldObj              = LoadOBJFile(MeshFiles{M});
    [~,MeshName]        = fileparts(MeshFiles{M});
    fprintf('Ro-ordering mesh %s...\n', MeshName);
    NewObj.faces        = TargetObj{1}.faces;                     % Copy target object's face indices
    NewObj.vertices     = OldObj{1}.vertices(:,VertIndx);           % Copy edited object's vertices, and reorder them
    NewObj.texcoords    = TargetObj{1}.texcoords;                   % Copy target objects' texture coords
    NewObj.normals      = [];
    
    %======== Plot data?
    if PlotMeshes == 1
        figure;
        scatter3(TargetObj{1}.vertices(1,:), TargetObj{1}.vertices(2,:), TargetObj{1}.vertices(3,:));
        hold on;
        scatter3(OldObj{1}.vertices(1,:), OldObj{1}.vertices(2,:), OldObj{1}.vertices(3,:));
        for v = 1:size(TargetObj{1}.vertices,2)
            plot3([TargetObj{1}.vertices(1,v), OldObj{1}.vertices(1,VertIndx(v))], [TargetObj{1}.vertices(2,v), OldObj{1}.vertices(2,VertIndx(v))], [TargetObj{1}.vertices(3,v), OldObj{1}.vertices(3,VertIndx(v))], '-r');
            hold on;
        end
        
        figure('position',get(0,'screensize'));
        FV(1) = TargetObj{1};
        FV(2) = OldObj{1};
        FV(3) = NewObj; 
        FV = rmfield(FV, {'normals','texcoords','subMeshName','mtllib','usemtl'});
        MeshNames = {'Target','Edited','Reordered'};
        for n = 1:3
            subplot(1,3,n);
            FV(n).vertices          = FV(n).vertices';
            FV(n).faces             = FV(n).faces'+1;
            FV(n).FaceVertexCData   = [1:size(FV(n).faces,1)]';
            patch(FV(n));
            hold on;
            grid on;
            camlight headlight
            axis equal tight
            shading flat
            title(MeshNames{n}, 'fontsize', 18);
        end
        colormap jet
        clear FV
    end
    
    write_quadobj(fullfile(OutputDir, [MeshName, '.obj']), NewObj.vertices, NewObj.faces+1, NewObj.texcoords);
end