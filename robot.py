# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import serial

command = ['move_forward','move_backward','turn_right','turn_left','stop',
           'dome_home', 'dome_left', 'dome_right', 'dome_move',
           'led_command_1', 'led_command_2','led_command_3', 'led_off'
           ]

status = ['ack', 'button'
           ]

class r2d2Robot(object):
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate)
            print('found serial interface')
        except:
            print('no serial interface found')
            self.ser = 0

    def robotCommand(self,cmd):
        if self.ser and cmd in command:
            self.ser.write(command)

    def robotCheck(self):
        if self.ser:
            if(self.ser.inWaiting()>0):
                val = self.ser.read(self.ser.inWaiting()).decode('ascii')
                if val in status: return val
                else: return 0
            else:
                return 0
        else:
            return 0
