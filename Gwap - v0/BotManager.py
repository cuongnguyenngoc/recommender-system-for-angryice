from tkinter import *
import tkinter as tk
import Utils

class BotNotifier:
    def __init__(self, window, artManager, botTwitch):
        text = 'Please describe pictures on the right of screen you prefer follow format "imageID:discription"'
        self.label = Label(window, text=text, bg="green", fg="white", font="none 20 bold")
        self.label.place(x=10, y=940)
        self.artManager = artManager
        self.botTwitch = botTwitch

        self.botTwitch.giving_stop_voting_signal(text) # stop voting at the beginning

        self.session = 0
        self.twinkle_signal = 0
        self.update_label()
        self.create_notification_label()

    def create_notification_label(self):
        if self.twinkle_signal == 0:
            self.label.after(1000, self.change_label_color)
            self.twinkle_signal = 1
        else:
            self.label.after(1000, self.revert_label_color)
            self.twinkle_signal = 0
        
        self.label.after(1000, self.create_notification_label)
    
    def update_label(self):
        time = 60000
        if self.session == 0:
            self.label.after(time, self.change_label_text)
            self.session = 1
        elif self.session == 1:
            time = 15000
            self.label.after(time, self.showing_winner)
            self.session = 2
        else:
            time = 5000
            self.label.after(time, self.revert_label_text)
            self.session = 0
        self.label.after(time, self.update_label)
        

    def change_label_color(self):
        self.label.configure(fg="red")

    def revert_label_color(self):
        self.label.configure(fg="white")

    def change_label_text(self):
        try:
            des_list_file = open('votetag_log.txt','r')
            des_file_lines = des_list_file.read().splitlines()
            text = "Time of describing is up. Please vote for these descriptions \n"
            for line in des_file_lines:
                fields = line.split(",")
                if (len(fields) == 5):
                    if (int(fields[0]) == self.botTwitch.getGameSession()):
                        text = text + line.split(",")[1] + ":" + line.split(",")[4] + "\n"
        except:
            text = "Time of describing is up."
        
        self.label.configure(text=text)
        self.botTwitch.giving_stop_describing_signal(text)
        Utils.Utils().retrieveImages() # random retrieve other images

    def revert_label_text(self):
        text = 'Time is up for voting. Please describe pictures on the right of screen you prefer follow format "imageID:discription"'
        self.label.configure(text=text)

        self.botTwitch.giving_stop_voting_signal(text)

        self.botTwitch.setGameSession() # increase game session to next round

        self.artManager.refresh()
    
    def showing_winner(self):
        text = "Winners for this round are:"
        self.label.configure(text=text)
        self.botTwitch.sendMessage(text)
        


