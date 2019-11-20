from tkinter import *
import tkinter as tk
import Utils
import json

class BotNotifier:
    def __init__(self, window, artManager, botTwitch):
        

        self.artManager = artManager
        self.botTwitch = botTwitch
        self.utils = Utils.Utils()

        text = 'Please describe pictures on the right of screen you prefer follow format "imageID:discription"\n'
        # text = 'Please describe pictures' + str(json.dumps(self.botTwitch.get_audiences().get_describers()))
        

        self.botTwitch.giving_stop_voting_signal(text) # stop voting at the beginning
        
        # in case of improving description when image shown again
        if bool(self.botTwitch.get_audiences().get_describers()):

            for describer, value in self.botTwitch.get_audiences().get_describers().items():
                other_role = value.get("other_role")
                msg = ""
                if other_role == "former_voter":
                    msg = describer + " turned from voter to describer as default with description he voted: "
                    text = text + describer + " turned from voter to describer as default with description he voted: \n"
                else:
                    text = text + describer + "  created the description: \n"
                    msg = describer + "  created the description: "
                for img, i in value.get('imgs').items():
                    msg = msg + ' '.join(str(key) + ":" + val for (key,val) in i.items()) + ' for image ' + img
                    text = text + ' '.join(str(key) + ":" + val for (key,val) in i.items()) + ' for image ' + img + '\n'
                msg = msg + 'Update your descriptions to get more vote if necessary'
                self.botTwitch.sendMessage(msg)
            text = text + 'Update your descriptions to get more vote if necessary'     
        
        self.label = Label(window, text=text, bg="green", fg="white", font="none 20 italic", wraplength=1250)
        self.label.place(x=10, y=870)

        top_score_text = self.set_top_score_text()

        self.top_score_label = Label(window, text=top_score_text, bg="blue", fg="white", font="none 20 italic")
        self.top_score_label.place(x=1310, y=870)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)

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
        # text = "Time of describing is up. " + str(json.dumps(self.botTwitch.get_audiences().get_describers()))

        # descriptions = self.botTwitch.get_descriptions()
        # if bool(descriptions):
        #     text = text + 'Please vote for these descriptions following format "#description_id":\n'
        if bool(self.botTwitch.get_audiences().get_describers()):
            text = text + 'Please vote for these descriptions following format "#description_id":\n'
            des_s = []
            for describer, value in self.botTwitch.get_audiences().get_describers().items():

                for img, i in value.get('imgs').items():
                    des = next(iter(str(key) + ':' + val for (key,val) in i.items()))
                    if des not in des_s:
                        des_s.append(des)
                        text = text + ' '.join(str(key) + ":" + val for (key,val) in i.items()) + ' for image ' + img
        
        # for k, v in descriptions.items():
        #     text = text + "     " + k + ": " + v 
        
        self.label.configure(text=text)
        self.botTwitch.giving_stop_describing_signal(text)
        self.utils.retrieveImages() # random retrieve other images

    def revert_label_text(self):

        self.botTwitch.setGameSession() # increase game session to next round
        self.botTwitch.refresh_desid()

        self.artManager.refresh() # refresh to new images
        
        self.botTwitch.get_audiences().refresh_players(self.artManager.get_images())

        text = 'Next round. Please describe pictures on the right of screen you prefer follow format "imageID:discription"\n'
        # text = "Next round. Please describe " + str(json.dumps(self.botTwitch.get_audiences().get_describers()))
        # in case of improving description when image shown again
        if bool(self.botTwitch.get_audiences().get_describers()):
            
            for describer, value in self.botTwitch.get_audiences().get_describers().items():
                other_role = value.get("other_role")
                msg = ""
                if other_role == "former_voter":
                    msg = describer + " just turned from voter to describer as default with description he voted: "
                    text = text + describer + " just turned from voter to describer as default with description he voted: \n"
                else:
                    text = text + describer + "  created the description: \n"
                    msg = describer + "  created the description: "
                for img, i in value.get('imgs').items():
                    msg = msg + ' '.join(str(key) + ":" + val for (key,val) in i.items()) + ' for image ' + img
                    text = text + ' '.join(str(key) + ":" + val for (key,val) in i.items()) + ' for image ' + img + '\n'
                msg = msg + 'Update your descriptions to get more vote if necessary'
                
                self.botTwitch.sendMessage(msg)
            text = text + 'Update your descriptions to get more vote if necessary'
            
        self.label.configure(text=text)

        self.botTwitch.giving_stop_voting_signal(text)
       
        
        
    
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
        participant_results = self.botTwitch.get_audiences().get_participants_results(images, game_session)

        for u, value in participant_results.items():
            
            game_session_value = value.get(game_session)

            if game_session_value is not None:
            
                added_score = game_session_value.get("added_score")
                if added_score is None:
                    print("added_score None")
                else:
                    print("added_score " + str(added_score))
                win_or_novoted_img_desid = game_session_value.get("img_w_des")
                # des_ids = game_session_value.get("des_ids")
                # des_list = []
                # for did in des_ids:
                #     des_list.append(descriptions.get(did))
                
                # des = ";".join(des_list)
                role = game_session_value.get("role")

                for img, vl in win_or_novoted_img_desid.items():
                    did = vl[0]
                    stt = vl[1]
                    score = vl[2]
                    if stt == "winning":
                        message = "      User " + u + " get rewarded score " + str(score) + " for description " + descriptions.get(did) + "\n"
                        self.utils.store_winning_user(u, game_session, img, descriptions.get(did), role)
                    else:
                        if score is not None:
                            print("GOOOD")
                            message = "      User " + u + " get minus score " + str(score) + " as punished for making poor description or voted " + descriptions.get(did) + "\n"
                        else:
                            print("I have no idea why score is none here")
                
                # if value.get("status") == "rewarded":
                    
                #     message = "      User " + u + " get rewarded score " + str(score) + "\n"
                    
                #     self.utils.store_winning_user(u, game_session, img, des, role)
                # else:

                #     message = "      User " + u + " get minus score " + str(score) + "as punished as making poor description or voted" + "\n"
 
                #     self.utils.store_winning_user(u, game_session, img, des, role)

                text = text + message

        self.label.configure(text=text)
        self.botTwitch.sendMessage(text)
        self.utils.store_participants_info(participant_results)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)
