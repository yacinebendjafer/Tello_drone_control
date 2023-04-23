
from djitellopy import tello


import time


me = tello.Tello()


me.connect()


print(me.get_battery())

x_prev_pos = 0

kp_x_y = 10.5


kd_x_y = 40


x = 0
y = 0


prev_time = time.time()

# x_wanted = input()
# y_wanted = input()
# z_wanted = input()

x_wanted = [7,-5,-2,7]
y_wanted = [0,7,-6,5]
z_wanted = [10,6,8,10]


# x_wanted = float(x_wanted)
# y_wanted = float(y_wanted)
# z_wanted = float(z_wanted)



me.takeoff()
time.sleep(2)
vel_error_roll = 0
vel_error_pitch = 0

for i in range(200):
    vel_error_roll = vel_error_roll + me.get_speed_y()

vel_error_roll = vel_error_roll / 200

for i in range(200):
    vel_error_pitch = vel_error_pitch + me.get_speed_x()
vel_error_pitch = vel_error_pitch / 200


me.send_rc_control(0, 0, 0, 0)
time.sleep(1)

x_actual_pos = 0
y_actual_pos = 0
z_actual_pos_error = me.get_height()

x_prev_error = 0
y_prev_error = 0
z_prev_error = 0

point = 0

reached_x = False
reached_y = False
reached_z = False
while True and me.is_flying:
    
    
    
    now = time.time()
    
    delta_time = now - prev_time
    

    
    if  delta_time > 0.002:
        
        prev_time = now
        velocity_roll = me.get_speed_y() - vel_error_roll
        velocity_pitch = me.get_speed_x() - vel_error_pitch
        
        acc_x = me.get_acceleration_x() 
        acc_y = me.get_acceleration_y()
            
        x_actual_pos = x_actual_pos + velocity_roll * delta_time
        x_actual_pos = round(x_actual_pos,2)
        
        y_actual_pos = y_actual_pos + velocity_pitch * delta_time
        y_actual_pos = round(y_actual_pos,2)
        
        z_actual_pos = me.get_height() - z_actual_pos_error
        z_actual_pos /= 10
        
        x_error = 0 
        y_error = 0
        z_error = 0
        
        x_speed = 0
        y_speed = 0
        z_speed = 0
        
        x_diff_error = 0
        y_diff_error = 0
        z_diff_error = 0
        
        
        x_error = round(x_wanted[point] - x_actual_pos)
        y_error = round(y_wanted[point] - y_actual_pos)
        z_error = round(z_wanted[point] - z_actual_pos)
        
        x_diff_error = (x_error - x_prev_error) / delta_time
        y_diff_error = (y_error - y_prev_error) / delta_time
        z_diff_error = (z_error - z_prev_error) / delta_time
        if z_diff_error > 0:
            kp_z = 10
            kd_z = 35
        else:
            kp_z = 10 * 1.4
            kd_z = 40 * 1.4
        
        # print(x_error," | ",y_error," | ",z_error," | ", point)
        # print("")
        
        
        
        
        if abs(x_error) > 0.9:
            
            x_speed = (kp_x_y * x_error) + (kd_x_y * x_diff_error)
            
            if x_speed > 40:
                x_speed = 40
            if x_speed < -40:
                x_speed = -40
        else:
            x_speed = 0
            reached_x = True
            
            
        if abs(y_error) > 0.9:
            
            y_speed = kp_x_y * y_error + (kd_x_y * y_diff_error)
            
            if y_speed > 40:
                y_speed = 40
            if y_speed < -40:
                y_speed = -40
        else:
            y_speed = 0
            reached_y = True
        
        if abs(z_error) > 1.1:
            
            z_speed = kp_z * z_error + (kd_z * z_diff_error)
            
            if z_speed > 40:
                z_speed = 40
            if z_speed < -40:
                z_speed = -40
        else:
            z_speed= 0
            reached_z = True
        
        if reached_x == True and reached_y == True and reached_z == True:
            point += 1
           
            reached_x = False
            reached_y = False
            reached_z = False
            if point > 2:
                me.send_rc_control(0, 0, 0, 0)
                time.sleep(2)
                me.land()
                quit()

            
            
    x_speed = int(x_speed)
    y_speed = int(y_speed)
    z_speed = int(z_speed)
    
    me.send_rc_control(x_speed, y_speed, z_speed, 0)  
    
    x_prev_error = x_error
    y_prev_error = y_error
    z_prev_error = z_error  
        # vals = getKeyboardInput()

    
    
