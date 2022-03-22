import subprocess
import os 
import glob 
import argparse
import getpass 
import pandas as pd
from collections import defaultdict
import json
import os.path as osp

def get_video_paths(file): 
    df = pd.read_csv(file)

    paths = list(df['video_paths'])

    return paths
    
def get_task_ids(file):
    df = pd.read_csv(file)

    task_ids = list(df['task_ids'])

    return task_ids

def create_task(args): 
    auth_account = f"{args.user_name}:{args.password}"
    
    video_paths = get_video_paths(args.csv_file)
    
    for video_path in video_paths: 
        name = video_path.split('/')[-1][0:-4]
        task_name = "{} {}".format(args.task_prefix, name)
        # print(task_name)
            
        subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", auth_account, "create", task_name, "--project_id", str(args.project_id), args.resource_type, video_path])

def delete_tasks(task_ids, args): 
    '''
    args: list of task ids
    '''
    # auth_account = f"{args.user_name}:{args.password}"

    # subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", auth_account, "delete", \
    #                 task_ids])

    subprocess.call(['python', 'cvat/utils/cli/cli.py', "delete", \
                    task_ids])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user_name", type=str, help="name of user to login", default="hain")
    ap.add_argument("--password", type=str, help="password to login", default=getpass.getpass())
    ap.add_argument("--project_id", type=int, help="id of project which contains task", required = True, default = 1)

    args = ap.parse_args()

    id_list = [str(id) for id in range(261, 305)]

    delete_tasks(id_list, args)