import os
import os.path as osp
import glob
import pandas as pd
import numpy as np
from annotation_postprocess.utils import *
from annotation_postprocess.config import *

if __name__ == '__main__':
    # data_root = 'CONCAT_DURATIONS_V2'
    # scene_dirs = glob.glob(osp.join(data_root, '*'))
    # vid_list = []
    # for scene in scene_dirs:
    #     duration_dirs = sorted(glob.glob(osp.join(scene, 'MOT_gt_processed/*')))
    #     for duration_dir in duration_dirs:
    #         duration_id = osp.basename(duration_dir)
    #         # if its concated duration
    #         if '-' in duration_id:
    #             vid_paths = sorted(glob.glob(osp.join(scene, 'videos', duration_id, '*.mp4')))
    #             vid_list.extend(vid_paths)

    
    # gt_list = []
    # for scene in scene_dirs:
    #     duration_dirs = sorted(glob.glob(osp.join(scene, 'MOT_gt_processed/*')))
    #     for duration_dir in duration_dirs:
    #         duration_id = osp.basename(duration_dir)
    #         if '-' in duration_id:
    #             view_dirs = sorted(glob.glob(osp.join(duration_dir, '*')))
    #             for view_dir in view_dirs:
    #                 gt_dir = osp.join(view_dir, 'gt')
    #                 view_id = osp.basename(view_dir)

    #                 gt_list.append(osp.join(view_dir, 'gt.zip'))

    #                 zip_dir(src_dir=view_dir, out_zip=gt_dir)

    # start = 325
    # end = 382

    # ids = []

    # for id in range(start, end + 1):
    #     ids.append(id)
    
    # ids = np.array(ids).reshape(-1,1)
    # gt_list = np.array(gt_list).reshape(-1,1)

    # data = np.concatenate((ids, gt_list), axis=1)

    # df = pd.DataFrame(data = data, columns = ['task_ids', 'annotation_paths'])

    # df = pd.DataFrame(vid_list, columns=['video_paths'])
    # df.to_csv('test_concat_gt.csv', index=False)

    df = pd.read_csv('test_concat_gt.csv')
    anno_paths = df['annotation_paths'].to_list()
    anno_paths = np.array(anno_paths).reshape(-1,1)
    start = 325
    end = 382
    ids = [id for id in range(start, end+1)]
    ids = np.array(ids).reshape(-1,1)

    data = np.concatenate((ids, anno_paths), axis=1)

    df = pd.DataFrame(data = data, columns = ['task_ids', 'annotation_paths'])
    df.to_csv('test_concat_gt_2.csv', index=False)

    print(anno_paths)

        
