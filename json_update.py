import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from tkinter import *
import time
import threading
import logging
import openpyxl
import pandas as pd
import random

import json
import time

FILE_PATH = "../msa/config-msa.json"
bo1_is_on = 0
auto_mode_is_on = 0

def switch_bo1():
    global bo1_is_on
     
    # Determine is on or off
    if bo1_is_on:
        bo1_is_on = 0
        print("bo1_is_on", bo1_is_on)
        on_button1.configure(image = photoimage_off)
        
    else:
        bo1_is_on = 1
        print("bo1_is_on", bo1_is_on)
        on_button1.configure(image = photoimage_on)
        
def switch_auto_mode():
    global auto_mode_is_on
     
    # Determine is on or off
    if auto_mode_is_on:
        auto_mode_is_on = 0
        print("auto_mode_is_on", auto_mode_is_on)
        auto_mode_button.configure(image = photoimage_off)
        
    else:
        auto_mode_is_on = 1
        print("auto_mode_is_on", auto_mode_is_on)
        auto_mode_button.configure(image = photoimage_on)
 
        
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
            if(auto_mode_is_on == 0):
                value1 = w1.get()
                value2 = w2.get()
            else:
                value1 = w1data[random.randrange(len(w1data))]
                value2 = w2data[random.randrange(len(w2data))]
                
            result = update_json_element(data, 30, value1)
            result |= update_json_element(data, 32, value2)
            result |= update_json_element(data, 200, bo1_is_on)
            if (result):
                jsonfile = open(FILE_PATH, "w")
                jsonfile.write(json.dumps(data, indent = 2))
                jsonfile.close()
                os.system("../msa/./msa --assetid 2 --config ../msa/config-msa.json")
            time.sleep(0.5)
        except:
            jsonfile.close()
            SystemExit

dataframe = openpyxl.load_workbook('warrendaledata-mod.xlsx')
data = dataframe.active

for row in data.iter_cols(min_row=6, values_only=True):
    if row[0] == "BusV":
        w1data = row
        print(len(w1data))
        # for cell in row:
        #     print(cell)
    if row[0] == "Bus Freqency":
        w2data = row
        print(len(w2data))
            
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

# Creating a photoimage object to use image 
photo_Off = PhotoImage(file = r"off.png") 
photo_On = PhotoImage(file = r"on.png") 

# Resizing image to fit on button 
photoimage_off = photo_Off.subsample(2,2)
photoimage_on = photo_On.subsample(2,2) 

on_button1 = Button(master, command= switch_bo1,image = photoimage_off)
on_button1.place(x=10, y=200)

auto_mode_button = Button(master, command= switch_auto_mode,image = photoimage_off)
auto_mode_button.place(x=200, y=10)
 
thread1 = threading.Thread(target=thread_function, args=(1,))
thread1.setDaemon(True)
logging.info("Main    : before running thread")
thread1.start()
logging.info("Main    : wait for the thread to finish")
logging.info("Main    : all done")
       

mainloop()
thread1.join()
