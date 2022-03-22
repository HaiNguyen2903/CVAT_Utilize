import zipfile
import os
import os.path as osp
from config import *
import shutil
import glob

def mkdir_if_missing(path):
    if not os.path.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

def unzip(save_folder, zip_name):
    zip_path = osp.join(save_folder, zip_name)
    # out_dir = save_folder
    # out_dir = osp.join(save_folder, zip_name[:-4])
    out_dir = osp.join(save_folder)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        
        zip_ref.extractall(out_dir)
    
    return out_dir

def zip_dir(src_dir, out_zip):
    # shutil.make_archive(out_zip, 'zip', src_dir)
     shutil.make_archive(out_zip, 'zip', src_dir)

if __name__ == "__main__":
    scene_dir = '/root/hain/CVAT/test/8d/'

    duration_dirs = sorted(glob.glob(osp.join(scene_dir, '*')))
    # dir = '/root/hain/CVAT/test/8d/3/mix'
    # out = '/root/hain/CVAT/test/8d/3/gt'
    # zip_dir(dir, out)

    for dir in duration_dirs:
        mix_dir = osp.join(dir, 'mix')
        zip_dir(mix_dir, mix_dir)