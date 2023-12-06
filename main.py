#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from tkinter import *

import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
updateValue=0
def threaded_server(arg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                #data = conn.recv(1024)
                print("Data should be sent to the client: ", str(arg))
                #if not data:
               #    break
                #print("Data sent to the client: ", ex.changeValue)
                conn.sendall(arg.encode())


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setGeometry(30, 40, 200, 30)
        updateValue = mySlider.valueChanged[int].connect(self.changeValue)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Slider Example :)")
        self.label1 = QLabel("tool :)", self);
        self.label1.setAlignment(Qt.AlignCenter);
        self.show()

    def changeValue(self, value):
        print(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()

    #while True:
     #   print(ex.getValue())
    #thread = threading.Thread(target=threaded_server, args=(updateValue,))
    #thread.start()
    sys.exit(app.exec_())
    #print("thread finished...exiting")
    #thread.join()

