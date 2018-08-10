#!/usr/bin/python

# -*- coding: utf8 -*-
import os
import subprocess
import time
import smtplib
import datetime

from time import sleep
import sys
import urllib.request
import json
import urllib.parse
import threading
import socket
from datetime import datetime
import queue
import threading
import serial

from common_def import *  
AutoFan = 1
FanStatus = 1

g_USBPortsList = ('/dev/ttyUSB0', '/dev/ttyUSB1')
g_comUSBPortName = ""
g_comSerial = serial.Serial()
g_comDataArrayRcv = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # UART rcv buffer 100bytes
g_comDataArraySend = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # UART rcv buffer 10bytes

#Format: [Start][Load][End]
#[Start]: S
#[End]: E
#Ex: S ON E: power up
#S C 20 E: set temp 20

def Off():
    global g_comDataArraySend
    Sendfb_rq.put(u">> Tắt điều hòa ok !!!")
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('O')
    g_comDataArraySend.append('F')
    g_comDataArraySend.append('F')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()

def On():
    global g_comDataArraySend
    Sendfb_rq.put(u">> Bật điều hòa ok !!!")
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('O')
    g_comDataArraySend.append('N')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()

def Set_Temp(temp):
    global g_comDataArraySend
    temp1 = u">> Cài đặt nhiệt độ: " + str(temp) + " ok !!!"
    Sendfb_rq.put(temp1)
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('C')
    g_comDataArraySend.append(str(int(temp/10)))
    g_comDataArraySend.append(str(temp%10))
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()
    
# 0 is auto, 1-5 is the speed, 6 is silent.
def Set_Fan(fan):
    global g_comDataArraySend
    Sendfb_rq.put(u">> Cài đặt quạt số: " + str(fan) + " ok !!!")
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('F')
    g_comDataArraySend.append(str(fan%10))
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()
    
def Set_Air_Direct(direct):
    global g_comDataArraySend
    Sendfb_rq.put(u">> Cài đặt hướng gió: " + str(direct) + " ok !!!")
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('D')
    g_comDataArraySend.append(str(direct%10))
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()
    
def GetStatus():
    global g_comDataArraySend
    Sendfb_rq.put(u">> Trạng thái điều hòa: ok !!!")
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('S')
    g_comDataArraySend.append('T')
    g_comDataArraySend.append('A')
    g_comDataArraySend.append('T')
    g_comDataArraySend.append('U')
    g_comDataArraySend.append('S')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append('E')
    g_comDataArraySend.append(' ')
    g_comDataArraySend.append(' ')
    comSend()
    
    
def setDefault():
    pass

def comGetUSBPort():
    global g_comUSBPortName
    global g_comSerial
    
    for usb in g_USBPortsList:
        try:
            g_comSerial = serial.Serial(usb,  115200)
            g_comSerial.timeout = 1 # set timeout 1s
            g_comUSBPortName = usb
            print("Connected to arduio at " + g_comUSBPortName)
            print(type(g_comDataArrayRcv))
        except serial.SerialException:
            print("Arduino not found at " + usb)
            pass

def comSend():
    global g_comSerial
    global g_comDataArraySend
    try:
        print(g_comDataArraySend)
        for char in g_comDataArraySend:
            g_comSerial.write(char.encode()) # send to ESP
    except KeyboardInterrupt:
        exit()
    except serial.SerialException:
        print("Lost connection. Trying to reconnect...")  
    except IOError:
        print("IOError...")
        pass

# hoi vong de doc UART
def loop_comUSB():
    global g_comDataArrayRcv
    #while 1:
    #print("loop_comUSB...")
    try: 
        temp = g_comSerial.read(100) # moi lan read 100byte, timeout 1s
        if len(temp):
            print("data: ", temp)
            print("len: ", len(temp))
        # search nếu thấy "Power" thì trả lời trạng thái điều hòa
    except KeyboardInterrupt:
        exit()
    except serial.SerialException:
        print("Lost connection. Trying to reconnect...")  
        #break
    except IOError:
        print("IOError...")
        pass
        
def control_init():
    localtime = time.asctime( time.localtime(time.time()) )
    debug_print(localtime)
    Sendfb_rq.put(localtime)
    # set default value, turn off RED, Green and Fan
    Sendfb_rq.put(u'System started!')
    Sendfb_rq.put(u'Khởi tạo, cài đặt trạng thái mặc định')

    # đọc file để xác định chế độ chạy hay test
    # chế độ chạy: có delay khi khởi động, tắt trâu khi mới chạy
    # chế độ test: không delay, không tắt trâu khi mới chạy
    path = os.getcwd() + "/run"
    file = os.path.isfile(path)    # True 
    if file:
        NormalRun = 1
        debug_print("Che do chay binh thuong ok")
        Sendfb_rq.put(u'Chế độ chạy bình thường ok')
        
    else:
        NormalRun = 0
        debug_print("Che do chay thu ok")
        Sendfb_rq.put(u'Chế độ chạy thử ok')

    AutoFan = 1
    comGetUSBPort()
    
def handle_req(mess):
    global AutoFan
    global g_comDataArraySend
    g_comDataArraySend.clear()
    if mess == "ON":
        debug_print("Control AC ON")
        On()

    elif mess == "OFF":
        debug_print("Control AC OFF")
        Off()

    elif(mess[0] == "Q"):
        debug_print("Control Fan: ", mess)
        temp = mess[1]
        try:
            temp = int(temp)
        except ValueError:
            Sendfb_rq.put(u'Cài đặt quạt gió sai.')
        Set_Fan(temp)

    elif(mess[0] == "H"):
        debug_print("Control Direct: ", mess)
        temp = mess[1]
        try:
            temp = int(temp)
        except ValueError:
            Sendfb_rq.put(u'Cài đặt hướng gió sai.')
        Set_Air_Direct(temp)

    elif(mess[0] == "C"):
        debug_print("Control Temp: ", mess)
        temp = mess[1] + mess[2]
        try:
            temp = int(temp)
        except ValueError:
            Sendfb_rq.put(u'Cài đặt nhiệt độ sai.')
        Set_Temp(temp)

    elif mess == "init":
        control_init()

def Control_process(self):
    while 1:
        g_queueLock.acquire()
        if not Control_rq.empty():
            data = Control_rq.get()
            g_queueLock.release()
            handle_req(data)
            debug_print ("%s processing %s %s" % (self.threadName, data, datetime.now()))
        else:
            #debug_print (self.threadName, " Control_rq empty")
            g_queueLock.release()
        loop_comUSB()
