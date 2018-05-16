function AverageMeshes

%============================ AverageMeshes.m =============================
% This function loads multiple meshes with corresponding vertices and faces
% that allow for simple geometric averaging. 
% 

global MeshH MixPercent Obj MeshPropTxt SliderH

if ismac
    Prefix = '/Volumes';
else
    Prefix = [];
end


VertFile = 'AllOrigMorphs2.mat';
if exist(VertFile,'file')
    fprintf('Loading %s...\n', VertFile);
    load(VertFile);
else
    %MeshDir     = '/Volumes/Seagate Backup 1/NIH_PhD_nonthesis/7. 3DMacaqueFaces/MF3D_database/CT_wrapped_meshes';
    MeshDir     = '/Volumes/PROCDATA/murphya/CT/Edited Ent/';
    MeshFiles   = wildcardsearch(MeshDir, 'M*.obj');
    MeshFiles   = MeshFiles(cellfun(@isempty, strfind(MeshFiles, 'Average')));
end

%================ Settings
InteractivePlot = 0;
DoPCA           = 1;
PlotPCA         = 1;  
PlotMeshes      = 1;                          	% Plot meshes?
SaveAntiFace    = 0;    
SaveMeanFace    = 0;
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


%================ Load mesh data
OriginalMeshFile    = fullfile(Prefix, '/projects/murphya/MorphBlender/BaseMesh_50K_openmouth.obj');
obj = LoadOBJFile(OriginalMeshFile);
TexCoords = obj{1}.texcoords';

if ~exist(VertFile,'file')
    h = waitbar(0, '');
    for m = 1:numel(MeshFiles)
        waitbar( m/numel(MeshFiles), h, sprintf('Loading mesh %d of %d...', m, numel(MeshFiles)));
    %     [v, f, n] = read_obj(MeshFiles{m});
        obj = LoadOBJFile(MeshFiles{m});
        Obj.AllVerts(m, :, :) = obj{1}.vertices;
        Obj.AllFaces(m, :, :) = obj{1}.faces;
    end
    delete(h);
    Obj.MeanMesh = squeeze(mean(Obj.AllVerts))';
end

MixPercent      = zeros(1, size(Obj.AllVerts,1));
m               = 1;
MixPercent(m)   = 100;

%================ Interactive plot
if InteractivePlot == 1
    figure('position', get(0,'screensize'));

    FV.faces = squeeze(Obj.AllFaces(m,:,:))'+1;
    FV.vertices = squeeze(Obj.AllVerts(m,:,:))';
    MeshH = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0.5, 0.5, 0.5]*1.5, 'BackFaceLighting', Backface);
    set(MeshH, 'faceVertexCData', 0.5*ones(size(Obj.AllVerts,3), 3));
    set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
    axis vis3d tight off;                                           % Turn axes off
    material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
    shading interp
    lh(1) = camlight('headlight');                              	% Add headlight at camera position
    lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
        
    
    
    %========= Add GUI
    for m = 1:size(Obj.AllVerts,1)
        uicontrol('Style','text','string',sprintf('M%02d',m),'Position',[20, 50+m*30 30 20])
        SliderPos(m,:) = [50 50+m*30 120 20];
        SliderH(m) = uicontrol('Style', 'slider','Min',0,'Max',100,'Value',MixPercent(m),'Position', SliderPos(m,:), 'Callback', {@UpdateMesh, m}); 
        MeshPropTxt(m) = uicontrol('Style','text','string',sprintf('%.0f %%', (MixPercent(m)/100)/sum(MixPercent)*100), 'position', SliderPos(m,:)+[140,0,-80,0]); 
    end
    uicontrol('Style', 'togglebutton','string','Right','value',0, 'position', [50, 50, 50, 20],'callback',@RotateMeshR);
    uicontrol('Style', 'togglebutton','string','Left','value',0, 'position', [120, 50, 50, 20],'callback',@RotateMeshL);
    uicontrol('Style', 'pushbutton','string','Random','value',0, 'position', [120, 20, 50, 20],'callback',@RandomMesh);
    
end

