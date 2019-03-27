%function SaveMacaquePCA(PCAmatfile)

%========================= SavePCAmeshes.m ================================
% This function loads original mesh surface data (.obj files) from the
% specified directory, computes and saves the average mesh, performs principal
% component analysis on the set, and saves new meshes for each PC based on
% the average +/- the specified number of standard deviations.
%
% REQUIREMENTS: - LoadOBJFile.m (provided in PsychToolbox)
%               - pca.m (the Mathworks version)
%               - write_quadobj.m (an edited version of write_obj.m that
%               can handle quad polygons.
% HISTORY:
%   2017 - Written by Aidan Murphy (murphyap@nih.gov)
%==========================================================================

if ismac
    Prefix = '/Volumes';
else
    Prefix = [];
end
% if nargin == 0
    %PCAmatfile = fullfile(Prefix, 'procdata/murphya/CT/Edited Ent/AllMeshPCA.mat');
	%OriginalMeshFile    = fullfile(Prefix, '/projects/murphya/MorphBlender/BaseMesh_50K_openmouth.obj');
    %OutputDir           = fullfile(Prefix, '/projects/murphya/MacaqueFace3D/MeshMorphing/PCAmeshes_2018_v2');
    PCAmatfile          = fullfile(Prefix, 'Seagate Backup 1/NIH_Postdoc/MF3D database/PCA_N=23/AllMeshPCA_N=23.mat');
    OriginalMeshFile    = fullfile(Prefix, 'Seagate Backup 1/NIH_Postdoc/MF3D database/PCA_N=23/AverageMesh_N=23.obj');
    OutputDir           = fullfile(Prefix, 'Seagate Backup 1/NIH_Postdoc/MF3D database/PCA_N=23/');
% end
load(PCAmatfile);

%========== Load original mesh file's texture coordinates
obj             = LoadOBJFile(OriginalMeshFile);
max_pc          = 10;
SavePCA         = 1;
%range_sd_score  = [-3,-2,-1,0,1,2 3];
range_sd_score  = [-3,3];
coeff_vertex    = pca_vertex.coeff;
score_vertex    = pca_vertex.score;
exp_vertex      = pca_vertex.exp;
prefix_pcatype  = 'PCA_N=23_';
EdgeColor       = 'none';
Backface        = 'reverselit';
Ambient         = 0.3;                         	% Ambient light strength          
Diffuse         = 0.6;                      	% Diffuse light strength
Specular        = 0.1;                         	% Specular light strength 
SpecExp         = 2;                           	% Specular reflection exponent 
SpecCol         = 1;                          	% Specular light color


%% =================== Plot PCA statistics
fh(1) = figure;
plot(pca_vertex.exp(1:max_pc), 'o-b');
title('PCA Explained variance', 'fontsize', 18);
xlabel('Principal component', 'fontsize', 18);
ylabel('Variance explained (%)', 'fontsize', 18);
set(gca,'fontsize',16,'xtick',1:max_pc,'xlim',[1,max_pc]);
grid on;   

fh(2) = figure; 
plot(0:max_pc, [0; cumsum(pca_vertex.exp(1:max_pc))], 'o-b')
grid on
title('PCA Cumulative explained variance', 'fontsize', 18);
xlabel('Principal component', 'fontsize', 18);
ylabel('Cumulative variance explained (%)', 'fontsize', 18);
set(gca,'fontsize',16,'xtick',0:1:max_pc)

fh(3) = figure;
sch = scatter3(pca_vertex.score(:,1),pca_vertex.score(:,2),pca_vertex.score(:,3), 'filled');
for m = 1:size(pca_vertex.score, 1)
    mlh(m)      = line([0, pca_vertex.score(m,1)],[0,pca_vertex.score(m,2)],[0,pca_vertex.score(m,3)]);
    %PCdist(m)   = pdist([0,0,0; pca_vertex.score(m,1:3)]);
    PCdist(m)   = pdist([zeros(1, size(pca_vertex.score,2)); pca_vertex.score(m,:)]);
end
ColorScale      = cool(100);
PCdistNorm      = (PCdist-min(PCdist))/range(PCdist);
PCdistColor     = round(PCdistNorm*100);
PCdistColor(PCdistColor==0) = 1;
for m = 1:size(pca_vertex.score, 1)
    set(mlh(m), 'color', ColorScale(PCdistColor(m),:),'linewidth',2);
end
set(sch, 'cdata', ColorScale(PCdistColor,:));
axis equal
grid on
hold on
lh(1) = line(xlim, [0,0],[0,0]);
lh(2) = line([0,0],ylim, [0,0]);
lh(3) = line([0,0],[0,0], zlim);
set(lh,'color',[0 0 0]);
xlabel('PC1', 'fontsize', 18);
ylabel('PC2', 'fontsize', 18);
zlabel('PC3', 'fontsize', 18);
colormap(cool);
%cbh = colorbar;
%set(cbh, 'Ticks', [0.2:0.2:1.2], 'FontSize', 14);
set(gca,'clim',[0.2, 1.2]);
%set(cbh.Label, 'String','Euclidean Distance from Mean','FontSize', 18);

fh(4) = figure;
histogram(PCdist, 'BinEdges',0:0.1:1.4)
grid on
box off
set(gca, 'fontsize', 16, 'xlim', [0, 1.4], 'tickdir', 'out');
xlabel('Euclidean distance from mean (SD)', 'fontsize', 18);
ylabel('Number of identities', 'fontsize', 18);

% print(hf,'-depsc2',[directory_obj prefix_pcatype '_exp.eps']);
% close(hf);
score_sd = std(pca_vertex.score,1); 


h = waitbar(0, '');
figure('position', get(0,'screensize'));
axh = tight_subplot(max_pc, numel(range_sd_score), 0.02, 0.02, 0.02);
for pc = 1:max_pc                                                       % For each principal component...
    
    for num_sd = range_sd_score                                         % For each standard deviation requested...
        N           = (pc-1)*numel(range_sd_score)+find(range_sd_score==num_sd);
        name_new    = sprintf('%s_shape_PC%d_sd%d.obj', prefix_pcatype, pc, num_sd);
        waitbar(N/numel(range_sd_score)*max_pc, h, sprintf('Saving %s... (mesh %d of %d)...', name_new, N, numel(range_sd_score)*max_pc));
        pc_vertex   = Obj.MeanMesh + pca_vertex.coeff(:,:,pc).*num_sd.*score_sd(pc);   
        
        %============ Plot PCA mesh
        axes(axh(N));
        FV.vertices = pc_vertex(:,[1,3,2]);
        fh(N) = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0.5, 0.5, 0.5]*1.5, 'BackFaceLighting', Backface);
        set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
        axis vis3d tight;                                               % Turn axes off
        material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
        view(-180, 0) %<<<<<<< TEMPORARY!
        axis off
        lh(1) = camlight('headlight');                              	% Add headlight at camera position
        lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
