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

def SystemStatus():
    global giFanStatus
    global giAutoFan

    debug_print("FanStatus: ", giFanStatus, " AutoFan: ", giAutoFan)

    path = os.getcwd() + "/run"
    file = os.path.isfile(path)    # True 
    if file:
        debug_print("Running in normal mode")
        Sendfb_rq.put(u'Chế độ chạy bình thường')
    else:
        debug_print("Running in test mode")
        Sendfb_rq.put(u'Chế độ chạy thử')
        
def handle_req(mess):
    global ListMiner
    global giAutoFan
    global giFanStatus
    
    debug_print ("GetInfo ", mess)
    if mess == "init":
        pass

    elif mess == "STATUS":
        SystemStatus()

def GetInfo_process(self):
    while 1:
        g_queueLock.acquire()
        if not GetInfo_rq.empty():
            data = GetInfo_rq.get()
            g_queueLock.release()
            handle_req(data)
            debug_print ("%s processing %s %s" % (self.threadName, data, datetime.now()))
        else:
            #debug_print (self.threadName, "GetInfo_rq empty")
            g_queueLock.release()
