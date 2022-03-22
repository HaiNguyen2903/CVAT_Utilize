import zipfile
import os
import glob
import os.path as osp
import shutil
 
def unzip_file(zip_file, out_dir):
    zipname = osp.basename(zip_file)

    with zipfile.ZipFile(zip_file) as z:
        # z.extractall(out_path)
        z.extract('gt/gt.txt', 
                path=(out_dir))
        print("Extracted {}".format(zipname))

def mkdir_if_missing(path):
    if not osp.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

if __name__ == '__main__':
    scene_ids = ['10d', '5a']
    for scene_id in scene_ids:
        parent = f'/root/hain/CVAT/data_tree/week8_p1/{scene_id}'

        root_dirs = glob.glob(osp.join(parent, '*'))

        # root_dirs = [osp.join(parent, str(dir)) for dir in duration_dirs]

        for root_dir in root_dirs:
            mix_dir = osp.join(root_dir, 'mix')
            mkdir_if_missing(mix_dir)

            for file in sorted(glob.glob(osp.join(root_dir, '*.zip'))):
                print(file)
                filename = osp.basename(file).split('.')[0]
                out_path = osp.join(root_dir, filename)
                unzip_file(file, out_path)

                shutil.copy(osp.join(out_path, 'gt/gt.txt'),
                            osp.join(mix_dir, '{}.txt'.format(filename)))
            