root="/root/SALSA_DATASET/video"
                                              
for vid_path in "$root"/*.avi                                   
    do                                                                  
        name="$(basename -- $vid_path)"                                 
        ffmpeg -i $vid_path -c:v copy -c:a copy -y $root/${name:0:-4}.mp4
    done