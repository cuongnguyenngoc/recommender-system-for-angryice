from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import requests, csv, random, json
import Utils

class ArtManager1:
    def __init__(self):
        self.images = {}
        self.set_images()

    def initialize_window(self, window):

        self.window = window
        
        
        self.Top = Frame(self.window, width=1660, height=50, bg="white", relief="raise")
        self.Top.pack(side=TOP, padx=5, pady=5)

        self.Title = Label(self.Top, font=('arial', 40, 'bold'), text="Describing Session", fg="red", bg="white", bd=10, anchor='w')
        self.Title.grid(row=0,column=0)

        self.Bottom = Frame(self.window, width=1660, height=150, bg="white", relief="raise")
        self.Bottom.pack(side=BOTTOM, padx=10, pady=10)

        self.Right = Frame(self.window, width=250, height=750, bg="white", relief="raise")
        self.Right.pack(side=RIGHT, padx=5, pady=5)

        self.show_content()
        
    # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
    def refresh(self):
        try:
            
            self.set_images()

            self.show_content()

        except:
            pass

    def get_images(self):
        return self.images
    
    def set_images(self):
        self.images = {}
        name_bg_file_lines = []
        is_error = False
        try:
            open("../VoteImage/image1.jpg")
            open("../VoteImage/image2.jpg")
            open("../VoteImage/image3.jpg")
            name_bg_file = open('../VoteImage/name_bg.txt','r')
            name_bg_file_lines = name_bg_file.read().splitlines()
        except:
            is_error = True
            
        
        # name_bg_file = open('../VoteImage/name_bg.txt','r')
        # name_bg_file_lines = name_bg_file.read().splitlines()
        if name_bg_file_lines or is_error:
            Utils.Utils().retrieveImages()
            name_bg_file = open('../VoteImage/name_bg.txt','r')
            name_bg_file_lines = name_bg_file.read().splitlines()
        
        bg_img1_order = "1"
        bg_img2_order = "2"
        bg_img3_order = "3"

        self.images[bg_img1_order] = name_bg_file_lines[0]
        self.images[bg_img2_order] = name_bg_file_lines[1]
        self.images[bg_img3_order] = name_bg_file_lines[2]


    def show_content(self):
        bg_img1_order = "1"
        bg_img2_order = "2"
        bg_img3_order = "3"
        size = 128, 128

        self.Left = Frame(self.window, width=1390, height=750, bg="white", relief="raise")
        self.Left.pack(side=LEFT, padx=5, pady=5)

        self.T = Label(self.Left, font=('arial', 20), text=bg_img1_order, bg="white", anchor="w")
        self.T.grid(row=0,column=0)
        
        img = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image1.jpg"), 455))
        self.panel = Label(self.Left, image = img, height=350, width=455, bg="white", padx=0)
        self.panel.grid(row=1, column=0)
        self.panel.image = img
        
        Label(self.Left, font=('arial', 5), bg="white", text=" ").grid(row=1, column=1)

        # Label(self.Left, font=('arial', 20), text="3:a painting of a man standing next to a building", bg="white", wraplengt=420).grid(row=4, column=0)
        # Label(self.Left, font=('arial', 20), text="4:a group of people standing on top of a beach", bg="white", wraplengt=420).grid(row=5, column=0)

        self.T2 = Label(self.Left, font=('arial', 20), bg="white", text=bg_img2_order, anchor="w")
        self.T2.grid(row=0, column=2)
        
        img2 = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image2.jpg"), 455))
        self.panel2 = Label(self.Left, image = img2, height=350, width=455, bg="white", padx=0)
        self.panel2.grid(row=1, column=2)
        self.panel2.image = img2

        Label(self.Left, font=('arial', 5), bg="white", text=" ").grid(row=1, column=3)

        # Label(self.Left, font=('arial', 20), text="3:a painting of a man standing next to a building", wraplengt=420, bg="white", anchor='e').grid(row=4, column=2)
        # Label(self.Left, font=('arial', 20), text="4:a group of people standing on top of a beach", wraplengt=420, bg="white", anchor='e').grid(row=5, column=2)

        self.T3 = Label(self.Left, font=('arial', 20), text=bg_img3_order, bg="white", anchor="w")
        self.T3.grid(row=0, column=4)
        
        img3 = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image3.jpg"), 455))
        self.panel3 = Label(self.Left, image = img3, height=350 ,width=455, bg="white", padx=0)
        self.panel3.grid(row=1, column=4)
        self.panel3.image = img3
    
    def resize_image(self, img, width):
        wpercent = (width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((width,hsize), Image.ANTIALIAS)

        return img