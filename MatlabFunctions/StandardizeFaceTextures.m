
%======================== StandardizeFaceTextures.m =======================
% This script loads mesh and image data for the 'Ten24 Male Pack' faces and
% extracts the RGB values for each polygon of each identity mesh, which is
% then saved to the mesh itself (rather than using UV coordinates). This
% facilitates texture morphing for experimental purposes.
%
% 11/26/2018 - Written by APM
%==========================================================================

DataDir = '/Volumes/PROJECTS/murphya/Stimuli/BlenderAssets/HumanFaces/Ten24_MalePack_Unzipped';
AllDirs = dir(DataDir);
AllIds  = {AllDirs.name};

for n = 3:4%:numel(AllIds)
    ObjFile{n}  = wildcardsearch(fullfile(DataDir, AllIds{n}, 'OBJ/SubD/'), '*.OBJ');
    TexFile{n}  = wildcardsearch(fullfile(DataDir, AllIds{n}, 'Textures/Colour/JPG/'), '*Reduction.JPG');
    Obj{n}      = LoadOBJFile(ObjFile{n}{1});
    TexIm{n}    = imread(TexFile{n}{1});
    
    TexSize         = size(TexIm{n});
    PixCoords{n}    = Obj{n}{1}.texcoords.*repmat(TexSize([1,2])', [1, size(Obj{n}{1}.texcoords, 2)]);
    FV(n).faces    	= Obj{n}{1}.quadfaces'+1;
    FV(n).vertices 	= Obj{n}{1}.vertices';
end


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


NoseVert        = 6072;                         % Vertex index number corresponding to tip of nose

figure;


subplot(2,2,1);
image(TexIm{3});
hold on;
plot(xlim, repmat(PixCoords{n}(2,NoseVert),[1,2]), '-r');
plot(repmat(PixCoords{n}(1,NoseVert),[1,2]), ylim, '-r');

subplot(2,2,2);
image(TexIm{4});
hold on;


subplot(2,2,3);
MeshH = patch(FV(3),'edgecolor','none','BackFaceLighting', Backface,'facecolor',[1,1,1]/2);
%set(MeshH, 'faceVertexCData', MeshDiff{N}');    
set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
axis vis3d tight off;                                           % Turn axes off
material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
view(-180, -90)
%shading interp
lh(1) = camlight('headlight');                              	% Add headlight at camera position
lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
hold on
plot3(FV(3).vertices(NoseVert,1), FV(3).vertices(NoseVert,2), FV(3).vertices(NoseVert,3), '.r','markersize', 20)


subplot(2,2,4);
MeshH = patch(FV(4),'edgecolor','none','BackFaceLighting', Backface,'facecolor',[1,1,1]/2);
%set(MeshH, 'faceVertexCData', MeshDiff{N}');    
set(gca,'DataAspectRatio',[1 1 1]);                             % Make axes equal
axis vis3d tight off;                                           % Turn axes off
material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
view(-180, -90)
%shading interp
lh(1) = camlight('headlight');                              	% Add headlight at camera position
lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
hold on;
plot3(FV(4).vertices(NoseVert,1), FV(4).vertices(NoseVert,2), FV(4).vertices(NoseVert,3), '.r','markersize', 20)


DistancesXYZ    = abs(FV(3).vertices - FV(4).vertices);
Distances3D     = sqrt(DistancesXYZ(:,1)^2 + DistancesXYZ(:,2)^2+ DistancesXYZ(:,3)^2);
hist(Distances3D, 100)
