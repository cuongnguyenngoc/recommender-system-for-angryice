import socket
import datetime
import re
import threading
import time

from PIL import Image
import requests
from io import BytesIO
import random
import csv

import codecs
import webbrowser

from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

### Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667 # port
### Options (Edit this)
PASS = "oauth:kykwow2afwwea6yvu92d6qoebt44c3"  # bot password can be found on https://twitchapps.com/tmi/
BOT = "botch932"  # Bot's name [NO CAPITALS]
CHANNEL = "ch932"  # Channal name [NO CAPITALS]
OWNER = "ch932"  # Owner's name [NO CAPITALS]

### global variables
isStopDescribingSignal = False
isStopVotingSignal = False

### Functions

def writeFileLog(user,message):
    f = open("chat_log.txt", "a")
    f.write("Time="+str(datetime.datetime.now())+" Name="+user+" Message="+message+"\n")

def writeVoteAndTagsData(user, message):
    global bg_img1
    global bg_img2
    global bg_img3

    f = open("votetag_log.txt", "a")
    lines = message.split(":")
    vote = lines[0]
    description = lines[1]
    picname = bg_img1
    if (int(vote) == 2):
        picname = bg_img2
    elif (int(vote) == 3):
        picname = bg_img3
    f.write(user + "," + picname + "," + description + "\n")

def writeFile(user,message):
    ### open chat.txt and append
    f = open("../AngryICE/chat.txt", "a")
    ### write user name and message 
    f.write(user+":"+message+"\n")
    
def writeFile2(user,message):
    ### open chat.txt and append
    f = open("../AngryICE2/chat.txt", "a")
    ### write user name and message 
    f.write(user+":"+message+"\n")    
    
def writeFileVote(user,message):
    ### open bg_vote.txt and append
    f = open("../AngryICE/bg_vote.txt", "a")
    ### write user name and message 
    f.write(user+":"+message+"\n")    

def giving_stop_describing_signal():
    global isStopDescribingSignal
    global isStopVotingSignal
    print("Stop describing now")
    sendMessage(s, "Time is up for describing. Please voting these descriptions")
    isStopDescribingSignal = True
    isStopVotingSignal = False

def giving_stop_voting_signal():
    global isStopVotingSignal
    print("Stop voting now")
    sendMessage(s, "Time is up for voting")
    isStopVotingSignal = True

def readFileScore():
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
            sendMessage(s, "A win")
        elif (float(scoreA) < float(scoreB)):
            sendMessage(s, "B win")
        elif (float(scoreA) == float(scoreB)):
            sendMessage(s, "Draw")  
        ###this to clean scorea.txt file
        open("../AngryICE/scorea.txt", "w").close()
        ###this to clean scoreabtxt file
        open("../AngryICE2/scoreb.txt", "w").close() 
        voteBackground()
        RandomBackGround()
        
        # asking people vote and tag pictures
        time.sleep(3)
        global isStopDescribingSignal
        isStopDescribingSignal = False
        sendMessage(s, 'Please vote and describe pictures on the left of screen you prefer follow format "imageID:discription"')
        time.sleep(60)
        giving_stop_describing_signal()  # after 1 min stop receiving chat messages
        
        global isStopVotingSignal
        isStopVotingSignal = False
        time.sleep(15)
        giving_stop_voting_signal() # after 15 seconds stop receiving voting messages

        # t = threading.Timer(60.0, giving_stop_describing_signal)
        # t.start()

# start 
def RandomBackGround():
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
                continu
            elif (bg_pick3 == bg_pick2):
                continue
            else:
                break
        global bg_img1
        global bg_img2
        global bg_img3
        global url_bg_img1
        global url_bg_img2
        global url_bg_img3    
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
    
