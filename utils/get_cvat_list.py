import os
import os.path as osp
import pandas as pd
import glob

root = '/root/hain/MTMC_Select_Data/MTMC_Select_Data/selected_data_v2'
scene_ids = ['3b']

vid_dirs = [osp.join(root, scene_id, 'videos') for scene_id in scene_ids]

for vids_root in vid_dirs:
    # vids_root = '/home/ailab/hain/code/mtmc_collect_data/MTMC_Select_Data/video_segments/10a/videos'
    scene_id = vids_root.split('/')[-2]
    out_path = 'dataset/{}.csv'.format(scene_id)

    path_list = []

    segment_dirs = sorted(glob.glob(osp.join(vids_root, '*')))

    for dir in segment_dirs:
        vid_paths = sorted(glob.glob(osp.join(dir, '*.mp4')))
        path_list.extend(vid_paths)

    # for path in path_list:
    #     print(path)

    df = pd.DataFrame(path_list, columns = ["video_paths"])

    df.to_csv(out_path, index=False)
