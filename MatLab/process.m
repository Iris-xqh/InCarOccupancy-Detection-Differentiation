csi_trace = read_bf_file("tet_30_1_empty_to_one_03");
for i = 1:30
    csi_entry = csi_trace{i};
    csi = get_scaled_csi(csi_entry);
    csiAll(i,:,:,:) = csi;
end
save('ssss.mat','csiAll')
figure;imagesc(db(abs(squeeze(csiAll(:,1,:)))).')
%plot(db(abs(squeeze(csi).')))
