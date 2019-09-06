from tkinter import *
import tkinter as tk
import Utils

class BotNotifier:
    def __init__(self, window, artManager, botTwitch):
        text = 'Please describe pictures on the right of screen you prefer follow format "imageID:discription"'
        self.label = Label(window, text=text, bg="green", fg="white", font="none 20 italic", wraplength=1250)
        self.label.place(x=10, y=870)

        self.artManager = artManager
        self.botTwitch = botTwitch
        self.utils = Utils.Utils()

        self.botTwitch.giving_stop_voting_signal(text) # stop voting at the beginning

        
        top_score_text = self.set_top_score_text()

        self.top_score_label = Label(window, text=top_score_text, bg="blue", fg="white", font="none 20 italic")
        self.top_score_label.place(x=1310, y=870)

        self.session = 0
        self.twinkle_signal = 0
        self.update_label()
        self.create_notification_label()

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
        text = "Time of describing is up. "

        descriptions = self.botTwitch.get_descriptions()
        if bool(descriptions):
            text = text + 'Please vote for these descriptions following format "#description_id":\n'
        
        for k, v in descriptions.items():
            text = text + "     " + k + ": " + v 
        
        self.label.configure(text=text)
        self.botTwitch.giving_stop_describing_signal(text)
        self.utils.retrieveImages() # random retrieve other images

    def revert_label_text(self):
        text = 'Next round. Please describe pictures on the right of screen you prefer follow format "imageID:discription"'
        self.label.configure(text=text)

        self.botTwitch.giving_stop_voting_signal(text)

        self.botTwitch.setGameSession() # increase game session to next round
        self.botTwitch.refresh_desid()
        
        self.botTwitch.get_audiences().refresh_players()
        if bool(self.botTwitch.get_audiences().get_describers()):
            self.botTwitch.sendMessage("some people are describers as default. And If your description u voted before is bad, please improve your description to get more vote")
        
        self.artManager.refresh()
    
    def showing_winner(self):
        text = "Time is up for voting. Winners for this round are:\n"
        descriptions = self.botTwitch.get_descriptions()
        images = self.artManager.get_images()
        
        for img_id in images:
            des_id = self.botTwitch.get_audiences().get_winning_des_id_foreach_img(img_id)
            if des_id is not None:
                description = descriptions.get(des_id)
                text = text + "   " + des_id + ": " + description + " for image " + img_id + "\n"
            else:
                text = text + "    No winner for image " + img_id + "\n"
        
        game_session = self.botTwitch.getGameSession()
        winning_participants = self.botTwitch.get_audiences().get_participants_results(images, game_session)

        for u, value in winning_participants.items():
            
            game_session_value = value.get(game_session)
            if game_session_value is not None:
                score = game_session_value.get("added_score")
                text = text + "      User " + u + " get score " + str(score)
                img = game_session_value.get("img")
                des_ids = game_session_value.get("des_ids")
                des_list = []
                for did in des_ids:
                    des_list.append(descriptions.get(did))
                
                des = ";".join(des_list)
                role = game_session_value.get("role")
                text = text + "  " + img + "  " + des + "  " + role
                self.utils.store_winning_user(u, game_session, img, des, role)
        
        self.label.configure(text=text)
        self.botTwitch.sendMessage(text)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)
        


