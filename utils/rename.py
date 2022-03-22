from hashlib import new
import os
import os.path as osp
import glob
import shutil

root_dir = '/root/hain/CVAT/data_tree/week8_final'
scene_dirs = glob.glob(osp.join(root_dir, '*'))

def mkdir_if_missing(path):
    if not osp.exists(path):
        os.makedirs(path)

for dir in scene_dirs:
    duration_dirs = sorted(glob.glob(osp.join(root_dir, dir, 'videos/*')))

    for duration_dir in duration_dirs:
        video_paths = glob.glob(osp.join(duration_dir, '*'))

        for path in video_paths:
            vid_name = osp.basename(path)
            if '25fps' not in vid_name:
                shutil.move(path, osp.join(duration_dir, 'multiple_view.mp4'))
        
        # zip_files = sorted(glob.glob(osp.join(duration_dir, '*.zip')))

        # for file in zip_files:
        #     name = osp.basename(file)
        #     new_name = name.replace('_origional', '')
            
        #     shutil.move(file, osp.join(duration_dir, new_name))

