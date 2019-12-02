import socket, time, datetime, re, json

import Utils, Audiences

class BotTwitch:

    def __init__(self, artManager):
        ### Options (Don't edit)
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667 # port
        ### Options (Edit this)
        self.PASS = "oauth:kykwow2afwwea6yvu92d6qoebt44c3"  # bot password can be found on https://twitchapps.com/tmi/
        self.BOT = "botch932"  # Bot's name [NO CAPITALS]
        self.CHANNEL = "ch932"  # Channal name [NO CAPITALS]
        self.OWNER = "ch932"  # Owner's name [NO CAPITALS]
        self.utils = Utils.Utils()

        self.isStopDescribingSignal = False
        self.isStopVotingSignal = False
        self.game_session = self.utils.get_last_game_session() + 1
        # self.game_session = 0
        
        self.audiences = Audiences.Audiences(artManager.get_images())

        self.des_id = self.audiences.get_init_des_id()

        ### Code start runs
        self.s_prep = socket.socket()
        self.s_prep.connect((self.SERVER, self.PORT))
        self.s_prep.send(("PASS " + self.PASS + "\r\n").encode())
        self.s_prep.send(("NICK " + self.BOT + "\r\n").encode())
        self.s_prep.send(("JOIN #" + self.CHANNEL + "\r\n").encode())

        self.joinchat()
        self.readbuffer = ""
    
    def get_audiences(self):
        return self.audiences
    
    def set_audiences(self, audiences):
        self.audiences = audiences

    def get_img_id(self, des_id):
        if des_id in self.audiences.get_descriptions():
            return self.audiences.get_descriptions().get(des_id)[0]
        return None

    def refresh_desid(self):
        self.des_id = self.audiences.get_init_des_id()

    def joinchat(self):
        readbuffer_join = "".encode()
        Loading = True
        while Loading:
            readbuffer_join = self.s_prep.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            temp = readbuffer_join.split("\n")
            readbuffer_join = readbuffer_join.encode()
            readbuffer_join = temp.pop()
            for line in temp:
                Loading = self.loadingCompleted(line)
        self.sendMessage("Chat room joined!")
        print("Bot has joined " + self.CHANNEL + " Channel!")
    
    def loadingCompleted(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

    def giving_stop_describing_signal(self):
        print("Stop describing now")
        # self.sendMessage(message)
        self.isStopDescribingSignal = True
        self.isStopVotingSignal = False

    def giving_stop_voting_signal(self):
        print("Stop voting now")
        # self.sendMessage(message)
        self.isStopVotingSignal = True
        self.isStopDescribingSignal = False

    def Console(self, line):
        # gets if it is a user or twitch server
        if "PRIVMSG" in line:
            return False
        else:
            return True
    
    def sendMessage(self, message):
        message = "PRIVMSG #" + self.CHANNEL + " :" + message
        self.s_prep.send((message + "\r\n").encode())

    def getUser(self, line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        try:
            message = (line.split(":", 2))[2].rstrip("\n\r")
        except:
            message = ""
        return message

    def setGameSession(self):
        self.game_session += 1

    def getGameSession(self):
        return self.game_session
    
    def CheckScoreProcess(self):
        while True:
            ### read score file
            self.readFileScore()

            time.sleep(3)

    def readFileScore(self):
        ### open score.txt and read
        f = open("../AngryICE/scorea.txt", "r")
        f2 = open("../AngryICE2/scoreb.txt", "r")
        ### score teamA
        scoreA = (f.readline())
        ### score teamB
        scoreB = (f2.readline())
        ### if scoreA and scoreB file have parameters.
        if ( scoreA != "" and  scoreB != ""):
            if (float(scoreA) > float(scoreB)):
                self.sendMessage("A win")
            elif (float(scoreA) < float(scoreB)):
                self.sendMessage("B win")
            elif (float(scoreA) == float(scoreB)):
                self.sendMessage("Draw")
            
            ###this to clean scorea.txt file
            open("../AngryICE/scorea.txt", "w").close()
            ###this to clean scoreabtxt file
            open("../AngryICE2/scoreb.txt", "w").close() 
            self.utils.voteBackground()
            
    
    def MainBotProcess(self, artManager):
        while True:
            try:
                self.readbuffer = self.s_prep.recv(2048)
                self.readbuffer = self.readbuffer.decode()
                temp = self.readbuffer.split("\n")
                self.readbuffer = self.readbuffer.encode()
                self.readbuffer = temp.pop()
            except:
                temp = ""
            for line in temp:
                if line == "":
                    break
                # So twitch doesn't timeout the bot.
                if "PING" in line and self.Console(line):
                    msgg = "PONG tmi.twitch.tv\r\n".encode()
                    self.s_prep.send(msgg)
                    print(msgg)
                    break
                # get user
                user = self.getUser(line)
                # get message send by user
                message = self.getMessage(line)
                # for you to see the chat from CMD             
                # print(user + " > " + message)         
                # sends private msg to the user (start line)
                PMSG = "/w " + user + " "
                

    ################################# Command ##################################
    ############ Here you can add as many commands as you wish of ! ############
    ############################################################################
                self.utils.writeFileLog(user, message) #write log file

                if (user == self.OWNER) and (message == "!next\r"):
                    self.utils.writeFile(user,"!next")
                    self.sendMessage("Next level")
                    break
                elif (user == self.OWNER) and (message == "!retry\r"):
                    self.utils.writeFile(user,"!retry")
                    self.sendMessage("Retry level")
                    break  
                elif (user == self.OWNER) and (message == "!s\r"):#Shoot
                    self.utils.writeFile(user,"!s")
                    break
                elif (message == "!aa\r")  or (message == "!AA\r"):#Ability  #user1     
                    self.utils.writeFile(user,"!a")
                    break            
                elif (message == "!am\r")  or (message == "!AM\r"):       
                    self.utils.writeFile(user,"!m")
                    break
                elif (message == "!al\r") or (message == "!AL\r"):       
                    self.utils.writeFile(user,"!l")
                    break
                elif (message == "!au\r") or (message == "!AU\r"):       
                    self.utils.writeFile(user,"!u")
                    break
                elif (message == "!ad\r") or (message == "!AD\r"):       
                    self.utils.writeFile(user,"!d")
                    break
                elif (message == "!ba\r")  or (message == "!BA\r"):#Ability   #user2
                    self.utils.writeFile2(user,"!a")
                    break            
                elif (message == "!bm\r")  or (message == "!BM\r"):       
                    self.utils.writeFile2(user,"!m")
                    break
                elif (message == "!bl\r") or (message == "!BL\r"):       
                    self.utils.writeFile2(user,"!l")
                    break
                elif (message == "!bu\r") or (message == "!BU\r"):       
                    self.utils.writeFile2(user,"!u")
                    break
                elif (message == "!bd\r") or (message == "!BD\r"):       
                    self.utils.writeFile2(user,"!d")
                    break   
                elif (message == "!bg1\r"):       
                    self.utils.writeFileVote(user,"!bg1")
                    break  
                elif (message == "!bg2\r"):       
                    self.utils.writeFileVote(user,"!bg2")
                    break 
                elif (message == "!bg3\r"):       
                    self.utils.writeFileVote(user,"!bg3")
                    break             
                elif (user != self.OWNER) and (message == "!next\r"):
                    self.sendMessage("This is private command for ownner.")
                    break   
                elif (user != self.OWNER) and (message == "!retry\r"):
                    self.utils.sendMessage("This is private command for ownner.")
                    break
                elif (not self.isStopDescribingSignal) and self.isStopVotingSignal and (user != self.OWNER) and len(message.split(":")) == 2 and message.split(":")[0].isdigit():
                    print(user + " and " + message)

                    imgs = {}
                    if user in self.audiences.get_describers():
                        imgs = self.audiences.get_describers().get(user)
                    
                    img_id = message.split(":")[0]
                    description = message.split(":")[1]
                    images = artManager.get_images()

                    if img_id in images:
                        did = str(self.des_id)
                        if img_id in imgs:
                            self.sendMessage("You have updated description for image " + img_id)
                            did = next(iter(imgs.get(img_id))) #string
                        else:
                            self.des_id += 1
                        
                        self.audiences.get_descriptions()[did] = (img_id, description)
                        self.audiences.get_descriptions()[did] = (img_id, description)
                        imgs[img_id] = {did: description}
                        
                        self.audiences.get_describers()[user] = imgs

                        self.utils.writeVoteAndTagsData(user, message, images, self.game_session)

                        print("descriptions in botTwitch " + json.dumps(self.audiences.get_descriptions()))
                    else:
                        self.sendMessage("There is no typed image id shown on the screen. Please try again following the format.")
                    break
                elif (not self.isStopVotingSignal) and self.isStopDescribingSignal and (user != self.OWNER) and message.startswith("#"):                    

                    if user not in self.audiences.get_describers():

                        des_id = message.replace("#", "") # string
                        descriptions = self.audiences.get_descriptions()
                        if des_id in descriptions:
                            description = descriptions.get(des_id)[1]

                            is_voted = True
                            if user in self.audiences.get_old_participants():
                                if description == self.audiences.get_old_participants().get(user).get("des"):
                                    is_voted = False
                                    self.sendMessage("Sorry you cannot vote for this description because it was the winning description you voted or created before")
                            
                            if is_voted:

                                img_id = self.get_img_id(des_id)
                                
                                des_list = {}
                                if img_id in self.audiences.get_voters():
                                    des_list = self.audiences.get_voters().get(img_id)
                                
                                users = []
                                if des_id in des_list:
                                    users = des_list.get(des_id)
                                
                                    if user not in users:
                                        users.append(user)
                                        print("images in BotTwitch " + json.dumps(artManager.get_images()))
                                        self.utils.writeVoteData(user, img_id, description, artManager.get_images(), self.game_session)
                                    else:
                                        self.sendMessage("You already voted for this description.")
                                    
                                else: #des_id not in des_list
                                    total_users = []  # flatten to 1 array of all users voted for all descriptions
                                    for ds in self.audiences.get_voters().values():
                                        total_users = total_users + [u for sublist in ds.values() for u in sublist]
                                    
                                    if user not in total_users:
                                        users.append(user)
                                        self.utils.writeVoteData(user, img_id, description, artManager.get_images(), self.game_session)
                                    else:
                                        self.sendMessage("You cannot vote for more than one description.")
                                
                                if users: # store when users array not empty
                                    des_list[des_id] = users
                                    self.audiences.get_voters()[img_id] = des_list
                        else:
                            self.sendMessage("There is no typed description id shown on the list. Please try again.")
                    else:
                        self.sendMessage("Sorry you cannot vote since you are a describer. Wait for the next round if you wish.")
                    break
                elif (not self.isStopDescribingSignal) and self.isStopVotingSignal and message.startswith("#"):
                    self.sendMessage("Voting session is over. Please wait for its turn.")
                    break
                elif self.isStopDescribingSignal and not self.isStopVotingSignal and len(message.split(":")) == 2 and message.split(":")[0].isdigit():
                    self.sendMessage("You cannot describe picture in voting session.")
                    break
                else:
                    # Replace all non-alphanumeric non-# characters in a string.
                    message = re.sub('[^0-9a-zA-Z#! ]+', '', message)
                    if message == "":
                        break
                    else:
                        self.utils.writeFile(user,message)
                        break
