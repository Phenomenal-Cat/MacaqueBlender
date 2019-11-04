

ViewingDistances = [100, 60];
MaxDepth        = 20;
PhysicalSize    = 11;       % Size (cm) of stimulus at ViewingDistance and 100% scale
NoDists         = 9;

figure;
for vd = 1:numel(ViewingDistances)

    %======== Calculate retinal angles
    Depths          = linspace(-MaxDepth, MaxDepth, NoDists);
    Distances       = ViewingDistances(vd)+Depths;
    Scales          = (Depths./repmat(ViewingDistances(vd), size(Depths)))+1;
    for dist = 1:numel(Distances)
        for sc = 1:numel(Scales)
            RetinalAngles(dist, sc) = atand((PhysicalSize*Scales(sc)/2)/Distances(dist))*2;
        end
    end

    %======== Plot data
    axh(vd) = subplot(numel(ViewingDistances),1,vd);
    imagesc(RetinalAngles);
    hold on;
    ph = plot(1:9, 1:9, '--.c', 'linewidth',2,'markersize', 30);
    ph2 = plot([1,9],[5,5], '-w', 'linewidth',2);
    axis xy equal tight;
    box off;
    set(gca,'tickdir','out','xtick',1:NoDists,'xticklabel',round(Scales*100),'ytick',1:NoDists,'yticklabel',Distances,'fontsize', 16);
    ylabel('Distance (cm)', 'fontsize', 20);
    if vd == numel(ViewingDistances)
        xlabel('Physical scale (%)', 'fontsize', 20);
        cbh = colorbar;
        set(cbh.Label, 'String', sprintf('Retinal angle (%s)',char(176)), 'FontSize', 18);
        colormap hot;
    end
end
linkaxes(axh);
set(axh(1),'clim',get(axh(2),'clim'));


%============ Plot stimulus space
Distances   = linspace(20, 140, 1400);
Scales      = linspace(50, 150, 1000);
for d = 1:numel(Distances)
    for s = 1:numel(Scales)
        RetAngMat(d, s) = atand((PhysicalSize*Scales(s)/100/2)/Distances(d))*2;
    end
end
ScaleRange      = [80, 66.7];
ScaleWidth      = [40, 66.7];
figure;
imagesc(Scales([1,end]), Distances([1,end]), RetAngMat);
hold on;
for vd = 1:numel(ViewingDistances)
    rh(vd) = rectangle('Position',[ScaleRange(vd), ViewingDistances(vd)-MaxDepth, ScaleWidth(vd), MaxDepth*2]);
end
axis xy equal tight;
box off;
ylabel('Distance (cm)', 'fontsize', 20);
xlabel('Physical scale (%)', 'fontsize', 20);
colormap hot;
set(gca,'clim',[min(RetinalAngles(:)), max(RetinalAngles(:))],'tickdir','out');