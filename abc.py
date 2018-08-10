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

counter = 0
while 1:
    global counter
    print(datetime.datetime.now())
    time.sleep(2)
    counter += 1
    if counter == 30:
        os.system("lxterminal -e python3 /home/pi/Desktop/ACRemote/MitsubishiACRemoteV1.0/main.py")
