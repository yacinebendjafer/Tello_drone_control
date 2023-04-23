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
    
    if me.is_flying == False:
        statee = False
        print("reeeeeeeeeqdddddddddyyyyyyyy")
    if pressed and button == button.right:  

        print("BATTERY CHARGE: " , me.get_battery(),"%")
    me.takeoff() if not me.is_flying else me.land() and quit()
    sleep(1)
       ##@@@@ add aa functionality to take off  with a while pressed instead off a pressed
    
    
        
        
    if pressed and button == button.right:
      
        yv = 0
        
        if x < 250:
            yv = 50
            me.send_rc_control(0, 0, 0, -yv)
            sleep(0.5)
            me.send_rc_control(0, 0, 0, 0)
            sleep(0.07)
        if x > 910:
            yv = 50
            me.send_rc_control(0, 0, 0, yv)
            sleep(0.5)
            me.send_rc_control(0, 0, 0, 0)
            sleep(0.07)
    
    
        
                


          
        ########@@@@ same here with the landing but try to use only button for takeoff and landing
def on_scroll(x, y, dx, dy):    
    speed = 50
    ud= 0
    if dy <0:
        
        ud = -speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.3)
        me.send_rc_control(0, 0, 0, 0)
    else:
        ud = speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.3)
        me.send_rc_control(0, 0, 0, 0)
    
    
        
    ######TRY TO PRINT THE VARIABLE DX PURHAPS IT READS THE X AXIS VARIATION OF THE JOYSTICK
def on_move(x, y):
    lr, fb = 0, 0
    speed = 30
    if x < 250:
        lr = -speed
    if x > 910:
        lr = speed
    
    if y < 100: 
        fb = speed
    if y > 600:
        fb = -speed
    me.send_rc_control(lr, fb, 0, 0)  
    # print('Pointer moved to {0}'.format((x, y)))
    
    


mouse_thread = threading.Thread(target=Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll).start)
mouse_thread.start()   


def tello_video():
    # Initialize video stream
    me.streamoff()
    me.streamon()

    

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