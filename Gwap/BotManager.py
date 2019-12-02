from tkinter import *
import tkinter as tk
import Utils
import json

class BotNotifier:
    def __init__(self, artManager, botTwitch):
        

        self.artManager = artManager
        self.botTwitch = botTwitch
        self.utils = Utils.Utils()

        text = 'Please describe pictures in format "imageID:discription" Ex. 1:aaaa'
        

        self.botTwitch.giving_stop_voting_signal() # stop voting at the beginning   
        
        self.label = Label(self.artManager.Bottom, text=text, bg="white", fg="black", font="arial 40 italic", wraplength=1660)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        top_score_text = self.set_top_score_text()

        self.top_score_label = Label(self.artManager.Right, text=top_score_text, bg="white", fg="blue", font="arial 20 italic")
        self.top_score_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)

        self.session = 0
        self.twinkle_signal = 0
        self.update_label()
        # self.check_at_least_has_one_description() # start 
        self.create_notification_label()

    def check_at_least_has_one_description(self):
        while True:
            if len(self.botTwitch.get_audiences().get_describers()) == 1:
                self.update_label()
                break

    def set_top_score_text(self):
        top_score_text = "Ranking score:\n"
        top_participants = self.botTwitch.get_audiences().get_top_participants()
        if top_participants is not None:
            for participant in top_participants:
                top_score_text = top_score_text + participant[0] + ": " + str(participant[1].get("total_score")) + "\n"
        return top_score_text

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
            time = 18000
            self.label.after(time, self.showing_winner)
            self.session = 2
        else:
            time = 8000
            self.label.after(time, self.revert_label_text)
            self.session = 0
        self.label.after(time, self.update_label)
        

    def change_label_color(self):
        self.label.configure(fg="green")

    def revert_label_color(self):
        self.label.configure(fg="black")

    def change_label_text(self):
        self.botTwitch.giving_stop_describing_signal()
        self.artManager.Title.configure(text="Voting session")

        row1 = row2 = row3 = 2
        if bool(self.botTwitch.get_audiences().get_descriptions()):
            text = 'Please vote for a description of each image above in format "#description_id" Ex. #1'
            for des_id, value in self.botTwitch.get_audiences().get_descriptions().items():
                des = des_id + ":" + value[1]
                if value[0] == "1":
                    l7 = Label(self.artManager.Left, font=('arial', 20), text=des, bg="white", wraplength=420).grid(row=row1, column=0)
                    row1 += 1
                elif value[0] == "2":
                    l7 = Label(self.artManager.Left, font=('arial', 20), text=des, bg="white", wraplength=420).grid(row=row2, column=2)
                    row2 += 1
                else:
                    l7 = Label(self.artManager.Left, font=('arial', 20), text=des, bg="white", wraplength=420).grid(row=row3, column=4)
                    row3 += 1
        else:
            text = "There is no description to vote. Sad emoji."
        
        self.label.configure(text=text)
        self.utils.retrieveImages() # random retrieve other images
        

    def revert_label_text(self):

        self.botTwitch.setGameSession() # increase game session to next round
        self.botTwitch.refresh_desid()

        self.reset_description_labels()
        self.artManager.refresh() # refresh to new images
        
        self.botTwitch.get_audiences().refresh_players(self.artManager.get_images())
        

        text = 'Please describe pictures in format "imageID:discription" Ex. 1:aaaa'
            
        self.label.configure(text=text)

    def reset_description_labels(self):
        self.artManager.Left.destroy()

    def showing_winner(self):
        self.botTwitch.giving_stop_voting_signal()
        text = "Winners for this round are:\n"
        descriptions = self.botTwitch.get_audiences().get_descriptions()
        images = self.artManager.get_images()
        
        for img_id in images:
            des_id = self.botTwitch.get_audiences().get_winning_des_id_foreach_img(img_id)
            if des_id is not None:
                description = descriptions.get(des_id)[1]
                text = text + "   " + des_id + ": " + description + " for image " + img_id + "\n"
            else:
                text = text + "    No winner for image " + img_id + "\n"
        
        game_session = self.botTwitch.getGameSession()
        participant_results = self.botTwitch.get_audiences().get_participants_results(images, game_session, descriptions)

        for u, value in participant_results.items():
            
            game_session_value = value.get(game_session)

            if game_session_value is not None:
            
                added_score = game_session_value.get("added_score")
                message = "      User " + u + " get score " + str(added_score)
                text = text + message

        self.label.configure(text=text)
        self.utils.store_participants_info(participant_results)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)
        # self.botTwitch.sendMessage(text)
