import os
import json
import praw
import time
import keyboard
import random as r
import webbrowser as web
import pygetwindow as pgw
from datetime import datetime
from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx

os.system("cls")

##########################################################################################################################

with open("original.json") as f:
#with open("config.json") as f:
    data = json.load(f)

reddit_data = data["reddit"]
reddit = praw.Reddit(client_id=reddit_data["client_id"], client_secret=reddit_data["client_secret"], user_agent=reddit_data["user_agent"])
posts = []
url = []
load_time = 40 
version_no = data["version_no"]
# titles = []


reg_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
brow = ""
final_browser = ""

sleeptm = None

##########################################################################################################################

def red():
    global posts,url,reddit
    #reddit_list = ['all','Jokes','TwoSentenceHorror','WTF','Funny','TwoSentenceComedy']
    #choice = r.choice(reddit_list)
    choice="TwoSentenceHorror"
    #print ("\nShuffled subreddit is : ",choice)
    if "WTF" in choice or "Funny" in choice:
        pass
    else:
        hot_posts = reddit.subreddit(choice).top(limit=50)
        for i in hot_posts:
            # Filtering Process
            # Filtering all posts that are contests or by mods on reddit
            if "contest" in i.title.lower() or "prize" in i.title.lower() or "mods" in i.title.lower():
                pass
            else:
                # Filtering posts with too morbid words
                if "rape" in i.selftext:
                    pass
                else:
                    if i.score>500:
                        #titles.append(i.title)
                        posts.append(i.title+" "+i.selftext)
                        url.append(i.url)
#         for i in range(len(posts)):
#             print (titles[i],end="\n-------\n")
#             print (posts[i],end="\n#########\n\n")

##########################################################################################################################

def browser():
    global brow, final_browser, load_time, reg_path
    flag = 0
    with OpenKey(HKEY_CURRENT_USER, reg_path) as key:
        brow = list(QueryValueEx(key,'ProgId'))
    BROWSER = ["firefox","chrome","edge","opera"]
    for i in BROWSER:
        if brow[0].lower().find(i) != -1:
            final_browser = i
    apps = pgw.getAllTitles()
    open_apps = []
    for i in apps:
        if i != "":
            open_apps.append(i.lower())
    for i in open_apps:
        if i.find(final_browser) != -1:
            flag = 0
            break
        else:
            flag = 1

    if flag == 1:
        web.open("-n")
        print ("\n\n\t\t\tTHE DEFAULT BROWSER IS NOT OPEN. OPENING DEFAULT BROWSER!!!!\n\n")

##########################################################################################################################

def sendwhatmsg(phone_no, message, time_hour, time_min, wait_time=20, print_waitTime=True):
    '''Sends whatsapp message to a particulal number at given time
Phone number should be in string format not int
***This function will not work if the browser's window is minimised,
first check it by calling 'check_window()' function'''
    global sleeptm
    # if "+" not in phone_no:
    #     raise CountryCodeException("Country code missing from phone_no")
    timehr = time_hour

    # if time_hour not in range(0,25) or time_min not in range(0,61):
    #     print("Invalid time format")
    
    if time_hour == 0:
        time_hour = 24
    callsec = (time_hour*3600)+(time_min*60)
    
    curr = time.localtime()
    currhr = curr.tm_hour
    currmin = curr.tm_min
    currsec = curr.tm_sec

    if currhr == 0:
        currhr = 24

    currtotsec = (currhr*3600)+(currmin*60)+(currsec)
    lefttm = callsec-currtotsec

    if lefttm <= 0:
        lefttm = 86400+lefttm

    if lefttm < wait_time:
        raise CallTimeException("Call time must be greater than wait_time as web.whatsapp.com takes some time to load")
    
    date = "%s:%s:%s"%(curr.tm_mday,curr.tm_mon,curr.tm_year)
    time_write = "%s:%s"%(timehr,time_min)
    file = open("whatsapp_dbs.txt","a")
    file.write("Date: %s\nTime: %s\nPhone number: %s\nMessage: %s"%(date,time_write,phone_no,message))
    file.write("\n--------------------\n")
    file.close()
    sleeptm = lefttm-wait_time
    if print_waitTime :
        print(f"In {sleeptm} seconds web.whatsapp.com will open and after {wait_time} seconds message will be delivered")
    time.sleep(sleeptm)
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message,new=2, autoraise=True)
    time.sleep(2)
    # width,height = pg.size()
    # print ("PG SIZE : ",pg.size())
    # pg.click(width/2,height/2)
    time.sleep(wait_time-2)
    # pg.press('enter')

