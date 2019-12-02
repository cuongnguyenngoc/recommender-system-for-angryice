import csv, requests, random, datetime, os, json
import pandas as pd

class Utils:
    def __init__(self):
        self.url_bg_img1 = ""
        self.url_bg_img2 = ""
        self.url_bg_img3 = ""

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
            self.url_bg_img1 = your_list[bg_pick1][1]
            self.url_bg_img2 = your_list[bg_pick2][1]
            self.url_bg_img3 = your_list[bg_pick3][1]   
            save_img_bg = open('../VoteImage/image1.jpg','wb')
            save_img_bg.write(requests.get(self.url_bg_img1).content) 
            save_img_bg.close()  
            save_img_bg = open('../VoteImage/image2.jpg','wb')
            save_img_bg.write(requests.get(self.url_bg_img2).content) 
            save_img_bg.close()   
            save_img_bg = open('../VoteImage/image3.jpg','wb')
            save_img_bg.write(requests.get(self.url_bg_img3).content) 
            save_img_bg.close()  
            name_bg_file = open('../VoteImage/name_bg.txt','w')
            name_bg_file.write(bg_img1+"\n")
            name_bg_file.write(bg_img2+"\n")
            name_bg_file.write(bg_img3+"\n")
    
    def voteBackground(self):
        vote_file = open("../AngryICE/bg_vote.txt", "r")
        vote_file_lines = vote_file.read().splitlines()
        # below this is score from bg_vote.tx bg1 score from !bg1 , bg2 score from !bg2 ....
        bg1 = 0
        bg2 = 0
        bg3 = 0
        for vote_line in vote_file_lines:  
            if ("1" == vote_line.split(":")[1][3:]):
                bg1 += 1
            elif ("2" == vote_line.split(":")[1][3:]):
                bg2 += 1
            elif ("3" == vote_line.split(":")[1][3:]):
                bg3 += 1
        save_img_bg = open('../VoteImage/image.jpg','wb')
        #below this to check if score equal or more or less and save image to image.jpg which one most score! || if score equal it randomly
        if (bg1 > bg2 and bg1 > bg3):
            save_img_bg.write(requests.get(self.url_bg_img1).content)
        elif (bg2 > bg1 and bg2 > bg3):
            save_img_bg.write(requests.get(self.url_bg_img2).content)
        elif (bg3 > bg2 and bg3 > bg1):
            save_img_bg.write(requests.get(self.url_bg_img3).content)          
        # 3 bg vote equal to random bg
        elif (bg1 == bg2 and bg2 == bg3):
            num_select = (random.randint(1, 3))
            if (num_select == 1 ):
                save_img_bg.write(requests.get(self.url_bg_img1).content)
            elif (num_select == 2):
                save_img_bg.write(requests.get(self.url_bg_img2).content)
            elif (num_select == 3):
                save_img_bg.write(requests.get(self.url_bg_img3).content)
        # 1 = 2 to random 1,2
        elif (bg1 == bg2):
            num_select = (random.choice('12'))
            if (int(num_select) == 1 ):
                save_img_bg.write(requests.get(self.url_bg_img1).content)
            elif (int(num_select) == 2):
                save_img_bg.write(requests.get(self.url_bg_img2).content)     
        # 2 = 3 to random 2,3
        elif (bg2 == bg3):
            num_select = (random.choice('23'))
            if (int(num_select) == 2 ):
                save_img_bg.write(requests.get(self.url_bg_img2).content)
            elif (int(num_select) == 3):
                save_img_bg.write(requests.get(self.url_bg_img3).content)  
        # 1 = 3 to random 1,3
        elif (bg1 == bg3):
            num_select = (random.choice('13'))
            if (int(num_select) == 1 ):
                save_img_bg.write(requests.get(self.url_bg_img1).content)
            elif (int(num_select) == 3):
                save_img_bg.write(requests.get(self.url_bg_img3).content)  
        ###this to clean bg_vote.btxt file
        save_img_bg.close()   
        open("../AngryICE/bg_vote.txt", "w").close()
    
    def writeFileVote(self, user, message):
        ### open bg_vote.txt and append
        f = open("../AngryICE/bg_vote.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
    

    def writeFile(self, user, message):
        ### open chat.txt and append
        f = open("../AngryICE/chat.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
        
    def writeFile2(self, user, message):
        ### open chat.txt and append
        f = open("../AngryICE2/chat.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
    
    def writeVoteData(self, user, img_id, description, images, game_session):

        f = open("vote_log.txt", "a")
        print("images in writevotedata " + json.dumps(images))
        print("user in writeVoteData " + str(user))
        print("description in writeVoteData " + str(description))
        print("game session in writeVoteData " + str(game_session))
        picname = images.get(img_id)
        print("img_id in writeVoteData " + str(img_id))
        print("pic name in writeVoteData " + str(picname))
        f.write(str(game_session) + "," + user + "," + picname + "," + description+"\n")

    def writeVoteAndTagsData(self, user, message, images, game_session):

        f = open("votetag_log.txt", "a")
        lines = message.split(":")
        img_id = lines[0]
        description = lines[1]
        if img_id in images:
            picname = images.get(img_id)
            f.write(str(game_session) + "," + img_id + "," + user + "," + picname + "," + description+"\n")
    
    def writeFileLog(self, user, message):
        f = open("chat_log.txt", "a")
        f.write("Time="+str(datetime.datetime.now())+" Name="+user+" Message="+message+"\n")

    def get_last_game_session(self):
        game_session = 1
        try:
            f = open('votetag_log.txt', 'r')
            lines = f.read().rstrip('\n').splitlines()
            last_line = lines[-1]
            game_session = int(last_line.split(",")[0])
        except:
            pass
        
        return game_session

    def store_winning_user(self, user, game_session, img, des, role):
        f = open("winning_users_log.txt", "a")
        f.write(str(game_session) + "," + user + "," + img + "," + des + "," + role + "\n")
    
    def store_punished_user(self, user, game_session, img, des, role):
        f = open("punished_users_log.txt", "a")
        f.write(str(game_session) + "," + user + "," + img + "," + des + "," + role + "\n")

    def get_old_participants_for_used_images(self, images):
        old_participants = {} ### {u8: {'imgs': {img1: {d1: "description"}, img2: {d6: "description"}}, 'role':'former_voter'}, 
                        ###  u9:...}
        tmp = self.get_img_descriptions_by_pythia(images)
        descriptions = tmp[0]

        print(json.dumps(descriptions))

        des_id = tmp[1]
        try:
            f = open('winning_users_log.txt', 'r')
            lines = f.read().splitlines()
            
            for line in lines:
                
                components = line.split(",")
                img_id = next((id for id, img in images.items() if img == components[2]), None)
                
                if img_id is not None:
                    old_participants[components[1]] = {"des": components[3], "des_id": str(des_id), "img_id": img_id, "other_role": components[4]}
                    if components[4] == "describer":
                        descriptions[str(des_id)] = (img_id, components[3])
                        des_id += 1
        except:
            pass
        return (old_participants, des_id, descriptions)

    def get_img_descriptions_by_pythia(self, images):
        df = pd.read_csv("uki-captions-pythia.csv", index_col=False)
        descriptions = {}

        des_id = 0
        for id, img in images.items():
            print("id " + id + " image " + img)
            try:
                descriptions[str(des_id)] = (id, df.loc[df['name'] == img]['caption_1'].values[0])
                descriptions[str(des_id + 1)] = (id, df.loc[df['name'] == img]['caption_2'].values[0])
                des_id += 2
            except:
                print("error ")

        return (descriptions, des_id)

    def store_participants_info(self, participants):
        with open('participants_info.txt', 'w') as outfile:
            json.dump(participants, outfile)
    
    def load_participants_info(self):
        participants = {}
        try:
            with open('participants_info.txt') as json_file:
                participants = json.load(json_file)
        except:
            pass
        return participants