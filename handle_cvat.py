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
    subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", \
                    f"{args.user_name}:{args.password}", "ls", "--json"])
    
    with open(os.path.join("static", "cvat_task", "task_exists.json"), "r") as f:
        tasks = json.load(f)
    
    tasks_exist = []
    for task in tasks:
        if(task["project_id"] == int(args.project_id)):
            tasks_exist.append(task["name"])
    return tasks_exist

def get_video_paths(file): 
    df = pd.read_csv(file)

    paths = list(df['video_paths'])

    return paths
    
def create_task(args): 
    auth_account = f"{args.user_name}:{args.password}"
    
    video_paths = get_video_paths(args.csv_file)
    
    for video_path in video_paths: 
        name = video_path.split('/')[-1][0:-4]

        # scene_id = video_path.split('/')[1]

        # task_name = f'[{scene_id}] {name}'

        task_name = "{} {}".format(args.task_prefix, name)
            
        subprocess.call(['python', 'cvat/utils/cli/cli.py', "--auth", \
                        auth_account, "create", task_name, "--project_id", \
                        str(args.project_id), args.resource_type, video_path])
               

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user_name", type=str, help="name of user to login", default="hain")
    ap.add_argument("--password", type=str, help="password to login", default=getpass.getpass())
    ap.add_argument("--resource_type", type=str, help="local|share|remote", default="local") 
    ap.add_argument("--project_id", type=int, help="id of project which contains task", 
                    required = True, default = 1)
    ap.add_argument("--csv_file", type=str, help="csv file contains all videos u want to push", 
                    default = 'temp.csv')
    ap.add_argument("--task_prefix", type=str, help="prefix of task name on CVAT", default = "[5a]")

    args = ap.parse_args()
    create_task(args)