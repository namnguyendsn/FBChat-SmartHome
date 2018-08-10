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
import queue
import threading

from common_def import *  
ctFanStatus = 0
ctAutoFan = 0

def handle_req(mess):
    if mess == "init":
        checkTime_init()

def checkTime_init():
    threading.Timer(2.0, checkTime).start() # test only

def checkTime():
    global ctAutoFan
    threading.Timer(900.0, checkTime).start()
    if (ctAutoFan == 1):
        pass
    else:
        debug_print("AutoFan: check time fail")

def CheckTime_process(self):
    while 1:
        g_queueLock.acquire()
        if not CheckTime_rq.empty():
            data = CheckTime_rq.get()
            g_queueLock.release()
            handle_req(data)
            debug_print ("%s processing %s %s" % (self.threadName, data, datetime.datetime.now()))
        else:
            #debug_print (self.threadName, " handle_req empty")
            g_queueLock.release()