%         if pc == 1
%             title(sprintf('SD = %d', num_sd), 'fontsize', 18);
%         end
%         if num_sd == range_sd_score(1)
%             ylabel(sprintf('PC %d', pc), 'fontsize', 18);
%         end
        
        if SavePCA == 1
            write_quadobj(fullfile(OutputDir, name_new), pc_vertex, FV.faces, obj{1}.texcoords');
            
        elseif SavePCA == 2
            
            OBJ.vertices            = pc_vertex;                % Vertices coordinates
            OBJ.vertices_texture    = obj{1}.texcoords;         % Texture coordinates 
            OBJ.vertices_normal     = [];%obj{1}.normals;     	% Normal vectors
            OBJ.vertices_point      = [];                       % Vertice data used for points and lines 
            OBJ.objects(1).type     = 'f';               
%             OBJ.objects(1).data.vertices    = FV.faces;
%             OBJ.objects(1).data.texture     = obj{1}.texcoords;
%             OBJ.objects(1).data.normal      = obj{1}.normals;

            write_wobj(OBJ, fullfile(OutputDir, name_new));
        end
        
%         fid = fopen([directory_obj, name_new '.obj'], 'w');
%         fprintf(fid,['mtllib ' name_new '.mtl\n']);
%         for i=1:size(pc_vertex,1)
%             fprintf(fid,'v %2.6f %2.6f %2.6f\n', pc_vertex(i,1), pc_vertex(i,2), pc_vertex(i,3));
%         end
%         for i=1:size(obj.vt,1)
%             fprintf(fid,'vt %1.6f %1.6f\n', obj.vt(i,1), obj.vt(i,2));
%         end
%         for i=1:size(obj.f,1)
%             fprintf(fid,'f %1.0f/%1.0f/ %1.0f/%1.0f/ %1.0f/%1.0f/ \n', obj.f(i,1), obj.f(i,2), obj.f(i,3), obj.f(i,4), obj.f(i,5), obj.f(i,6));
%         end
%         fclose(fid);
% 
%         disp(['   Saving ' name_new '.mtl']);    % material library file
%         fid = fopen([directory_obj name_new '.mtl'], 'w');
%         fprintf(fid,['newmtl ' mat_obj.name '\n']);
%         fprintf(fid,['Ka ' num2str(mat_obj.ka) '\n']);
%         fprintf(fid,['Kd ' num2str(mat_obj.kd) '\n']);
%         fprintf(fid,['Ks ' num2str(mat_obj.ks) '\n']);
%         fprintf(fid,['d '  num2str(mat_obj.d)  '\n']);
%         fprintf(fid,['Ns ' num2str(mat_obj.ns) '\n']);
%         fprintf(fid,['illum ' num2str(mat_obj.illum) '\n']);
%         fprintf(fid,['map_Kd ' 'mean.jpg' '\n']);
%         fclose(fid);
% 
%         disp(['   Saving ' name_new '.jpg']);    % material texture file
%         new_texture = uint8(zeros([1024 1024 3]));
%         new_texture(200:1000,150:1024-150,:) = mean_texture;
%         imwrite(uint8(new_texture), [directory_obj name_new '.jpg']);
    end
end
delete(h);
