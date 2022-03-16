"""@file           servo_driver.py
   @brief          A driver for servo motor
   @details        The driver creates a servo object and changes the arm position from two predetermined values
   @author         Clayton Elwell
   @author         Tyler McCue
   @date           March 4, 2022
"""

import pyb

class Servo:
    '''@brief       Interface with servo motor
       @details     Contains basic functionality to move servo motor from level to raised
    '''
    
    def __init__(self, timer, pin):
        '''
        @brief          Constructor for servo motor
        @param timer    Timer object used by servo for PWM
        @param pin      Pin object that carries the command to the servo
        '''
        ### Timer number for servo motor PWM
        self.timer = timer
        ### Input pin for servo PWM
        self.pin = pin
        ## Timer object for servo
        self.tim = pyb.Timer(self.timer, freq=50) # create a timer object using timer 4

        #pinB3 = pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP)
        ## Timer channel for servo PWM
        self.ch2 = self.tim.channel(2, pyb.Timer.PWM, pin=pin)


    def change_pen(self, value):
        '''@brief       Changes servo motor level based on given value, 1 levels motor and rest raises motor  
        '''
        if value == 1:
            self.ch2.pulse_width_percent(8) #Level
        else:
            self.ch2.pulse_width_percent(7)


