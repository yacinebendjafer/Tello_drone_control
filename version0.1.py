#Keyboard Control
from djitellopy import tello
# import KeyPressModule as kp
import cv2
from pynput import mouse
from time import sleep



width = 320
height = 240


me = tello.Tello()

me.connect()


me.streamoff()
me.streamon()


########
x_direction = "center"
y_direction = "center"


        
    
 

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format( 'Pressed' if pressed else 'Released',(x, y)))
    #print(button)
    if pressed and button == button.left:
        me.land()
        sleep(3)
        print("land")
    if pressed and button == button.right:
        me.takeoff()
        print("to")
    
def on_scroll(x, y, dx, dy):
    speed = 50
    # print('Scrolled {0}'.format('down' if dy < 0 else 'up'))
    ud= 0
    if dy <0:
        
        ud = -speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.5)
    else:
        ud = speed
        me.send_rc_control(0, 0, ud, 0)
        sleep(0.5)
    
    # elif kp.getKey("s"): ud = -speed


        
# Collect events until released


    

def on_move(x, y):
    
    # print('Pointer moved to {0}'.format((x, y)))
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
        
    # print(x_direction + " | " + y_direction)

    speed = 50
    
    if x_direction=="left": lr = -speed

    elif x_direction=="right": lr = speed

     

    if y_direction=="forward": fb = speed

    elif y_direction=="backward": fb = -speed

       
   

    # if kp.getKey("a"):yv = -speed

    # elif kp.getKey("d"): yv = speed

   
    # if kp.getKey("c"): me.streamon()
    me.send_rc_control(lr, fb, ud, yv)

    
    
with mouse.Listener(
    
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

 
while True:

    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    cv2.imshow('camera du drone', img)

    listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

    #print(me.get_battery())
    
    
    
    listener.start()
    
    sleep(0.01)
