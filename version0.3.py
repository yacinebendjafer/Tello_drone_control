from djitellopy import tello
import cv2
from pynput.mouse import Listener
from time import sleep
import threading

width = 320
height = 240




me = tello.Tello()
me.connect()
# me.connect_to_wifi("0000000", "00000000")

x_direction = "center"
y_direction = "center"


def on_click(x, y, button, pressed):
    
    #print('{0} at {1}'.format( 'Pressed' if pressed else 'Released',(x, y)))
    
    
    if pressed and button == button.right:  
        print("BATTERY CHARGE: " , me.get_battery(),"%")
        me.takeoff() if not me.is_flying else me.land()
      
           
    ########@@@@ add aa functionality to take off  with a while pressed instead off a pressed
    if pressed and button == button.left:  
        if x < 250:
                me.send_rc_control(0, 0, 0, -50)
                sleep(0.2)
        elif x > 910:
            
            me.send_rc_control(0, 0, 0, 50)
            sleep(0.2)

    if not pressed:
        lr, fb, ud, yv = 0, 0, 0, 0
     
        if x < 250:
            x_direction = "left"
        elif x > 910:
            x_direction = "right"
        else:
            x_direction = "center"
        if y < 100:
            y_direction = "forward"
        elif y > 600:
            y_direction = "backward"
        else:
            y_direction = "center"


        speed = 50
        
        if x_direction=="left": lr = -speed
        elif x_direction=="right": lr = speed

        if y_direction=="forward": fb = speed
        elif y_direction=="backward": fb = -speed

            
        # if kp.getKey("a"):yv = -speed
        # elif kp.getKey("d"): yv = speed
        # if kp.getKey("c"): me.streamon()
        
        me.send_rc_control(lr, fb, ud, yv)    
        ########@@@@ same here with the landing but try to use only button for takeoff and landing
def on_scroll(x, y, dx, dy):    
    speed = 50
    ud= 0
    if dy <0:
        
        ud = -speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.3)
    else:
        ud = speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.3)
    
    
        
    ######TRY TO PRINT THE VARIABLE DX PURHAPS IT READS THE X AXIS VARIATION OF THE JOYSTICK
def on_move(x, y):
    x = x
    # print('Pointer moved to {0}'.format((x, y)))
    
    


mouse_thread = threading.Thread(target=Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll).start)
mouse_thread.start()   


def tello_video():
    # Initialize video stream
    me.streamoff()
    me.streamon()

    sleep(1)

    # Initialize OpenCV window
    cv2.namedWindow("Tello Video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tello Video", 960, 720)
        
    while True:

        frame_read = me.get_frame_read()
        img = frame_read.frame
        
        # img = cv2.resize(myFrame, (width, height))
        cv2.imshow('Tello video', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
        

    cv2.destroyAllWindows()
    tello.streamoff()

video_thread = threading.Thread(target=tello_video)
video_thread.start()

mouse_thread.join()
video_thread.join()