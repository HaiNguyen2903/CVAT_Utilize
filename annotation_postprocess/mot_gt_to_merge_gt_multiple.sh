root_dir='/root/hain/CVAT/data_tree/week8_p1'
scene_dirs=(
    '5a'
)

# ap.add_argument("--gt_dir", type=str, help="dir of  \
#                     multiple view", 
#                     default="/root/hain/CVAT/data_tree/week8_annotate_010322_070322/3b/2/mix")
#     ap.add_argument("--save_folder", type=str, help="out folder contains \
#                      processed annotation file of each view", 
#                      default="/root/hain/CVAT/data_tree/week8_annotate_010322_070322/3b/2")
#     args = ap.parse_args()

for scene in ${scene_dirs[@]}
    do
        for duration in ${root_dir}/${scene}/*
            do
                gt_dir=${duration}/mix
                save_folder=${duration}
                
                python mot_gt_to_merge_gt.py --gt_dir $gt_dir --save_folder $save_folder
            done
    done