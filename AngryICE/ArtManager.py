
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import requests, csv, random

class ArtManager2:
    def __init__(self, window):
        # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
        def refresh(window):
            try:
                name_bg_file = open('../VoteImage/name_bg.txt','r')
                name_bg_file_lines = name_bg_file.read().splitlines()  
                # bg_img1_name = name_bg_file_lines[0]
                # bg_img2_name = name_bg_file_lines[1]
                # bg_img3_name = name_bg_file_lines[2]
                bg_img1_name = "1"
                bg_img2_name = "2"
                bg_img3_name = "3"
                T.configure(text=bg_img1_name )
                T.text = bg_img1_name 
                T2.configure(text=bg_img2_name )
                T2.text = bg_img2_name 
                T3.configure(text=bg_img3_name )
                T3.text = bg_img3_name             
                img = ImageTk.PhotoImage(Image.open("../VoteImage/image1.jpg"))
                panel.configure(image=img)
                panel.image = img
                img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
                panel2.configure(image=img2)
                panel2.image = img2
                img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
                panel3.configure(image=img3)
                panel3.image = img3

            except:
                pass

            window.after(75000,refresh,window)
        
        name_bg_file = open('../VoteImage/name_bg.txt','r')
        name_bg_file_lines = name_bg_file.read().splitlines()  
        # bg_img1_name = name_bg_file_lines[0]
        # bg_img2_name = name_bg_file_lines[1]
        # bg_img3_name = name_bg_file_lines[2]
        bg_img1_name = "1"
        bg_img2_name = "2"
        bg_img3_name = "3"
        
        self.T = Label(window, text=bg_img1_name,height=1, width=30)
        self.T.place(x=1380, y=2)
        # T.pack()
        
        img = ImageTk.PhotoImage(file = "../VoteImage/image1.jpg")
        self.panel = Label(window, image = img , height=240 ,width=330)
        self.panel.place(x=1310, y=20)
        self.panel.image = img
        # panel.pack()
        
        self.T2 = Label(window, text=bg_img2_name,height=1, width=30)
        self.T2.place(x=1380, y=270)
        # T2.pack()
        
        img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
        self.panel2 = Label(window, image = img2 , height=240 ,width=330)
        self.panel2.place(x=1310, y=290)
        # panel.grid(column=5, row=2)
        self.panel2.image = img2
        # panel2.pack()
        
        self.T3 = Label(window, text=bg_img3_name,height=1, width=30)
        self.T3.place(x=1380, y=540)
        # T3.pack()
        
        img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
        self.panel3 = Label(window, image = img3 , height=240 ,width=330)
        self.panel3.place(x=1310, y=560)
        # panel.grid(column=5, row=3)
        self.panel3.image = img3
        # panel3.pack()

        window.after(75000,refresh,window)
        # window.after(60000,self.retrieveImages)


class ArtManager:
    def __init__(self, window):
        self.window = window
        name_bg_file = open('../VoteImage/name_bg.txt','r')
        name_bg_file_lines = name_bg_file.read().splitlines()
        print("hello ", name_bg_file_lines)  
        bg_img1_name = name_bg_file_lines[0]
        bg_img2_name = name_bg_file_lines[1]
        bg_img3_name = name_bg_file_lines[2]
        bg_img1_order = "1"
        bg_img2_order = "2"
        bg_img3_order = "3"

        # photo1 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
        # print(self.photo1)
        # l = Label(window, image=photo1, bg="black")
        # l.grid(row=0, column=0, sticky=W)
        # l.image=photo1
        # l.pack()

        # window.mainloop
        lightgray_bg = tk.Frame(master=window,bg='lightgray')
        lightgray_bg.pack_propagate(0) 
        lightgray_bg.pack(fill=tk.BOTH, expand=1) 
        
        self.img_label1 = Label(window, text=bg_img1_order,height=1, width=30)
        self.img_label1.pack()
        
        img = ImageTk.PhotoImage(file = "../VoteImage/image1.jpg")
        print("image ", img.height)
        self.panel1 = Label(window, image = img , height=240 ,width=330)
        panel.image = img
        self.panel1.pack()
        
        self.img_label2 = Label(window, text=bg_img2_order,height=1, width=30)
        self.img_label2.pack()
        
        img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
        self.panel2 = Label(window, image = img2 , height=240 ,width=330)
        panel2.image = img2
        self.panel2.pack()
        
        self.img_label3 = Label(window, text=bg_img3_order,height=1, width=30)
        self.img_label3.pack()
        
        img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
        self.panel3 = Label(window, image = img3 , height=240 ,width=330)
        panel3.image = img3
        self.panel3.pack()

        # self.window.after(1000,self.refresh,self.window)
        # self.refresh()
        # self.retrieveImages()

    # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
    def refresh(self):
        try:
            name_bg_file = open('../VoteImage/name_bg.txt','r')
            name_bg_file_lines = name_bg_file.read().splitlines()  
            bg_img1_name = name_bg_file_lines[0]
            bg_img2_name = name_bg_file_lines[1]
            bg_img3_name = name_bg_file_lines[2]
            
            img1 = ImageTk.PhotoImage(Image.open("../VoteImage/image1.jpg"))
            self.panel1.configure(image=img1)
            img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
            self.panel2.configure(image=img2)
            img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
            self.panel3.configure(image=img3)

        except:
            pass

        self.window.after(1000,self.refresh,self.window)

    def retrieveImages(self):
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)
            bg_pick1 = (random.randint(1, len(your_list)-1))
            while True :
                bg_pick2 = (random.randint(1, len(your_list)-1))
                if (bg_pick2 == bg_pick1) :
                    continue
                else:
                    break
            while True :
                bg_pick3 = (random.randint(1, len(your_list)-1))
                if (bg_pick3 == bg_pick1) :
                    continue
                elif (bg_pick3 == bg_pick2):
                    continue
                else:
                    break
            
            bg_img1 = your_list[bg_pick1][0]
            bg_img2 = your_list[bg_pick2][0]
            bg_img3 = your_list[bg_pick3][0]
            url_bg_img1 = your_list[bg_pick1][1]
            url_bg_img2 = your_list[bg_pick2][1]
            url_bg_img3 = your_list[bg_pick3][1]   
            save_img_bg = open('../VoteImage/image1.jpg','wb')
            save_img_bg.write(requests.get(url_bg_img1).content) 
            save_img_bg.close()  
            save_img_bg = open('../VoteImage/image2.jpg','wb')
            save_img_bg.write(requests.get(url_bg_img2).content) 
            save_img_bg.close()   
            save_img_bg = open('../VoteImage/image3.jpg','wb')
            save_img_bg.write(requests.get(url_bg_img3).content) 
            save_img_bg.close()  
            name_bg_file = open('../VoteImage/name_bg.txt','w')
            name_bg_file.write(bg_img1+"\n")
            name_bg_file.write(bg_img2+"\n")
            name_bg_file.write(bg_img3+"\n")

        self.window.after(45000,self.retrieveImages,self.window) 



# window = tk.Tk()
# window.title('Vote BG')
# window.geometry("350x800") 
# window.resizable(0, 0) 
# artManager = ArtManager2(window)
# window.mainloop()