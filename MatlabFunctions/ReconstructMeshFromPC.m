
%======================= ReconstructMeshFromPCs.m =========================
% This function plots the original meshes that went into the PCA, and
% compares them with the meshes reconstructed based on the PC coefficients
% returned for each of those meshes. Subjective visual comparison and
% quantitative statistics reveal how well the PCA decomposition captures
% the variability of the sample set.
%
%==========================================================================

if ismac
    Prefix = '/Volumes';
else
    Prefix = [];
end
PCAmatfile = fullfile(Prefix, 'procdata/murphya/CT/Edited Ent/AllMeshPCA.mat');
load(PCAmatfile);

OutputFile      = fullfile(Prefix, 'projects/murphya/MacaqueFace3D/MeshMorphing/PCAmeshes_2018/Docs/Reconstruction.gif');
PCstoUse        = 10;                           % How many PCs to use for reconstructions
PCsforGif       = 1:18;                         % How many PCs to use for reconstructions

Ambient         = 0.3;                         	% Ambient light strength          
Diffuse         = 0.6;                      	% Diffuse light strength
Specular        = 0.1;                         	% Specular light strength 
SpecExp         = 2;                           	% Specular reflection exponent 
SpecCol         = 1;                          	% Specular light color


fh  = figure('position',get(0,'screensize'));

for PCs = PCsforGif
    PCstoUse = PCsforGif(PCs);
    
    axh = tight_subplot(4,9, 0.02, 0.02, 0.01);
    for m = 1:18

        %========= Load original mesh
        FV.faces    = squeeze(Obj.AllFaces(m,:,:))'+1;
        FV.vertices = squeeze(Obj.AllVerts(m,:,:))';

        %========= Draw original mesh
        if m <= 9
            axn = m;
        else
            axn = m+9;
        end
        axes(axh(axn));
        ph(m,1) = patch(FV, 'facecolor', [1,1,1]/2, 'edgecolor','none');
        axis vis3d equal tight off;                                           % Turn axes off
        material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
        lh(1) = camlight('headlight');                              	% Add headlight at camera position
        lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
        title(sprintf('Original M%02d', m), 'fontsize', 16)

        %========= Reconstruction from PCA
        PCvals          = pca_vertex.score(m,1:PCstoUse);
        Recon_vertex    = Obj.MeanMesh;
        for pc = 1:PCstoUse
            Recon_vertex    = Recon_vertex + pca_vertex.coeff(:,:,pc)*PCvals(pc);  
        end
        FV.vertices     = Recon_vertex;

        %========= Draw reconstructed mesh5
        axes(axh(axn+9))
        ph(m,2) = patch(FV, 'facecolor', [1,1,1]/2, 'edgecolor','none');
        axis vis3d equal tight off;                                           % Turn axes off
        material([Ambient Diffuse Specular SpecExp SpecCol]);       	% Set material properties
        lh(1) = camlight('headlight');                              	% Add headlight at camera position
        lh(2) = light('Position',[-1 0 5],'Style','infinite');         	% Add 
        title(sprintf('Recon M%02d', m), 'fontsize', 16);

    end
    linkaxes(axh);
    if PCs == 1
        TitleAxh = axes('position',[0.02,0.95,0.2,0.05]);
        TextH = text(0, 0.7, sprintf('+ PC %d', PCs), 'fontsize', 22, 'FontWeight', 'bold');
        axis off;
    else
        set(TextH, 'string', sprintf('+ PC %d', PCs));
    end
    
    
    %=========== Save frame to animation
    Frame = getframe(fh);
  	[imind,cm]  = rgb2ind(Frame.cdata, 256);
    if PCs == 1
        imwrite(imind, cm, OutputFile, 'gif', 'Loopcount', inf, 'DelayTime', 0.5);
    else
        imwrite(imind, cm, OutputFile, 'gif','WriteMode','append', 'DelayTime', 0.5);
    end
    
    delete(axh);
end

