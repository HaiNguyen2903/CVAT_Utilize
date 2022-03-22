from heapq import merge
import json
import os 
import os.path as osp
from config import *
from utils import *
import argparse
import glob

def mkdir_if_missing(dir_path):
    if not os.path.exists(dir_path):
        print("Make dir in {}".format(dir_path))
        os.makedirs(dir_path)

def get_view_id(bbox, view_shape=VIEW_SHAPE):
    # each view is define as left top and width height
    # return view id
    width, height = view_shape

    view_coordinates = {
        "view_1": {"left":0,"top":0,"width":width,"height":height},
        "view_2": {"left":width,"top":0,"width":width,"height":height},
        "view_3": {"left":0,"top":height,"width": width,"height":height},
        "view_4": {"left":width,"top":height,"width":width,"height":height},
    }

    bbox_left, bbox_top, bbox_width, bbox_height = bbox

    # handle view 1 and view 2
    if bbox_top < view_coordinates["view_3"]["top"]:
        if bbox_left < view_coordinates["view_2"]["left"]:
            return 1
        else:
            return 2
    else:
        if bbox_left < view_coordinates["view_4"]["left"]:
            return 3
        else:
            return 4

def get_original_coordinate(bbox, view_id, view_shape):
    width, height = view_shape

    left, top = bbox[0], bbox[1]

    if view_id == 2:
        left = left - width
        bbox[0] = left
    if view_id == 3: 
        top = top - height
        bbox[1] = top
    if view_id == 4: 
        left = left - width
        top = top - height
        bbox[0], bbox[1] = left, top

    return bbox

def get_global_id(obj_list, id_groups):
    """
    Args:
        obj_list: list of objects in 1 view 
        id_groups: a dict where keys are group id and
                    values are ids in that group
    Return: 
        obj_list: list of object in 1 view after reid
    """
    for obj in obj_list:
        obj_id = int(obj[1])

        for idx, group_id in enumerate(id_groups.values()):
            if obj_id in group_id:
                obj_id = idx + 1
                obj[1] = obj_id
                break

    return obj_list

def get_view_objects(merge_gt, view_shape):
    # get object for each view
    view_objects = {
        "view_1": [],
        "view_2": [],
        "view_3": [],
        "view_4": []
    }

    # get a dictionary, where keys are group id and values are tracking id 
    groups = {}

    with open(merge_gt, 'r') as f: 
        data = json.load(f)

    for item in data["items"]:
        frame_id = item['id']
        frame_id = str(int(frame_id.split('_')[1]) + 1)

        obj_list = item["annotations"]

        for obj in obj_list: 
            track_id = obj["attributes"]["track_id"]
            group_id = obj["group"]

            bbox = obj["bbox"]

            view_id = get_view_id(bbox=bbox)

            bbox = get_original_coordinate(bbox, view_id, view_shape)

            # append id to corresponding group
            if group_id not in groups: 
                groups[group_id] = [track_id]   
            else:
                if track_id not in groups[group_id]:
                    groups[group_id].append(track_id)

            obj_info = [frame_id, str(track_id), bbox[0], bbox[1], bbox[2], 
                        bbox[3], 1, 1, 1]

            view_objects["view_{}".format(view_id)].append(obj_info)

    # get global id for each object by mapping each id in group to its 
    # index in list 

    # check if any view is empty
    empty_views = []

    for view in view_objects:
        # print('view')
        view_objects[view] = get_global_id(view_objects[view], groups)

        # if a view contains no object, then remove that view
        if len(view_objects[view]) == 0:
            empty_views.append(view)
    
    for view in empty_views:
        del view_objects[view]

    return view_objects, groups

def merge_gt_to_mot_gt(gt_zip, view_shape, save_folder):
    # root of datumaru annotation format
    gt_dir = unzip(save_folder=save_folder, zip_name=os.path.basename(gt_zip))

    zip_name=os.path.basename(gt_zip)[:-4]
    
    prefix, view_names = zip_name.split(' ')[0], zip_name.split(' ')[1]
    
    scene_id = prefix.replace('[', '')
    scene_id = scene_id.replace(']', '')

    view_names = view_names.split('_')

    duration_id = view_names[0]
    view_names = view_names[1:]

    # out_name = "{}_{}_".format(scene_id, duration_id) + '_'.join(view_names) + '_processed'

    # root output dir to save MOT gt files 
    # output_dir = osp.join(gt_dir, out_name)
    output_dir = gt_dir

    mkdir_if_missing(output_dir)

    merge_gt = osp.join(gt_dir, 'annotations/default.json')

    view_objects, id_groups = get_view_objects(merge_gt=merge_gt, view_shape=view_shape)

    for view in view_objects:
        idx = list(view_objects.keys()).index(view)

        view_dir = osp.join(output_dir, view_names[idx])

        mot_root = osp.join(view_dir, 'gt')

        mkdir_if_missing(mot_root)

        # os.mkdir(osp.join(view_dir, 'gt'))

        save_gt_path = osp.join(mot_root, "gt.txt")
        save_label_path = osp.join(mot_root, "labels.txt")

        with open(save_gt_path, 'w') as f:
            for obj in view_objects[view]:
                f.write("{},{},{},{},{},{},{},{},{}\n".format(obj[0], obj[1], 
                                                              obj[2], obj[3], 
                                                              obj[4], obj[5],
                                                              obj[6], obj[7], 
                                                              obj[8]))

        with open(save_label_path, 'w') as f:
            f.write('person')
            f.close
    
    # shutil.rmtree(osp.join(gt_dir, 'annotations'))

    #     zip_dir(src_dir=mot_root, out_zip=mot_root)

    # zip_dir(src_dir=output_dir, out_zip=output_dir)

    return output_dir + '.zip'

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    # ap.add_argument("--gt_zip", type=str, help="zip file annotation of \
    #                 multiple view", \
    #                 default="/root/hain/CVAT/week7_annotate_210222_270222/3b/MOT_gt_processed/0/[3a] 0_104124_104127_104129.zip")
    # ap.add_argument("--out_folder", type=str, help="out folder contains \
    #                  processed annotation file of each view", \
    #                 default="/root/hain/CVAT/week7_annotate_210222_270222/3b/MOT_gt_processed/0")

    ap.add_argument("--gt_dir", type=str, help="zip file annotation of \
                    multiple view", \
                    default="/root/hain/CVAT/data_tree/week8_multiple_views")
    ap.add_argument("--out_root", type=str, help="out folder contains \
                     processed annotation file of each view", \
                    default="/root/hain/CVAT/data_tree/week8_final")
    args = ap.parse_args()

    gt_root = '/root/hain/CVAT/data_tree/week8_multiple_views'

    # scene_ids = ['8d', '9a', '10a', '12a', '12b', '14b']
    scene_ids = ['5a', '10d']

    for scene_id in scene_ids:
        gt_dir = osp.join(gt_root, scene_id)

        duration_dirs = sorted(glob.glob(osp.join(gt_dir, '*')))

        for duration_dir in duration_dirs:
            duration_id = osp.basename(duration_dir)
            gt_zip = glob.glob(osp.join(duration_dir, '*.zip'))[0]

            merge_gt_to_mot_gt(gt_zip=gt_zip, view_shape=VIEW_SHAPE, 
                            save_folder=osp.join(args.out_root, duration_dir))