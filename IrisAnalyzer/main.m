w_dir = 'C:\Users\jmidv\Documents\Fall 2018\EECS 395 - Biometrics\Assignments\HW2\Iris\LG2200-2010-04-27_29\2010-04-27_29\';
d1 = dir(w_dir);
count = 1;
for i = 110:length(d1)
    curr_path = strcat(w_dir, d1(i).name);
    disp(curr_path)
    cp_left = strcat(curr_path, '\left_eyes\');
    files = dir(fullfile(cp_left, '*.tiff'));
    for j = 1:length(files_left) % first 3 images for now
        curr_folder = strcat(files(j).folder,   '\');
        curr_image = strcat(curr_folder, files(j).name);
        disp(curr_image);
        [a,b] = createiristemplate(strcat('', curr_image));
    end
    cp_right = strcat(curr_path, '\right_eyes\');
    files = dir(fullfile(cp_right, '*.tiff'));
    for j = 1:length(files_left) % first 3 images for now
        curr_folder = strcat(files(j).folder,   '\');
        curr_image = strcat(curr_folder, files(j).name);
        disp(curr_image);
        [a,b] = createiristemplate(strcat('', curr_image));
    end
    disp(count);
    count = count + 1;  

end
disp(count)
    