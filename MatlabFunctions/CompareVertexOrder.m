

MeshDir     = '/Volumes/Kastner/aidan/MacaqueExpressions/ExpressionTransfer/';
NeutralMesh = fullfile(MeshDir, 'BaseModelExpressions', 'M02_Neutral.obj');
ExpMesh     = fullfile(MeshDir, 'BaseModelExpressions', 'M02_Fear.obj');
TargetMesh  = fullfile(MeshDir, 'IdentityExamples', 'Average_Neutral.obj');
MeshFiles   = {NeutralMesh, ExpMesh, TargetMesh};

EdgeColor       = 'none';
Backface        = 'reverselit';
Ambient         = 0.3;                         	% Ambient light strength          
Diffuse         = 0.6;                      	% Diffuse light strength
Specular        = 0.1;                         	% Specular light strength 
SpecExp         = 2;                           	% Specular reflection exponent 
SpecCol         = 1;                          	% Specular light color

fh = figure;
for m = 1:3
    OldObj              = LoadOBJFile(MeshFiles{m});
    [~,MeshName]        = fileparts(MeshFiles{m});
    fprintf('Loading mesh %s...\n', MeshName);
    NewObj(m).faces        = OldObj{1}.faces'+1;                          % Copy target object's face indices
    NewObj(m).vertices     = OldObj{1}.vertices';                        % Copy edited object's vertices, and reorder them
    %NewObj(m).texcoords    = OldObj{1}.texcoords;                   % Copy target objects' texture coords
    %NewObj(m).normals      = [];
    
    %========== Plot meshes to figure
    axh(m)  = subplot(2,2,m);
    ph(m)   = patch(NewObj(m), 'facecolor', [1,1,1], 'edgecolor','none');
    axis vis3d tight off;
    daspect([1,1,1]);
    material([Ambient Diffuse Specular SpecExp SpecCol]);                   	% Set material properties
    %shading interp
    lh(m,1) = camlight('headlight');                                          % Add headlight at camera position
    lh(m,2) = light('Position',[-1 0 5],'Style','infinite');                  % Add 
    
    if m == 1
        title('Neutral expression', 'fontsize', 18);
        ylabel('Source Identity', 'fontsize', 18);
  	elseif m == 2
        title('Fear expression', 'fontsize', 18);
        cbh                 = colorbar;
        cbh.Label.String    = 'Dispalcement (mm)';
        cbh.Label.FontSize  = 18;
        cbh.Position        = cbh.Position + [0.05,0,0,0];
    elseif m == 3
        ylabel('Target Identity', 'fontsize', 18);
    end  
end
%linkprop(axh, {'CameraUpVector', 'CameraPosition', 'CameraTarget', 'XLim', 'YLim', 'ZLim'});



%====== Calculate dispalcement
Diff = NewObj(1).vertices - NewObj(2).vertices;
Disp = sqrt(Diff(:,1).^2+Diff(:,2).^2+Diff(:,3).^2);
for m = 1:3
    set(ph(m), 'FaceVertexCData', Disp);
    axes(axh(m));
    shading interp;
end

%====== Plot new mesh
m = 4;
NewObj(m).faces        = NewObj(3).faces;                          % Copy target object's face indices
NewObj(m).vertices     = NewObj(3).vertices*500 + Diff; 
axh(m)  = subplot(2,2,m);
ph(m)   = patch(NewObj(m), 'facecolor', [1,1,1], 'edgecolor','none');
axis vis3d tight off;
daspect([1,1,1]);
material([Ambient Diffuse Specular SpecExp SpecCol]);                   	% Set material properties
%shading interp
lh(m,1) = camlight('headlight');                                          % Add headlight at camera position
lh(m,2) = light('Position',[-1 0 5],'Style','infinite');   
set(ph(m), 'FaceVertexCData', Disp);
shading interp;
