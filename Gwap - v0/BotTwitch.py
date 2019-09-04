import socket, time, datetime, re

import Utils

class BotTwitch:

    def __init__(self):
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
        
        ### Code start runs
        self.s_prep = socket.socket()
        self.s_prep.connect((self.SERVER, self.PORT))
        self.s_prep.send(("PASS " + self.PASS + "\r\n").encode())
        self.s_prep.send(("NICK " + self.BOT + "\r\n").encode())
        self.s_prep.send(("JOIN #" + self.CHANNEL + "\r\n").encode())

        self.joinchat()
        self.readbuffer = ""
    
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

    def giving_stop_describing_signal(self, message):
        print("Stop describing now")
        self.sendMessage(message)
        self.isStopDescribingSignal = True
        self.isStopVotingSignal = False

    def giving_stop_voting_signal(self, message):
        print("Stop voting now")
        self.sendMessage(message)
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
            message = (line.split(":", 2))[2]
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
                print(user + " > " + message)         
                # sends private msg to the user (start line)
                PMSG = "/w " + user + " "
                

    ################################# Command ##################################
    ############ Here you can add as many commands as you wish of ! ############
    ############################################################################
                self.utils.writeFileLog(user,message) #write log file
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
                    writeFile2(user,"!a")
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
                elif (not self.isStopDescribingSignal) and (user != self.OWNER) and len(message.split(":")) == 2:
                    print(user + " and " + message)
                    self.utils.writeVoteAndTagsData(user, message, artManager.get_list_imgs(), self.game_session)
                    break
                elif (not self.isStopVotingSignal) and (user != self.OWNER) and message.startswith("#"):
                    print(user + " what is going on " + message)
                    self.utils.writeVoteData(user, message, artManager.get_list_imgs(), self.game_session)
                    break
                else:
                    # Replace all non-alphanumeric non-# characters in a string.
                    message = re.sub('[^0-9a-zA-Z#! ]+', '', message)
                    if (message == ""):
                        break
                    else:
                        self.utils.writeFile(user,message)
                        break      