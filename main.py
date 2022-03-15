"""!
@file main.py
    This file is the main program file for the plotter car.
    File creates several tasks including motor, interpreter tasks, and
    file parsing tasks.

@author         Clayton Elwell
@author         Tyler McCue
@date           March 4, 2022
"""

import gc
import pyb
import cotask
import task_share
import Closed_Loop as control
import encoder_elwell_mccue as enc
import motor_elwell_mccue as moe
import utime
import servo_driver as ser
import chassis_driver as ch


def task_MCU1 ():
    """!
    Task controls motor 1 
    """
    while True:
        update1 = enc1.update()
        duty1 = control1.run(update1)
        motor1.set_duty_cycle(duty1)
        if abs(duty1) <= 20 and enc1.get_delta() < 5:
            share_ready1.put(1)
        if share_ready1.get() == 1 and share_ready2.get() == 1:
            share_bothR.put(1)
        yield (0)


def task_MCU2 ():
    """!
    Task controls motor 2.
    """
    while True:
        update2 = enc2.update()
        duty2 = control2.run(update2)
        motor2.set_duty_cycle(duty2)
        if abs(duty2) <= 20 and enc2.get_delta() < 5:
            share_ready2.put(1)
        if share_ready1.get() == 1 and share_ready2.get() == 1:
            share_bothR.put(1)
        yield (0)
        
def task_interpret ():
    """!
    Task interprets commands from file to control certain motors
    """
    while True:
        if share_bothR.get() == 1:
            if share_comm.get() == 0:
                (ref1, ref2) = chass.find_motor_dists(True, share_theta.get())
                control1.setReference(ref1)
                control2.setReference(ref2)
                enc1.set_position(0)
                enc2.set_position(0)
                share_bothR.put(0)
                share_ready2.put(0)
                share_ready1.put(0)
            if share_comm.get() == 1:
                servo.change_pen(share_pen.get())
                (ref1, ref2) = chass.find_motor_dists(False, share_dist.get())
                control1.setReference(ref1)
                control2.setReference(ref2)
                enc1.set_position(0)
                enc2.set_position(0)
                share_bothR.put(0)
                share_ready2.put(0)
                share_ready1.put(0)
            if share_comm.get() == 2:
                share_nextI.put(1)
            share_comm.put(share_comm.get() + 1)
            if share_comm.get() > 2:
                share_comm.put(0)
        yield(0)
            

def task_parse ():
    """!
    Task parses file for commands
    """
    with open(r"code.txt", "r") as c:
        while True:
            if share_nextI.get() == 1:
                commands = c.readline()
                if "st" in commands:
                    share_stop.put(1)
                else:    
                    if len(commands) > 0:
                         commands = commands.split("_")
                         share_theta.put(float(commands[0][1:]))
                         share_dist.put(float(commands[1][1:]))
                         share_pen.put(float(commands[2][1:]))
            share_nextI.put(0)
            yield(0)
                
        
# This code creates all motor, encoder, control, servo, and chassis objects and instantiates 4 tasks to control the robot
#

if __name__ == "__main__":
    ## Right wheel tuning parameter
    right = 1.01
    ## Left wheel tuning parameter
    left = 1.01
    ## Chassis tuning parameter
    tune = 1.02
    ## Pen POC to wheel distance
    center = 3.03
    ## Wheel radius
    wheel = 2.53/2
    ## Gear ratio
    gear = 16/71
    ## Encoder conversion factor
    encoder = (256*16*4/360)

    ##Driver for chassis
    chass = ch.chassis(center, wheel, gear, encoder, tune, right, left)
    
    ##Driver for servo object
    servo = ser.Servo(2, pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP))
    
    ## Driver object for first motor
    motor1 = moe.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    
    ## Driver object for second motor
    motor2 = moe.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    
    ## Driver object for first encoder
    enc1 = enc.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    ## Driver object for second encoder
    enc2 = enc.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    
    motor1.enable()
    motor2.enable()
    
    enc1.set_position(0)
    enc2.set_position(0)
    
    ## Controller object for first motor
    control1 = control.ClosedLoop(-100, 100, .009, 0, 0)
    ## Controller object for second motor
    control2 = control.ClosedLoop(-100, 100, .009, 0, 0)
    
    

    # Create a shares for tasks
    ## Share to ensure motor 1 is at the correct position
    share_ready1 = task_share.Share ('f', thread_protect = False, name = "Ready1")
    ## Share to ensure motor 2 is at the correct position
    share_ready2 = task_share.Share ('f', thread_protect = False, name = "Ready2")
    ## Share to ensure both motors are at the correct position
    share_bothR = task_share.Share ('f', thread_protect = False, name = "Ready2")
    ## Share storing commands between PC and Nucleo
    share_comm = task_share.Share ('f', thread_protect = False, name = "Command")
    ## Share storing next instruction for plotter tool to execute
    share_nextI = task_share.Share ('f', thread_protect = False, name = "Stop")
    
    #share_c1val = task_share.Share ('f', thread_protect = False, name = "Val1")
    
    #share_c2val = task_share.Share ('f', thread_protect = False, name = "Val2")
    ## Current controller gain value
    share_currC = task_share.Share ('f', thread_protect = False, name = "CurrentCommand")
    ## Rotational distance for motors to travel
    share_theta = task_share.Share ('f', thread_protect = False, name = "ThetaVal")
    ## Wheel radius shared value
    share_dist = task_share.Share ('f', thread_protect = False, name = "RadiusVal")
    ## Boolean indicating whether pen should be up or down
    share_pen = task_share.Share ('f', thread_protect = False, name = "PenVal")
    ## Stores value that stops the plotter device
    share_stop = task_share.Share ('f', thread_protect = False, name = "Stop")
    
    
    share_ready1.put(0)
    share_ready2.put(0)
    share_currC.put(0)
    share_stop.put(0)
    share_nextI.put(1)
    share_comm.put(0)
    share_bothR.put(1)
    

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    ## Motor 1 Task
    task1 = cotask.Task (task_MCU1, name = 'Task_Motor_1', priority = 3, 
                         period = 25, profile = True, trace = False)
    ## Motor 2 Task
    task2 = cotask.Task (task_MCU2, name = 'Task_Motor_2', priority = 3, 
                         period = 25, profile = True, trace = False)
    ## Interpreter Task
    task3 = cotask.Task (task_interpret, name = 'Task_Interpreter', priority = 2, 
                         period = 500, profile = True, trace = False)
    ## Parser Task
    task4 = cotask.Task (task_parse, name = 'Task_Parser', priority = 1, 
                         period = 500, profile = True, trace = False)
    
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()
    
    while share_stop.get() == 0:
        cotask.task_list.pri_sched()
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    motor1.disable()
    motor2.disable()

    
            
        