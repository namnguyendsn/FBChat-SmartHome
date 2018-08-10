#!/usr/bin/python

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
import common_def
from common_def import *  

#import Adafruit_DHT
import queue
import threading
import fbMessListen
import Control
import MessParse
import GetInfo
import Sendfb
import CheckTime

class myThread (threading.Thread):
    def __init__(self, threadID, name, process, rq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = name
        self.ReceiveQueue = rq
        self.process = process
    def run(self):
        debug_print ("Starting " + self.threadName)
        self.process(self)
        debug_print ("Exiting " + self.threadName)

def GetTemp_process(self):
    pass

def run():
    g_queueLock.acquire()
    Sendfb_rq.put("run") # Start run
    g_queueLock.release()

g_fbClient = common_def.fb_init()
print("g_fbClient: ", g_fbClient)

threadID = 0
threads_arr = []
process_arr = [fbMessListen.fbmess_process,GetTemp_process,MessParse.MessParse_process,GetInfo.GetInfo_process,Control.Control_process,CheckTime.CheckTime_process, Sendfb.Sendfb_process]

threadList = ["fbMessListen", "GetTemp", "MessParse", "GetInfo", "Control", "CheckTime", "Sendfb"]


# Create new threads
for tName in threadList:
    thread = myThread(threadID + 1, tName, process_arr[threadID], g_workQueue[threadID])
    thread.start()
    threads_arr.append(thread)
    threadID += 1

g_queueLock.acquire()
# Fill the queue
FbVar["FbObj"] = g_fbClient
ShareFbVar_rq.put(FbVar)
time.sleep(2)
Control_rq.put("init")
time.sleep(2)
CheckTime_rq.put("init")
time.sleep(2)
GetInfo_rq.put("init")
g_queueLock.release()

threading.Timer(10.0, run).start() # test only

g_fbClient.listen()
    
# Wait for all threads to complete
for t in threads_arr:
    t.join()
debug_print ("Exiting Main Thread")
        
        
        
        
        
        
        
        
        
        
        
        
        