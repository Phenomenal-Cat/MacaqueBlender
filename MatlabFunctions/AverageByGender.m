
%% ======================== AverageByGender.m =============================
% Thsi script loads a series of 3D surfaces meshes specifying the cranio-facial 
% morphology of individual Rhesus macaques, divides them by sex and
% calculates the average surface for each gender. 'Neutral' gender and
% extreme gender versions of the mesh surface are then calculated and saved
% as new mesh (.obj) files.

if ismac, Prefix = '/Volumes'; else Prefix = []; end

%================ LOAD ORIGINAL MESHES
MeshDir     = fullfile(Prefix, '/procdata/murphya/CT/Edited Ent/');
MeshFiles   = sort_nat(wildcardsearch(MeshDir, 'M*_01.obj'));
Sex         = {'F','M','M','M','M','F','F','M','M','M','F','M','M','M','M','M','F','F','F','M','M','?','?','?','?','?','?','M','M'};
Sexes       = {'M','F'};
Scale       = 0;
Sex         = Sex(1:numel(MeshFiles));

h = waitbar(0, '');
for s = 1:numel(Sexes)
    Index = find(~cellfun(@isempty, strfind(Sex, Sexes{s})));
	for M = 1:numel(Index)
        waitbar(M/numel(Index), h, sprintf('Loading %s mesh %d of %d...', Sexes{s}, M, numel(Index)));
        obj                         = LoadOBJFile(MeshFiles{Index(M)});
        Obj(s).AllVerts(M, :, :)    = obj{1}.vertices;
        Obj(s).AllFaces(M, :, :)    = obj{1}.faces;
    end
end
delete(h);

%================ CACLULATE NEW MESHES
MeanMeshes{2} = squeeze(mean(Obj(1).AllVerts))';
MeanMeshes{4} = squeeze(mean(Obj(2).AllVerts))';

BothGenders(1,:,:)  = MeanMeshes{2};
BothGenders(2,:,:)  = MeanMeshes{4};
MeanMeshes{3}	= squeeze(mean(BothGenders));

Proportion = 2;
MeanMeshes{1} = MeanMeshes{3} + (MeanMeshes{2}-MeanMeshes{3})*Proportion;
MeanMeshes{5} = MeanMeshes{3} + (MeanMeshes{4}-MeanMeshes{3})*Proportion;

%============= Procrustes alignment
% for N = [1,2,4,5]
%     [d, MeanMeshes{N}] = procrustes(MeanMeshes{3}, MeanMeshes{N},'scaling',Scale);
% end

%============= Calculate distances
FV.vertices = MeanMeshes{3};
FV.faces    = squeeze(Obj(s).AllFaces(M,:,:))'+1;
for N = 1:numel(MeanMeshes)
    for pt = 1:size(MeanMeshes{2},1)
        MeshDiff{N}(pt) = pdist([MeanMeshes{3}(pt,:); MeanMeshes{N}(pt,:)],'euclidean');
    end
    IN	= inpolyhedron(FV, MeanMeshes{N});
    MeshDiff{N}(IN) = -MeshDiff{N}(IN);
end


%================ PLOT ALL MESHES
Background      = [1 1 1];                    	% Set background color
FaceColor       = [1 1 2]/2;                 	% Set surface mesh face color (only used if no texture provided)
EdgeColor       = 'none';%[0 0 0];%'none';     	% Set surface mesh edge color  
Backface        = 'reverselit';               	% Set surface mesh backface lighting
Alpha           =  1;                          	% Set surface mesh face alpha
Ambient         = 0.3;                         	% Ambient light strength          
Diffuse         = 0.6;                      	% Diffuse light strength
Specular        = 0.1;                         	% Specular light strength 
SpecExp         = 2;                           	% Specular reflection exponent 
SpecCol         = 1;                          	% Specular light color


figure('position', get(0,'screensize').*[1,1,1,0.5]);
axh = tight_subplot(1,5,0.02,0.02,0.02);
MeshTitles = {'Super-Male','Average Male','Average','Average Female','Super-Female'};
for N = 1:numel(MeanMeshes)
    axes(axh(N));
    FV.faces    = squeeze(Obj(s).AllFaces(M,:,:))'+1;
    FV.vertices = MeanMeshes{N}(:,[1,3,2]);
    MeshH = patch(FV, 'edgecolor', EdgeColor, 'facecolor', 'interp', 'BackFaceLighting', Backface);
    set(MeshH, 'faceVertexCData', MeshDiff{N}');    
    set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
    axis vis3d tight off;                                           % Turn axes off
    material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
    shading interp
    view(-195,14);
    lh(1) = camlight('headlight');                              	% Add headlight at camera position
    lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
    title(MeshTitles{N},'fontsize', 18);
end
set(axh, 'clim', [-0.05 0.05]);
colormap jet
linkaxes(axh);
Link = linkprop(axh, {'CameraUpVector','CameraPosition','CameraTarget'});


%% ================= Save new meshes to obj files
%export_fig('GenderFaceWarp_3D.png','-png','-m2','-transparent','-nocrop');
GenderDir       = fullfile(Prefix, '/projects/murphya/MacaqueFace3D/MeshMorphing/GenderMorph2');
Scaling         = {'Unscaled','Scaled'}; 
BaseMeshFile    = fullfile(Prefix, '/procdata/murphya/CT/Wrapped_meshes/M02_BaseMesh50K.obj'); 	% Full path of the original textured mesh at 50K polygon resolution (M02)
BaseMesh        = LoadOBJFile(BaseMeshFile);                                                    % Read the original mesh in so we can copy the UV texture coordinates
for N = 1:5
    Filename = fullfile(GenderDir, sprintf('GenderMorph_%s_%s.obj', MeshTitles{N}, Scaling{Scale+1}));
    write_quadobj(Filename, MeanMeshes{N}, FV.faces, BaseMesh{1}.texcoords);
end

%% ================= Plot meshes on-top of one another
figure;
FV.faces    = squeeze(Obj(s).AllFaces(M,:,:))'+1;
FV.vertices = MeanMeshes{4}(:,[1,3,2]);
Mesh = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [1,0,0], 'facealpha',0.5,'BackFaceLighting', Backface);
hold on;
FV.faces    = squeeze(Obj(s).AllFaces(M,:,:))'+1;
FV.vertices = MeanMeshes{2}(:,[1,3,2]);
Mesh2 = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0,0,1], 'facealpha',0.5, 'BackFaceLighting', Backface);
set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
axis vis3d tight off;                                           % Turn axes off
material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
shading interp
view(-195,14);
lh(1) = camlight('headlight');                              	% Add headlight at camera position
lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 


%% =============== Project gender average meshes into PCA space
x   = FV.vertices;
y0  = Y(1,:);    % point we should get in result
y   = (W*x')';    % our result
