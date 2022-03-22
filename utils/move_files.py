import os
import os.path as osp
import glob
import shutil

def mkdir_if_missing(path):
    if not osp.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

src_dir = '/root/hain/MTMC_Select_Data/MTMC_Select_Data/selected_data_v2'
dst_dir = '/root/hain/CVAT/data_tree/week8_final'
scene_ids = ['3b', '9a', '10a', '12a', '12b', '14b']

for scene_id in scene_ids:
    dst_durations = sorted(glob.glob(osp.join(dst_dir, scene_id, 'MOT_gt_processed/*')))
    duration_ids = [osp.basename(dst_duration) for dst_duration in dst_durations]

    for id in duration_ids:
        src_vid_dir = osp.join(src_dir, scene_id, 'videos', id)
        dst_vid_dir = osp.join(dst_dir, scene_id, 'videos', id)
        print(f"copy {src_vid_dir}")
        shutil.copytree(src_vid_dir, dst_vid_dir)




# scene_dirs = sorted(glob.glob(osp.join(root_dir, 'MOT_gt_processed', '*')))

# for scene in scene_dirs:
#     scene_id = osp.basename(scene)
#     dst_dir = osp.join(root_dir, scene_id, 'MOT_gt_processed')
#     mkdir_if_missing(dst_dir)

#     duration_dirs = sorted(glob.glob(osp.join(scene, '*')))

#     for duration_dir in duration_dirs:
#         duration_id = osp.basename(duration_dir)
#         shutil.copytree(duration_dir, osp.join(dst_dir, duration_id))






        


