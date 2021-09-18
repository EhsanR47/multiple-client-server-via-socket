#default run:
#ip = tcp://127.0.0.1
#port = 14200

#Used:
import socket 
from threading import Thread 
import time
import sys
import json
import os
from subprocess import check_output
from datetime import datetime
import threading
import platform
import gevent
from gevent import subprocess

#run:
#python server.py

./client
#python client.py --infile filename.json