def voteBackground():
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
        save_img_bg.write(requests.get(url_bg_img1).content)
    elif (bg2 > bg1 and bg2 > bg3):
        save_img_bg.write(requests.get(url_bg_img2).content)
    elif (bg3 > bg2 and bg3 > bg1):
        save_img_bg.write(requests.get(url_bg_img3).content)          
    # 3 bg vote equal to random bg
    elif (bg1 == bg2 and bg2 == bg3):
        num_select = (random.randint(1, 3))
        if (num_select == 1 ):
            save_img_bg.write(requests.get(url_bg_img1).content)
        elif (num_select == 2):
            save_img_bg.write(requests.get(url_bg_img2).content)
        elif (num_select == 3):
            save_img_bg.write(requests.get(url_bg_img3).content)
    # 1 = 2 to random 1,2
    elif (bg1 == bg2):
        num_select = (random.choice('12'))
        if (int(num_select) == 1 ):
            save_img_bg.write(requests.get(url_bg_img1).content)
        elif (int(num_select) == 2):
            save_img_bg.write(requests.get(url_bg_img2).content)     
    # 2 = 3 to random 2,3
    elif (bg2 == bg3):
        num_select = (random.choice('23'))
        if (int(num_select) == 2 ):
            save_img_bg.write(requests.get(url_bg_img2).content)
        elif (int(num_select) == 3):
            save_img_bg.write(requests.get(url_bg_img3).content)  
    # 1 = 3 to random 1,3
    elif (bg1 == bg3):
        num_select = (random.choice('13'))
        if (int(num_select) == 1 ):
            save_img_bg.write(requests.get(url_bg_img1).content)
        elif (int(num_select) == 3):
            save_img_bg.write(requests.get(url_bg_img3).content)  
    ###this to clean bg_vote.btxt file
    save_img_bg.close()   
    open("../AngryICE/bg_vote.txt", "w").close() 
    
# end here, right?
# below this draw GUI
def drawGUIVote():  
    # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
    def refresh(mw):
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

        mw.after(1000,refresh,mw)
    
    name_bg_file = open('../VoteImage/name_bg.txt','r')
    name_bg_file_lines = name_bg_file.read().splitlines()  
    # bg_img1_name = name_bg_file_lines[0]
    # bg_img2_name = name_bg_file_lines[1]
    # bg_img3_name = name_bg_file_lines[2]
    bg_img1_name = "1"
    bg_img2_name = "2"
    bg_img3_name = "3"

    mw = tk.Tk()
    mw.title('Vote BG')
    mw.geometry("350x800") 
    mw.resizable(0, 0) 
    
    lightgray_bg = tk.Frame(master=mw,bg='lightgray')
    lightgray_bg.pack_propagate(0) 
    lightgray_bg.pack(fill=tk.BOTH, expand=1) 
    
    T = Label(mw, text=bg_img1_name,height=1, width=30)
    T.pack()
    
    img = ImageTk.PhotoImage(file = "../VoteImage/image1.jpg")
    panel = Label(mw, image = img , height=240 ,width=330)
    panel.pack()
    
    T2 = Label(mw, text=bg_img2_name,height=1, width=30)
    T2.pack()
    
    img2 = ImageTk.PhotoImage(Image.open("../VoteImage/image2.jpg"))
    panel2 = Label(mw, image = img2 , height=240 ,width=330)
    panel2.pack()
    
    T3 = Label(mw, text=bg_img3_name,height=1, width=30)
    T3.pack()
    
    img3 = ImageTk.PhotoImage(Image.open("../VoteImage/image3.jpg"))
    panel3 = Label(mw, image = img3 , height=240 ,width=330)
    panel3.pack()
    # asking people vote and tag pictures
    sendMessage(s, 'Please vote and describe pictures on the left of screen you prefer follow format "imageID:discription"')
    t = threading.Timer(60.0, giving_stop_describing_signal) # after 1 min stop receiving chat messages
    t.start()
    
    mw.after(1000,refresh,mw)
    mw.mainloop()

    # time.sleep(60)
    t.cancel()

    t1 = threading.Timer(15.0, giving_stop_voting_signal)
    t1.start()
    t1.cancel()

def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())
 
def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

def getMessage(line):
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message

