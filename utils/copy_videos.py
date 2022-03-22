import os
import os.path as osp
import glob
import shutil

src_root = '/root/hain/MTMC_Select_Data/MTMC_Select_Data/selected_data'
out_root = '/root/hain/CVAT/week7_annotate_210222_270222'

scene_dirs = sorted(glob.glob(osp.join(out_root, '8d')))

for scene_dir in scene_dirs:
    duration_dirs = sorted(glob.glob(osp.join(scene_dir, 'MOT_gt_original/*')))
    scene_id = osp.basename(scene_dir)

    for duration_dir in duration_dirs:
        duration_id = osp.basename(duration_dir)
        src_video_dir = osp.join(src_root, scene_id + '_25fps', 'videos', duration_id)
        out_video_dir = osp.join(out_root, scene_id, 'videos', duration_id)
        shutil.copytree(src_video_dir, out_video_dir)
