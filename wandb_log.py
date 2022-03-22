import wandb                                                                                                                    
run = wandb.init(project = 'YOLOv5', tags = ['log MTMC annotation tasks'])
run.name = 'log MTMC annotation tasks'
infer_new = wandb.Artifact('MTMC_annotation_tasks', type='MTMC')   

infer_new.add_dir('/root/hain/CVAT/data_tree/week8_final/temp')

run.log_artifact(infer_new)