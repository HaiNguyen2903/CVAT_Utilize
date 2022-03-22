import os
import os.path as osp
import pandas as pd
import glob

root = '/root/hain/CVAT/data_tree/week8_annotate_010322_070322'
out_path = '/root/hain/CVAT/tasks_upload/week8.csv'

# scene_dirs = sorted(glob.glob(osp.join(root, '*')))

scene_ids = ['8d', '9a', '10a', '12a', '12b', '14b']
scene_dirs = [osp.join(root, scene_id) for scene_id in scene_ids]

merge_gt_list = []

for scene_dir in scene_dirs:
    duration_dirs = sorted(glob.glob(osp.join(scene_dir, '*')))
    for dir in duration_dirs:
        merge_gt_list.append(osp.join(dir, 'merge_MOT_gt.zip'))


df = pd.DataFrame(merge_gt_list, columns = ["annotation_paths"])

df.to_csv(out_path, index=False)

# vid_dirs = [osp.join(root, scene_id, 'videos') for scene_id in scene_ids]

# for vids_root in vid_dirs:
#     # vids_root = '/home/ailab/hain/code/mtmc_collect_data/MTMC_Select_Data/video_segments/10a/videos'
#     scene_id = vids_root.split('/')[-2]
#     out_path = 'dataset/{}.csv'.format(scene_id)

#     path_list = []

#     segment_dirs = sorted(glob.glob(osp.join(vids_root, '*')))

#     for dir in segment_dirs:
#         vid_paths = sorted(glob.glob(osp.join(dir, '*.mp4')))
#         path_list.extend(vid_paths)

#     # for path in path_list:
#     #     print(path)

#     df = pd.DataFrame(path_list, columns = ["video_paths"])

#     df.to_csv(out_path, index=False)
