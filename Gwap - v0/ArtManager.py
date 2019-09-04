from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import requests, csv, random

class ArtManager:
    def __init__(self):
        self.list_imgs = []
    
    def initialize_window(self, window):
        name_bg_file = open('../VoteImage/name_bg.txt','r')
        name_bg_file_lines = name_bg_file.read().splitlines()

        self.list_imgs = name_bg_file_lines

        bg_img1_order = "1"
        bg_img2_order = "2"
        bg_img3_order = "3"
        
        self.T = Label(window, text=bg_img1_order,height=1, width=30)
        self.T.place(x=1380, y=2)
        
        img = ImageTk.PhotoImage(file = "../VoteImage/image1.jpg")
        self.panel = Label(window, image = img , height=240 ,width=330)
        self.panel.place(x=1310, y=20)
        self.panel.image = img
        
        self.T2 = Label(window, text=bg_img2_order,height=1, width=30)
        self.T2.place(x=1380, y=270)
        
        img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
        self.panel2 = Label(window, image = img2 , height=240 ,width=330)
        self.panel2.place(x=1310, y=290)
        self.panel2.image = img2
        
        self.T3 = Label(window, text=bg_img3_order,height=1, width=30)
        self.T3.place(x=1380, y=540)
        
        img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
        self.panel3 = Label(window, image = img3 , height=240 ,width=330)
        self.panel3.place(x=1310, y=560)
        self.panel3.image = img3

    # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
    def refresh(self):
        try:
            name_bg_file = open('../VoteImage/name_bg.txt','r')
            name_bg_file_lines = name_bg_file.read().splitlines()

            self.list_imgs = name_bg_file_lines

            img = ImageTk.PhotoImage(Image.open("../VoteImage/image1.jpg"))
            self.panel.configure(image=img)
            self.panel.image = img
            img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
            self.panel2.configure(image=img2)
            self.panel2.image = img2
            img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
            self.panel3.configure(image=img3)
            self.panel3.image = img3

        except:
            pass

    def get_list_imgs(self):
        return self.list_imgs
