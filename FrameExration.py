import cv2
import numpy as np
import os
from glob import glob




def create_dir(path):
    try: 
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name{path}")

## Accepts the variables from main and them as fallows
def save_frame(video_path, save_dir):
    ## Grabs the name of the videos file in the video_path and assigns it to variable name by creating a list that first splits up the value in video_path by the \ in path then splits up things by . then grabing the first element in the list created by this spliting
    name = video_path.split("\\")[-1].split(".")[0]

    ## Creates the name for the new file to be created in the create_dir method by concatinating value in save_dir sent from main with the value of name derived above
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)

    ## Opens up the video file of intrest and assigns the refrence to it to cap
    cap = cv2.VideoCapture(video_path)
    ## Determins the frames per sec that video of intrest was recoreded in
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    ## Determins how many frames are in video
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    
  
    # This idx variable wll be used to name the frames
    idx = 0

  
    while True:
        ## modulowing the frame by frame rate to grab no more frames than videos frame rate originaly captured 
        ret, frame = cap.read()
       
        # If we reaache the end of the video
        if ret == False:
            cap.release()
            cv2.destroyAllWindows()
            break

        cv2.imwrite(f"{save_path}/{idx}.png", frame)
        idx += 1
        



if __name__ == "__main__":
    ## Grabing all video files in the specified folder
    video_paths = glob("Resources/Pvid/*")
    ## Naming the directory where the files containing the frames will be saved
    save_dir = "Resources/PVideoFrames"
    ## sends video_paths and save_dir values from main to save_frame method
    for path in video_paths:
        save_frame(path, save_dir)

