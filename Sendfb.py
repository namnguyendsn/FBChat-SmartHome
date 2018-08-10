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
from datetime import datetime
import queue
import threading

from fbchat import log, Client
from fbchat.models import *
from common_def import *  

#g_fbClient = Facebook(fbUser, fbPass)
def Sendfb_process(self):
    FbObj = None
    FbVar = None
    Init = 1
    while 1:
        g_queueLock.acquire()
        if Init:
            if not ShareFbVar_rq.empty():
                FbVar = ShareFbVar_rq.get()
                FbObj = FbVar["FbObj"]
                print("Init FbObj", FbObj)
            else:
                pass
                #debug_print (self.threadName, "Sendfb_rq empty")
            
            if not Sendfb_rq.empty():
                print("==================== Admin ====================")
                data = Sendfb_rq.get()
                if data == "run":
                    Init = 0
                g_queueLock.release()
                print(data)
                FbObj.fbSendMessage1(SendTo, data)
                debug_print ("%s processing %s %s" % (self.threadName, data, datetime.now()))
            else:
                #debug_print (self.threadName, "Sendfb_rq empty")
                g_queueLock.release()
        else:
            if not ShareFbVar_rq.empty():
                FbVar = ShareFbVar_rq.get()
                FbObj = FbVar["FbObj"]
                print("Reply FbObj", FbObj)
            else:
                pass
                #debug_print (self.threadName, "Sendfb_rq empty")
            
            if not Sendfb_rq.empty():
                print("==================== Reply ====================")
                data = Sendfb_rq.get()
                g_queueLock.release()
                print(data)
                print("Send to: ", FbVar["thread_id"])
                FbObj.send(Message(text=data), thread_id=FbVar["thread_id"], thread_type=FbVar["thread_type"])
                debug_print ("%s processing %s %s" % (self.threadName, data, datetime.now()))
            else:
                #debug_print (self.threadName, "Sendfb_rq empty")
                g_queueLock.release()