import os
import os.path as osp
import math

def mkdir_if_missing(path):
    if not osp.exists(path):
        print('mkdir {}'.format(path))
        os.makedirs(path)

def find_max_frame_id(path):
    with open(path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split(",") for line in lines]
        max_frame_id = len(set([line[0] for line in lines]))
    return max_frame_id

def check_delete(frame_id, original_frames, target_frames):
    frame_diff = abs(original_frames - target_frames)

    if original_frames > target_frames:
        # delete frame after every step
        step = math.floor(original_frames / frame_diff)
        if frame_id % step == 0:
            return True
        return False

def reformat_line(line):
    # take line in array format as input
    return "{},{},{},{},{},{},{},{},{}\n".format(
        line[0], line[1], line[2], line[3], line[4], line[5], line[6], \
        line[7], line[8]
    )

def delete_frames(gt_path, original_frames, target_frames, save_folder, duration_id):
    mkdir_if_missing(save_folder)
    
    # diff frames need to be deleted
    frames_diff = abs(original_frames - target_frames)
    # delete frame after each step
    step = math.floor(original_frames / frames_diff)
    # number of frames deleted
    deleted = 0
    # list of deleted frame ids
    deleted_list = []
    # new content for annotation file
    new_content = []
    
    f = open(gt_path)
    lines = f.readlines()

    lines = [line.strip() for line in lines]

    for line in lines:
        line = line.split(',')
        frame_id = int(line[0])

        # if deleted < frames_diff:
        #     if not check_delete(frame_id, original_frames, target_frames):
        #         line[0] = str(frame_id - deleted)
        #         formatted_line = reformat_line(line)
        #         new_content.append(formatted_line)
        #     else:
        #         deleted += 1
        # else:
        #     line[0] = str(frame_id - deleted)
        #     formatted_line = reformat_line(line)
        #     new_content.append(formatted_line)

        # if frame_id > target_frames:
        #     break
        # else:

        if frame_id % step != 0:
            line[0] = str(frame_id - deleted)
            formatted_line = reformat_line(line)
            new_content.append(formatted_line)
        else:
            if deleted > frames_diff:
                line[0] = str(frame_id - deleted)
                formatted_line = reformat_line(line)
                new_content.append(formatted_line)
            else:
                if frame_id not in deleted_list:
                    print('delete frame {}'.format(frame_id))
                    deleted += 1
                    deleted_list.append(frame_id)

    out_path = osp.join(save_folder, f'[8d] 109105_{duration_id}_640x480_25fps.txt')

    print(len(deleted_list))

    with open(out_path, "w") as f:
        for line in new_content:
            f.write(line)


if __name__ == "__main__":
    root = '/root/hain/CVAT/data_tree/week8_annotate_010322_070322/8d'
    duration_id = 17
    gt_path = osp.join(root, f'{duration_id}/[8d] 109105_{duration_id}_640x480_25fps/gt/gt.txt')
    gt_file = open(gt_path)
    save_folder = osp.join(root, f'{duration_id}/mix')

    original_frames = 2318
    target_frames = 2250

    # original_frames = 2344
    # target_frames = 2275

    delete_frames(gt_path, original_frames, target_frames, save_folder, duration_id)

# def write_video(original_video, original_frames, target_frames, out_fps, save_folder):
#     frames_diff = abs(original_frames - target_frames)
#     # delete frame after each step
#     step = math.floor(original_frames / frames_diff)
#     deleted = 0

#     vid_name = osp.basename(original_video)
#     save_path = osp.join(save_folder, vid_name)
#     cap= cv2.VideoCapture(original_video)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), out_fps, (w, h))

#     i=1

#     while(cap.isOpened()):
#         ret, frame = cap.read()
#         if ret == False:
#             break

#         if i > target_frames:
#             break
#         else:
#             if deleted < frames_diff:
#                 if i % step != 0:
#                     print(f'write frame {i}')
#                     i += 1
#                     vid_writer.write(frame)
#                 else:
#                     deleted += 1
#             else:
#                 print(f'write frame {i}')
#                 i += 1
#                 vid_writer.write(frame)

#         # i += 1
    
#     cap.release()
#     cv2.destroyAllWindows()

# write_video(vid_path, original_frames=original_frames,
#             target_frames=target_frames, out_fps=out_fps, save_folder=save_folder)


