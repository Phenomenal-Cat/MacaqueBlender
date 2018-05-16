
%========================= CompareWrappedMeshes.m ========================= 

MeshDirRaw      = '/procdata/murphya/CT/RawMeshes/';
MeshDirWrapped  = '/procdata/murphya/CT/Wrapped_meshes/';

%========== Set parameters
ViewAzmuths     = -90:45:90;
Backface        = 'reverselit';               	% Set surface mesh backface lighting
Alpha           =  1;                          	% Set surface mesh face alpha
Ambient         = 0.3;                         	% Ambient light strength          
Diffuse         = 0.6;                      	% Diffuse light strength
Specular        = 0.1;                         	% Specular light strength 
SpecExp         = 2;                           	% Specular reflection exponent 
SpecCol         = 1;                          	% Specular light color


%========== Loop through all identities
for M = 1:30                                                                    % For each identity...
    WrappedFile = wildcardsearch(MeshDirWrapped, sprintf('M%02d_*.obj', M));    % Find wrapped mesh file
    if ~isempty(WrappedFile)                                                    % If wrapped mesh exists...
        RawFile     = wildcardsearch(MeshDirRaw, sprintf('M%02d_*.obj', M));    % Find filename of raw mesh
        
        %========== Load mesh data
        obj = LoadOBJFile(RawFile{1});
        ObjRaw.Vertices = obj{1}.vertices;
        ObjRaw.Faces    = obj{1}.faces;
        
      	obj = LoadOBJFile(WrappedFile{1});
        ObjWrap.Vertices = obj{1}.vertices';
        ObjWrap.Faces    = obj{1}.faces+1;
        
%         ObjRaw  = read_wobj(RawFile{1});
%         ObjWrap = read_wobj(WrappedFile{1});
        
        %========== Plot meshes to figure
        fh = figure;
        axh(1) = subplot(1,2,1);
        ph(1) = patch(ObjRaw, 'facecolor', [1,1,1]/2, 'edgecolor','none');
        axis vis3d tight off;
        daspect([1,1,1]);
        material([Ambient Diffuse Specular SpecExp SpecCol]);                   % Set material properties
        shading interp
        lh(1) = camlight('headlight');                                          % Add headlight at camera position
        lh(2) = light('Position',[-1 0 5],'Style','infinite');                  % Add 
        
        axh(2) = subplot(1,2,2);
        ph(2) = patch(ObjWrap, 'facecolor', [1,1,1]/2, 'edgecolor','none');
        axis vis3d tight off;
        daspect([1,1,1]);
        material([Ambient Diffuse Specular SpecExp SpecCol]);                   % Set material properties
        shading interp
        lh(1) = camlight('headlight');                                          % Add headlight at camera position
        lh(2) = light('Position',[-1 0 5],'Style','infinite');                  % Add 
        linkaxes(axh);
        
        %========== Save figure as image
        for az = 1:numel(ViewAzmuths)
            view([ViewAzmuths(az), ViewElevations(el)]);
            
            
        end
    
    end
end