def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
    sendMessage(s, "Chat room joined!")
    print("Bot has joined " + CHANNEL + " Channel!")
 
def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True
    
### Code start runs
s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())

s = s_prep
joinchat()
readbuffer = ""

def askForVote():
    while True:
        sendMessage(s, 'Please vote which picture you prefer')
        time.sleep(1000)

def Console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True
    
def CheckScoreProcess():
    while True:
        ### read score file
        readFileScore()

        time.sleep(3)
        
def MainBotProcess():
    global isStopDescribingSignal   
    while True:
        try:
            readbuffer = s.recv(2048)
            readbuffer = readbuffer.decode()
            temp = readbuffer.split("\n")
            readbuffer = readbuffer.encode()
            readbuffer = temp.pop()
        except:
            temp = ""
        for line in temp:
            if line == "":
                break
            # So twitch doesn't timeout the bot.
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                print(msgg)
                break
            # get user
            user = getUser(line)
            # get message send by user
            message = getMessage(line)
            # for you to see the chat from CMD             
            print(user + " > " + message)         
            # sends private msg to the user (start line)
            PMSG = "/w " + user + " "
            

################################# Command ##################################
############ Here you can add as many commands as you wish of ! ############
############################################################################
            writeFileLog(user,message)#write log file
            if (user == OWNER) and (message == "!next\r"):
                writeFile(user,"!next")
                sendMessage(s, "Next level")
                break
            elif (user == OWNER) and (message == "!retry\r"):
                writeFile(user,"!retry")
                sendMessage(s, "Retry level")
                break  
            elif (user == OWNER) and (message == "!s\r"):#Shoot
                writeFile(user,"!s")
                break
            elif (message == "!aa\r")  or (message == "!AA\r"):#Ability  #user1     
                writeFile(user,"!a")
                break            
            elif (message == "!am\r")  or (message == "!AM\r"):       
                writeFile(user,"!m")
                break
            elif (message == "!al\r") or (message == "!AL\r"):       
                writeFile(user,"!l")
                break
            elif (message == "!au\r") or (message == "!AU\r"):       
                writeFile(user,"!u")
                break
            elif (message == "!ad\r") or (message == "!AD\r"):       
                writeFile(user,"!d")
                break
            elif (message == "!ba\r")  or (message == "!BA\r"):#Ability   #user2
                writeFile2(user,"!a")
                break            
            elif (message == "!bm\r")  or (message == "!BM\r"):       
                writeFile2(user,"!m")
                break
            elif (message == "!bl\r") or (message == "!BL\r"):       
                writeFile2(user,"!l")
                break
            elif (message == "!bu\r") or (message == "!BU\r"):       
                writeFile2(user,"!u")
                break
            elif (message == "!bd\r") or (message == "!BD\r"):       
                writeFile2(user,"!d")
                break   
            elif (message == "!bg1\r"):       
                writeFileVote(user,"!bg1")
                break  
            elif (message == "!bg2\r"):       
                writeFileVote(user,"!bg2")
                break 
            elif (message == "!bg3\r"):       
                writeFileVote(user,"!bg3")
                break             
            elif (user != OWNER) and (message == "!next\r"):
                sendMessage(s, "This is private command for ownner.")
                break   
            elif (user != OWNER) and (message == "!retry\r"):
                sendMessage(s, "This is private command for ownner.")
                break
            elif not isStopDescribingSignal and (user != OWNER) and len(message.split(":")) == 2:
                print(user + " and " + message)
                writeVoteAndTagsData(user, message)
                break
            else:
                # Replace all non-alphanumeric non-# characters in a string.
                message = re.sub('[^0-9a-zA-Z#! ]+', '', message)
                if (message == ""):
                    break
                else :
                    writeFile(user,message)
                    break      
############################################################################
RandomBackGround()

thread1 = threading.Thread(target=MainBotProcess)
thread1.start()

thread2 = threading.Thread(target=CheckScoreProcess)
thread2.start()

thread3 = threading.Thread(target=drawGUIVote)
thread3.start()

