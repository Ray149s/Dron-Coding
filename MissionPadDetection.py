from djitellopy import Tello
import cv2, time

# create and connect
# 创建Tello对象并连接
tello = Tello()
tello.connect()
text = "Battery Life Pecentage: " + str(tello.get_battery()) + " Tello Temp: " + str(tello.get_temperature())
print(text)
# configure drone
# 设置无人机
tello.enable_mission_pads()
tello.set_mission_pad_detection_direction(1)  # forward detection only  只识别前方
tello.streamon()

tello.takeoff()

pad = tello.get_mission_pad_id()


#############################
#############################
xdist = tello.get_mission_pad_distance_x()
ydist = tello.get_mission_pad_distance_y()
zdist = tello.get_mission_pad_distance_z()
# font = cv2.FONT_HERSHEY_SIMPLEX
# bottom_left_corner = (10, 710)
#############################
#############################


# detect and react to pads until we see pad #1
# 发现并识别挑战卡直到看见1号挑战卡
while pad != 1:
   
    
  
    # img= tello.get_frame_read().frame  ## Gives them the individual image frame 
    # cv2.putText(img, text, bottom_left_corner, font, 1, (0, 0, 255), 2)
    # img= cv2.resize(img,(360,240))  ## Resize the image in order to process faster keeping frame small makes Processing faster
    # cv2.imshow("Image ", img)       ## Gives window to display image
    # cv2.waitKey(1)                  ## With out the wait key the Image window will shutdown before we can see the image so we give it a delay of 1 mili sec
    
    if pad == 8:
        print("Pad 8 recognized")
        print(xdist, ydist, zdist)
        print(text)
        tello.rotate_clockwise(175)
        tello.go_xyz_speed(500, -150, 100, 90)
        time.sleep(4)
        tello.go_xyz_speed(85, 10, -30, 40)
        time.sleep(2)
        # time.sleep(4)
        # tello.move_up(100)
        # time.sleep(2)
        # tello.flip_back()
        # time.sleep(2)
        # tello.flip_left()
        # time.sleep(2)
        # tello.flip_forward()
        # time.sleep(2)
        # tello.flip_right()
        # time.sleep(2)
        # tello.go_xyz_speed(50, -50, -100, 20)
        # tello.send_rc_control(0,0,0,0)
        # time.sleep(3)
        # tello.move_back(30)
        # tello.rotate_clockwise(90)
        # cv2.destroyAllWindows()
        break
    if pad == 7:
        print("Pad 7 Recognized")
        tello.go_xyz_speed(-50, 50, 0, 20, )
        time.sleep(4)
        break
        # tello.move_up(30)
        # tello.flip_forward()

       

    pad = tello.get_mission_pad_id()

# graceful termination
# 安全结束程序
tello.disable_mission_pads()
tello.land()
tello.end()