import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from tkinter import *
import time
import threading
import logging

import json
import time

FILE_PATH = "../msa/config-msa.json"
bo1_is_on = 1
bo2_is_on = 1

def switch_bo1():
    global bo1_is_on
     
    # Determine is on or off
    if bo1_is_on:
        bo1_is_on = 0
    else:
        bo1_is_on = 1
        
def switch_bo2():
    global bo2_is_on
     
    # Determine is on or off
    if bo2_is_on:
        bo2_is_on = 0
    else:
        bo2_is_on = 1
        
def update_json_element(data, address, value):
    for element in data['assets']:
        if element['id'] == 2:
            for sub_element in element['points']:
                if sub_element['addr'] == address:
                    if sub_element['value'] == value:
                        return 0
                    else:
                        sub_element['value'] = value
                        return 1
                    
def update_json_element_by_name(data, name, value):
    for element in data['assets']:
        if element['id'] == 2:
            for sub_element in element['points']:
                if sub_element['name'] == name:
                    if sub_element['value'] == value:
                        return 0
                    else:
                        sub_element['value'] = value
                        return 1

def thread_function(name, ):
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s: finishing", name)
    
    while True: 
        try: 
            result = 0
            result = update_json_element(data, 30, w1.get())
            result |= update_json_element(data, 32, w2.get())
            result |= update_json_element(data, 200, bo1_is_on)
            result |= update_json_element(data, 201, bo2_is_on)
            if (result):
                jsonfile = open(FILE_PATH, "w")
                jsonfile.write(json.dumps(data, indent = 2))
                jsonfile.close()
                os.system("../msa/./msa --assetid 2 --config ../msa/config-msa.json")
            time.sleep(0.5)
        except:
            jsonfile.close()
            SystemExit
            
jsonfile = open(FILE_PATH, "r+")
data = json.load(jsonfile)
jsonfile.close()

master = Tk()
master.geometry("250x250")
w1 = Scale(master, from_=10, to=100, orient= HORIZONTAL, resolution= 0.01, label= "maxPchrg")
w1.set(19)
w1.pack()

w2 = Scale(master, from_=10, to=100, orient= HORIZONTAL, resolution= 0.01, label= "maxPdsch")
w2.set(25)
w2.pack()

on_button1 = Button(master, command= switch_bo1)
on_button1.place(x=10, y=200)

on_button2 = Button(master, command= switch_bo2)
on_button2.place(x=40, y=200)
 
thread1 = threading.Thread(target=thread_function, args=(1,))
thread1.setDaemon(True)
logging.info("Main    : before running thread")
thread1.start()
logging.info("Main    : wait for the thread to finish")
logging.info("Main    : all done")
       

mainloop()
thread1.join()