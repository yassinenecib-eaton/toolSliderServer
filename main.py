#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from tkinter import *
import time
import threading
import logging

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def show_values():
    return w1.get()

def thread_function(name, ):
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s: finishing", name)
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                time.sleep(1)
                print("In the thread: ", show_values())
                data = conn.recv(1024)
                dataTosend = str(show_values())
                myIntStr= dataTosend.encode('utf-8')
                conn.sendall(myIntStr) 

master = Tk()
w1 = Scale(master, from_=0, to=42, orient= HORIZONTAL)
master.geometry("250x250")
w1.set(19)
w1.pack()

x = threading.Thread(target=thread_function, args=(1,))
x.setDaemon(True)
logging.info("Main    : before running thread")
x.start()
logging.info("Main    : wait for the thread to finish")
logging.info("Main    : all done")


mainloop()
x.join()

