import subprocess
import os 
import glob 
import argparse
import getpass 
import pandas as pd
from collections import defaultdict
import json
import os.path as osp

def preprocess(df, rename=True): 
    """rename video file cuz we convert to fixed fps"""
    if(rename):
        df["video_path"] = df["video_path"].apply(lambda x: x.replace(".mp4", "_compressed.mp4"))
        return df 
    return None
    
def get_video_cluster(file):
    df = pd.read_csv(file) 
    df_new = preprocess(df)
    if(df_new is not None):
        df = df_new 
    df = df.groupby('cluster')
    cluster_idx = df["cluster"].unique()
    video_cluster = defaultdict(list) 
    for cluster in cluster_idx:
        cluster = cluster[0]
        videos_info = df.get_group(cluster)[["video_name","video_path"]].values 
        for info in videos_info:
            video_cluster[cluster].append(tuple(info)) 
    return video_cluster

def get_task_exist(args):
    """get all tasks have been created on cvat"""
    # this subprocess will save all task have been created before in static/cvat_task/task_exists.json
    subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", f"{args.user_name}:{args.password}", "ls", "--json"])

    # with open(os.path.join("static", "cvat_task", "task_exists.json"), "r") as f:
    #     tasks = json.load(f)
    
    # tasks_exist = []
    # for task in tasks:
    #     if(task["project_id"] == int(args.project_id)):
    #         tasks_exist.append(task["name"])
    # return tasks_exist

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

def dump_task(args): 
    auth_account = f"{args.user_name}:{args.password}"
    
    task_ids = get_task_ids(args.tasks_dump)

    for task_id in task_ids:
        subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", auth_account, "dump", \
                        str(task_id), '--format', args.fileformat, args.save_root])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user_name", type=str, help="name of user to login", default="hain")
    ap.add_argument("--password", type=str, help="password to login", default=getpass.getpass())
    ap.add_argument("--project_id", type=int, help="id of project which contains task", required = True, default = 1)
    # ap.add_argument("--fileformat", type=str, help="file format", default = "MOT 1.1")
    ap.add_argument("--fileformat", type=str, help="file format", default = "Datumaro 1.0")
    ap.add_argument("--save_root", type=str, help="file format", default = "/root/hain/CVAT/data_tree/week8_multiple_views")
    ap.add_argument("--tasks_dump", type=str, help="file csv of tasks need to dump annotation", default = "/root/hain/CVAT/tasks_dump/week8_multiple_views.csv")

    args = ap.parse_args()
    # create_task(args)
    dump_task(args)
    

    '''
    ngotuananh
    damphuongnam
    phihuuchinh
    hoangthingoc
    luutienhiep
    hoangquocanh
    nguyenthihai
    '''