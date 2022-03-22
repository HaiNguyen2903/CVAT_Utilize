import zipfile
import os
import glob
import os.path as osp
import shutil
 
def unzip_file(zip_file, out_dir):
    zipname = osp.basename(zip_file)

    with zipfile.ZipFile(zip_file) as z:
        z.extractall(out_path)
        # z.extract('gt/gt.txt', 
        #         path=(out_dir))
        print("Extracted {}".format(zipname))

def mkdir_if_missing(path):
    if not osp.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

if __name__ == '__main__':
    scene_ids = ['1b', '3b', '8d', '9a', '10a', '12a', '12b', '14b']

    for scene_id in scene_ids: 
        dir = '/root/hain/CVAT/data_tree/week8_multiple_views/{}'.format(scene_id)

        for file in sorted(glob.glob(osp.join(dir, '*.zip'))):
            filename = osp.basename(file).split('.')[0]
            out_path = osp.join(dir, filename)
            unzip_file(file, out_path)
            