%================ Plot each mesh
if PlotMeshes == 1
    figure('position', get(0,'screensize'));
    axh = tight_subplot(4, 5, 0.02, 0.02, 0.02);
    for m = 1:size(Obj.AllVerts,1)
        axes(axh(m));
        FV.faces    = squeeze(Obj.AllFaces(m,:,:))'+1;
        FV.vertices = squeeze(Obj.AllVerts(m,:,:))';
        fh(m)       = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0.5, 0.5, 0.5]*1.5, 'BackFaceLighting', Backface);
        set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
        axis vis3d tight off;                                           % Turn axes off
        material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
        lh(1) = camlight('headlight');                              	% Add headlight at camera position
        lh(2) = light('Position',[0 10 0],'Style','infinite');         	% Add 
        if exist('MeshFiles','var')
            [~, MeshName] = fileparts(MeshFiles{m});
            MeshName(strfind(MeshName, '_')) = ' ';
            title(MeshName, 'fontsize', 16);
        end
        
        %========= Calculate anti-faces and charicatures
        if SaveAntiFace == 1
            RawDiffs                = FV.vertices - Obj.MeanMesh;
            Obj.AntiVerts(:,:,m)    = Obj.MeanMesh - RawDiffs;
            Obj.UberVerts(:,:,m)    = FV.vertices + RawDiffs*0.5;
            Distances               = sqrt(sum(RawDiffs.^2, 2)); 

            axes(axh(m+10));
            FV.vertices = Obj.UberVerts(:,:,m);
            fh(m) = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0.5, 0.5, 0.5]*1.5, 'BackFaceLighting', Backface);
            set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
            axis vis3d tight off;                                           % Turn axes off
            material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
            lh(1) = camlight('headlight');                              	% Add headlight at camera position
            lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
            if exist('MeshFiles','var')
                [~, MeshName] = fileparts(MeshFiles{m});
                MeshName(strfind(MeshName, '_')) = ' ';
                title([MeshName ' anti-face'], 'fontsize', 16);
            end

            [a,b] = fileparts(MeshDir);
            AntiFaceFile = fullfile([a, 'AntiFaceMeshes'], sprintf('AntiFace_%s.obj', MeshName));
            write_quadobj(AntiFaceFile, Obj.MeanMesh, FV.faces);
        end
       
        AllVertsPCA(m, :) = reshape(squeeze(Obj.AllVerts(m, :, :))', [1, size(Obj.AllVerts,2)*size(Obj.AllVerts, 3)]); % Reshape vertex data for PCA
        
    end
    
    %========= Plot average mesh
%     m = m+1;
%     axes(axh(m));
%     FV.vertices = Obj.MeanMesh;
%     fh(m) = patch(FV, 'edgecolor', EdgeColor, 'facecolor', [0.5, 0.5, 0.5], 'BackFaceLighting', Backface);
%     set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
%     axis vis3d tight off;                                           % Turn axes off
% 	material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
%     lh(1) = camlight('headlight');                              	% Add headlight at camera position
%     lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add
%     title('Average mesh', 'fontsize', 16);

%     delete(axh(m+1:end));
end

%================ Save average mesh
if SaveMeanFace == 1
    MeanMeshFile = fullfile(MeshDir, sprintf('AverageMesh%d_%s.obj', numel(MeshFiles), date));
    write_quadobj(MeanMeshFile, Obj.MeanMesh, FV.faces, TexCoords);
end

%=============== Perform procrustes alignment & PCA
% BaseMesh = squeeze(Obj.AllVerts(2, :, :));
% h = waitbar(0, '');
% for m = 1:numel(MeshFiles)
%     waitbar( m/numel(MeshFiles), h, sprintf('Performing procrustes alignment (%d of %d)...', m, numel(MeshFiles)));
%     [d, Z, transform] = procrustes(BaseMesh, squeeze(Obj.AllVerts(m, :, :)));
%     Zunscaled = Y*transform.T + transform.c;
%     
%     
%     
% end
% delete(h);


%% ================ Perfrom Principal Component Analysis
if DoPCA == 1
    % AllVertsPCA = reshape(Obj.AllVerts, size(Obj.AllVerts, 1), size(Obj.AllVerts, 2)*size(Obj.AllVerts, 3));
    [coeff,score,latent,tsquared,explained,mu] = pca(AllVertsPCA);

    for n = 1:size(coeff,2)
        pca_vertex.coeff(:,:,n) = reshape(coeff(:,n), [size(coeff,1)/3, 3]);
    end
%     pca_vertex.coeff = reshape(coeff, [size(coeff,1)/3, 3, size(coeff,2)]);
    pca_vertex.score = score;
    pca_vertex.lat   = latent;
    pca_vertex.tsq   = tsquared;
    pca_vertex.exp   = explained;
    pca_vertex.mu    = mu;

    if PlotPCA == 1
        figure; 
        for n = 1:size(pca_vertex.coeff,3)
            FV.vertices = pca_vertex.coeff(:,:,n);
            subplot(4,5,n);
            ph(n) = patch(FV, 'facecolor', [1,1,1]/2, 'edgecolor','none');
            axis vis3d tight off;                                           % Turn axes off
            material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
            lh(1) = camlight('headlight');                              	% Add headlight at camera position
            lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
        end
    end
    

    if ~exist('MeshDir','var')
        MeshDir = cd;
    end
    Matfilename = fullfile(MeshDir, sprintf('AllMeshPCA.mat'));
    save(Matfilename, 'pca_vertex', 'Obj', 'FV');
end


end

%% ============================ Subfunctions ==============================
function RandomMesh(hObj, Event, h)
    global MeshH MixPercent Obj MeshPropTxt SliderH
    MixPercent = rand(size(MixPercent))*100;
    for m = 1:numel(MixPercent)
        set(SliderH(m), 'value', MixPercent(m));
    end
    UpdateMesh([],[],1);

end

function UpdateMesh(hObj, Event, h)
    global MeshH MixPercent Obj MeshPropTxt
    if ~isempty(hObj)
        MixPercent(h) = get(hObj,'Value');            % Get new blend amount
    end
    NewVerts = zeros(size(Obj.AllVerts,2), size(Obj.AllVerts,3));
    for m = 1:size(Obj.AllVerts, 1)
        NewVerts = NewVerts + squeeze(Obj.AllVerts(m,:,:))*(MixPercent(m)/100)/sum(MixPercent);
        if MixPercent(m) > 0
            set(MeshPropTxt(m), 'string', sprintf('%0.0f %%', (MixPercent(m)/sum(MixPercent)*100)));
        else
            set(MeshPropTxt(m), 'string', '');
        end
    end
 	NewVerts = NewVerts';%/size(Obj.AllVerts, 1)*sum(MixPercent/100);   	% Calculate new mesh vertices
    set(MeshH, 'vertices', NewVerts);                                   % Update mesh vertex coordinates
    
end

function RotateMeshR(hObj, Event, h)
    while get(hObj,'Value')==1
       camorbit(1,0,'camera')
       drawnow
    end
end

function RotateMeshL(hObj, Event, h)
 	while get(hObj,'Value')==1
       camorbit(-1,0,'camera')
       drawnow
    end
end

