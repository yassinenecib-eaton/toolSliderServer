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
                print(sub_element['name'])
                if sub_element['addr'] == address:
                    # print("found", address)
                    if sub_element['value'] == value:
                        return 0
                    else:
                        sub_element['value'] = value
                        return 1
                else:
                    print("element not found")
                    return 0
                    
def update_json_element_by_name(data, name, value):
    for element in data['assets']:
        if element['id'] == 2:
            for sub_element in element['points']:
                if sub_element['name'] == name:
                    print("found element")
                    if sub_element['value'] == value:
                        return 0
                    else:
                        sub_element['value'] = value
                        return 1
                    
def get_json_element(data, address):
    for element in data['assets']:
        if element['id'] == 2:
            for sub_element in element['points']:
                if sub_element['name'] == name:
                    return sub_element

def thread_function(name, ):
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s: finishing", name)
    
    while True: 
        print("new search")
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
    if row[0] == "Bus Freqency":
        w2data = row
            
jsonfile = open(FILE_PATH, "r+")
data = json.load(jsonfile)
jsonfile.close()

master = Tk()
# master.geometry("500x500")
w1 = Scale(master, from_=475, to=490, orient= HORIZONTAL, resolution= 0.01, label= "maxPchrg")
w1.grid(row=2, column=3)
w1.set(478)
# w1.pack()

w2 = Scale(master, from_=59, to=61, orient= HORIZONTAL, resolution= 0.01, label= "Freq_BU1ES1")
w2.grid(row=2, column=4)
w2.set(60)
# w2.pack()

# Creating a photoimage object to use image 
photo_Off = PhotoImage(file = r"off.png") 
photo_On = PhotoImage(file = r"on.png") 

# Resizing image to fit on button 
photoimage_off = photo_Off.subsample(2,2)
photoimage_on = photo_On.subsample(2,2) 

on_button1_label = Label(master, text = "ReadySt").grid(row=0, column=3, padx=2, pady=2)

on_button1 = Button(master, command= switch_bo1,image = photoimage_off)
on_button1.grid(row=1, column=3)

auto_mode = Label(master, text = "auto mode").grid(row=0, column=0, padx=2, pady=2)
# auto_mode.pack(padx = 5, pady=15, side=LEFT)

auto_mode_button = Button(master, command= switch_auto_mode,image = photoimage_off)
auto_mode_button.grid(row=1, column=0, padx=2, pady=2)

thread1 = threading.Thread(target=thread_function, args=(1,))
thread1.setDaemon(True)
logging.info("Main    : before running thread")
thread1.start()
logging.info("Main    : wait for the thread to finish")
logging.info("Main    : all done")
       

mainloop()
thread1.join()
