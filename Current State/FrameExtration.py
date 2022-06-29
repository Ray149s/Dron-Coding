import cv2
import numpy as np
import os
from glob import glob



## Creates directory specified and if you cant send specified error
def create_dir(path):
    try: 
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name{path}")

## Accepts the variables from main and implements them as fallows in order To:
## Extract Frames from each video in path
## Create a directory for each video file to store each the frames of that video
## Create file names for each frame
def save_frame(video_path, save_dir):
    ## Grabs the name of the video files in the video_path and assigns it to variable name 
    ##  by creating a list that first splits up the value in video_path by the \ in path 
    ##  then splits up things by . then grabbing the first element in the list generated 
    name = video_path.split("\\")[-1].split(".")[0]

    ## Creates the name for the new file to be created in the create_dir method by concatenating 
    ## value in save_dir sent from main with the value of variable name derived above
    save_path = os.path.join(save_dir, name)
    
    ## Creates the Directory
    create_dir(save_path)

    ## Opens up the video file of intrust and assigns its reference to cap
    cap = cv2.VideoCapture(video_path)

    
    ## Determine the frames per sec that video of interest was recorded in
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    ####################################################################
    ############ I want theses values so that I can ensure #############
    ############ that the number of frames matches the     #############
    ############ number of state readings I have per video #############
                                                           #############
    ## Determine how many frames are in video              #############
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))        #############
    print(length)                                          #############
    ###########                                            #############
    ####################################################################
   
    # This idx variable wll be used to name the frames
    idx = 0

    ## Here we extract each frame form the video and store it in the directory with a file name 
    ##  that is its frame number. 
    while True:
        ## 
        ret, frame = cap.read()
       
        # If we reach the end of the video stop the loop
        if ret == False:
            cap.release()
            cv2.destroyAllWindows()
            break

        cv2.imwrite(f"{save_path}/{idx}.png", frame)
        idx += 1
        



if __name__ == "__main__":
    ## Grabbing all video files in the specified folder
    video_paths = glob("Resources/Vid/*")
    ## Naming the directory where the files containing the frames will be saved
    save_dir = "Resources/VidFrame"
    ## sends video_paths and save_dir values from main to save_frame method
    for path in video_paths:
        save_frame(path, save_dir)

