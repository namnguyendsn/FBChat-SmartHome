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

from common_def import *  

def handle_req(mess):
    localtime = time.asctime( time.localtime(time.time()) )
    debug_print(localtime)
    Sendfb_rq.put(localtime)

    mess = mess.upper()
    if(mess == "ON"):
        debug_print("Parse ON")
        Control_rq.put("ON")

    elif(mess == "OFF"):
        debug_print("Parse OFF")
        Control_rq.put("OFF")

    elif(mess[0] == "Q"):
        debug_print("Parse Fan: ", mess)
        Control_rq.put(mess)

    elif(mess[0] == "H"):
        debug_print("Parse Direct: ", mess)
        Control_rq.put(mess)

    elif(mess[0] == "C"):
        debug_print("Parse Temp: ", mess)
        Control_rq.put(mess)

    elif(mess == "?"):
        debug_print("Parse HELP")
        Sendfb_rq.put(u'Gửi tin nhắn để điều khiển')
        Sendfb_rq.put(u'Bật/tắt: on/off')
        Sendfb_rq.put(u'Nhiệt độ: C16 - C31')
        Sendfb_rq.put(u'Quạt: Q1-Q3: số 1-3, Q0: tự động')
        Sendfb_rq.put(u'Hướng gió: H0: tự động, H1 - H4: Hướng gió, H7: tự động đổi hướng')
        Sendfb_rq.put(u'Vợ anh thật là xinh gái <3 <3 <3')
    elif(mess == "TEST"):
        debug_print("Che do chay thu")
        path = os.getcwd() + "/run"
        # xóa file "run"
        file = os.path.isfile(path)    # True 
        if file:
            os.remove(path)

    elif(mess == "RUN"):
        path = os.getcwd() + "/run"
        debug_print("Che do chay binh thuong")
        # tạo file "run"
        fo = open(path, "w")
        fo.close()

    else:
        debug_print("Parse NEED HELP?")
        Sendfb_rq.put(u'Gửi ? để hiển thị hướng dẫn')

def MessParse_process(self):
    while 1:
        g_queueLock.acquire()
        if not MessParse_rq.empty():
            data = MessParse_rq.get()
            g_queueLock.release()
            handle_req(data)
            debug_print ("%s processing %s %s" % (self.threadName, data, datetime.now()))
        else:
            #debug_print (self.threadName, "MessParse_rq empty")
            g_queueLock.release()
