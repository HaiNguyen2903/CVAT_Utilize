import os.path as osp
import glob
from annotation_postprocess.utils import *

root = '/root/hain/CVAT/CONCAT_DURATIONS_V2'

scene_dirs = sorted(glob.glob(osp.join(root, '*')))

for scene in scene_dirs:
    duration_dirs = sorted(glob.glob(osp.join(scene, 'MOT_gt_processed/*')))
    for duration_dir in duration_dirs:
        view_dirs = sorted(glob.glob(osp.join(duration_dir, '*')))
        for view_dir in view_dirs:
            gt_dir = osp.join(view_dir, 'gt')
            zip_dir(src_dir=view_dir, out_zip=gt_dir)
            # name = osp.basename(view_dir)
            # if 'zip' in name:
            #     os.remove(view_dir)
