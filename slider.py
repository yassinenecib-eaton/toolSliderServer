from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from tkinter import *

master = Tk()
w1 = Scale(master, from_=0, to=42, orient= HORIZONTAL)
master.geometry("250x250")
w1.set(19)
w1.pack()

mainloop()