#########################################################################################################################

def main():
    global posts, url, load_time, version_no
    reddit_flag = 0
    detail_flag = 0
    print ("\t\t\t\t\t\t\t  CODE BY @outcastdreamer on Github. \n\t\t\t\t\t\t\t\t   Version_No :",version_no)
    print ("\t\t\t\t\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print ("\n\n\t\tPLEASE MAKE SURE YOU ARE LOGGED IN TO \"web.whatsapp.com\" & HAVE SCANNED THE QR CODE!!\n\n")
    while True:
        pin = input("\nPlease enter the country code (Eg: +91, +1, etc) :\n\n\tKindly make sure Plus (+) symbol is there in the beginning of pincode : ")
        
        num = input("\tEnter the Mobile No. to send message to : ")
        opp_count = int(input("\tEnter the No. of messages to send : "))
        final = opp_count
        if pin[0] != "+":
            pin = "+" + pin
        if pin == "+91":
            if len(num) != 10:
                print ("\n\n\t\tERROR!! WRONG NUMBER!! THERE ARE LESS THAN 10 DIGITS!! TRY AGAIN!\n\n")
                detail_flag = 1
            else:
                detail_flag = 0
        if detail_flag != 1:
            f_num = pin+num
            print ("\n\n")
            print ("\t\t\t\t\tDETAILS : ")
            print ("\t\t\tPhone Number : ",f_num)
            print ("\t\t\tNo. of Messages to send : ",opp_count,"\n")
            choice = input("\nAre the following details correct? Please check & enter 'Y' for yes, 'N' for no : ")
            if choice.lower()=="y":
                break
        else:
            pass

    ##################

    reddit_checker = input("\n\n  Do you want to use the Reddit API (in case Reddit API details have not been set)? Type 'Y' to include Reddit API or 'N'for no : ")
    if reddit_checker.lower() == "y":
        reddit_flag = 1
        red()
    else:
        string = input("\n\tEnter the string you want to send to the user : ")
        reddit_flag = 0

    ##################

    count = 0
    #opp_count = 3
    flag = 0
    post_flag = 0
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    ##################

    while keyboard.is_pressed("q")==False:

        if count >= final:
            print ("\t\t\t\t\t\t\t--x--------------END OF EXECUTION--------------x--\n\n\n\n")
            break

        while count < final:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            m = int(current_time[-2:])+2

            ##################
            if reddit_flag == 1:
                s = r.choice(posts)
                index = posts.index(s)
                posts.pop(index)
                url_index = url[index]
                url.pop(index)
            ##################

            browser()

            print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print ("\n\nThe Current time is : ",current_time)
            hr = current_time[0:2]
            mn = int(current_time[-2:])+6

            if len(str(mn))==1:
                mn = "0"+str(mn)
                flag = 1

            if flag == 1:
                pass
            else:
                if int(mn) == 60:
                    mn = "00"
                    hr = int(hr)+1
                    if hr>23:
                        hr = "00"
                    if len(str(hr))==1:
                        hr = "0"+str(hr)
                    hr = str(hr)
                    flag = 2

            if flag == 2:
                pass
            else:
                if int(mn) > 60:
                    mn = "0"+str(mn%60)
                    hr = int(hr)+1
                    if hr>23:
                        hr = "00"
                    if len(str(hr))==1:
                        hr = "0"+str(hr)
                    hr = str(hr)

            t = str(hr)+":"+str(mn)
            flag = 0

            ################
            if reddit_flag == 1:
                if final == 1:
                    
                    string = """*----*%0aHi!!%0a%0aThis is an Automated Horror bot!!%0aI am currently sharing a randomly retrieved Short Horror Story from r/TwoSentenceHorror on Reddit.%0aHere's the story I have randomly retrieved : %0a%0a*----------------------------------------*%0a%0a_{0}_%0a%0a*---------------------------------------*%0a%0aTo view the whole post on reddit, click on : %0a{1}%0a%0aI hope you like it!!%0a%0aFeel free to checkout this project on github at : %0a{2}%0a%0aI hope you have a good day.%0aByeeee!!!%0a*--x----x--x----x--*""".format(s,url_index,"http://bit.ly/Automated_Whatsapp_Reddit")
                    post_flag = 1

                if count == 0 and final != 1:
                    
                    opp_count-=1
                    string = """*----*%0aHi!!%0a%0aThis is an Automated Horror bot!! %0aI am currently sharing a randomly retrieved Short Horror Story from r/TwoSentenceHorror on Reddit.%0aHere's the story I have randomly retrieved : %0a%0a*----------------------------------------*%0a%0a_{0}_%0a%0a*---------------------------------------*%0a%0aTo view the whole post on reddit, click on : %0a{1}%0a%0aI hope you like it!!%0a%0aMy next message will reach by {2} Hrs approx.!%0aThis bot will run for {3} more times!!%0a%0a""".format(s,url_index,t,opp_count)

                else:
                    if opp_count!=1:
                     
                        opp_count-=1
                        if opp_count == 1:
                            string = """*----*%0aAutomated Horror Bot Here!!%0a%0aTime for the story I have randomly retrieved : %0a%0a*----------------------------------------*%0a%0a_{0}_%0a%0a*---------------------------------------*%0a%0aTo view the whole post on reddit, click on : %0a{1}%0a%0aI hope you like it!!%0a%0aMy next message will reach by {2} Hrs approx.!%0aThis bot will run for {3} more time!!""".format(s,url_index,t,opp_count)
                            
                        else:
                            string = """*----*%0aAutomated Horror Bot Here!!%0a%0aTime for the story I have randomly retrieved : %0a%0a*----------------------------------------*%0a%0a_{0}_%0a%0a*---------------------------------------*%0a%0aTo view the whole post on reddit, click on : %0a{1}%0a%0aI hope you like it!!%0a%0aMy next message will reach by {2} Hrs approx.!%0aThis bot will run for {3} more times!!""".format(s,url_index,t,opp_count)
                    
                    elif opp_count==1 and post_flag != 1:
                        string = """*----*%0aAutomated Horror Bot Here for the last time :(%0a%0aTime for the story I have randomly retrieved : %0a%0a*----------------------------------------*%0a%0a_{0}_%0a%0a*---------------------------------------*%0a%0aTo view the whole post on reddit, click on : %0a{1}%0a%0aI hope you like it!!%0a%0aFeel free to checkout this project on github at : %0a{2}%0a%0aSorry for all the spam. I hope you have a good day.%0aByeeee!!!%0a*--x----x--x----x--*""".format(s,url_index,"http://bit.ly/Automated_Whatsapp_Reddit")                 
         
            try:
                count += 1
                time.sleep(2)

                ####################################################
                sendwhatmsg(f_num,string,int(current_time[:2]),m)
                ####################################################

                time.sleep(load_time)
                #click(1274,685)
                keyboard.send("enter")
                time.sleep(3)
                keyboard.send("enter")
                print("\n\t--Message has been sent!!--")
                time.sleep(7)
                keyboard.send("ctrl+F4")
                print ("\t--Whatsapp has been closed!!--")

                ################
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print ("\nNo. of messages sent : ",count,"\nMessage Sent at : ",current_time,"\n----\n")
                if count >= final:
                    break
                else:
                    print ("Initiating pause of 100 seconds!\n")
                    time.sleep(100)
                    print ("Sleep Time is over!!\n")
            
            except:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print("\n\n+++++++++++++++++++++++++++++")
                print("\t\t!!!EXCEPTION CAUGHT!!!\n\n")
                time.sleep(2)

                ####################################################
                sendwhatmsg(f_num,string,int(current_time[:2]),m+1)
                ####################################################

                time.sleep(load_time)
                keyboard.send("enter")
                time.sleep(3)
                keyboard.send("enter")
                #click(1274,685)
                print("\n--Message has been sent!!--")
                time.sleep(7)
                keyboard.send("ctrl+F4")
                print ("--Whatsapp has been closed!!--")
                ################
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print ("\nNo. of messages sent : ",count,"\nMessage Sent at : ",current_time,"\n----\n")
                if count >= final:
                    break
                else:
                    print ("\nInitiating pause of 100 seconds!\n")
                    time.sleep(100)
                    print ("Sleep Time is over!!\n")
                
#########################################################################################################################
                
main()

#########################################################################################################################

