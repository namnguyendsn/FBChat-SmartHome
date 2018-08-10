#!/usr/bin/python

import os
import queue
import threading
from fbchat import log, Client
from fbchat.models import *

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

g_queueLock = threading.Lock()
fbMessListen_rq = queue.Queue(10)
GetTemp_rq = queue.Queue(10)
MessParse_rq = queue.Queue(10)
GetInfo_rq = queue.Queue(10)
Control_rq = queue.Queue(10)
CheckTime_rq = queue.Queue(10)
Sendfb_rq = queue.Queue(10)
ShareFbVar_rq = queue.Queue(10)
g_workQueue = [fbMessListen_rq, GetTemp_rq, MessParse_rq, GetInfo_rq, Control_rq, CheckTime_rq, Sendfb_rq, ShareFbVar_rq]

AutoFan = 1
FanStatus = 1

FbVar = {"thread_id":None, "thread_type":None, "FbObj":None}

global g_fbClient
fbUserId = {"vo":'your facebook id', "admin":'admin's facebook id'}
fbUser = "fb user"
fbPass = "fb pass"
SendTo = "admin"

fbMess = ''
ENABLE_DEBUG = 1
def debug_print(*args, **kwargs):
    if ENABLE_DEBUG:
        print(args, kwargs)

class Facebook(Client):
    def fbSendMessage1(self, who, mess): # gui den 1 nguoi biet truoc userId
        if who:
            debug_print('INFO: send message to ', who)
            self.send(Message(text=mess), thread_id=fbUserId[who], thread_type=ThreadType.USER)
            self.who = who
        else:
            debug_print("ERROR: fbSendMessage fail!!!")
    def fbLogout(self):
        self.logout()
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        debug_print("onMessage: ", message_object.text)
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        self.thread_id = thread_id
        self.thread_type = thread_type
        HasMessEvent = 1
        
        # If you're not the author, echo
        if author_id != self.uid:
            mess = message_object.text
            if mess:
                FbVar["thread_id"] = thread_id
                FbVar["thread_type"] = thread_type
                FbVar["FbObj"] = self
                print("FbVar: ", FbVar)
                print("self: ", self)
                ShareFbVar_rq.put(FbVar)
                fbMessListen_rq.put(mess) # day message vao queue
                mess = ''
    def fbSendMessage(self, mess): # tra loi tin nhan
        self.send(Message(text=mess), thread_id=thread_id, thread_type=thread_type)

            
def fb_init():
    return Facebook(fbUser, fbPass)