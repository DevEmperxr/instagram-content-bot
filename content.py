from time import sleep
from dotenv import load_dotenv
import praw
import instagrapi
import urllib.request
import os
import datetime

#load env variables
load_dotenv()



#login reddit
print('login into reddit...')
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    password=os.getenv('PASSWORD'),
    user_agent=os.getenv('USER_AGENT'),
    username=os.getenv('USERNAME'),
)
print('successfully logged in!' )
sleep(1)

#login instagram bot

bot = instagrapi.Client()
print('enter instagram username: ')
uname = input()
print('inter instagram password:')
pword = input()
print('Trying to login...')
bot.login(uname,pword)
userID = bot.user_id
info = bot.user_info(userID)
print('logged in as: '+ info.username)
print('Followers: '+ str(info.follower_count))
print('Followers: '+ str(info.following_count))
print('Post count: '+ str(info.media_count))

#hashtags
hashtags = '#meme #memes #funny #dankmemes #memesdaily #funnymemes #lol #humor #follow #dank #love #like #memepage #comedy #instagram #dankmeme #tiktok #anime #lmao #dailymemes #ol #fun #edgymemes #offensivememes #memestagram #bhfyp #funnymeme #instagood #memer #shitpost'


#post loop
print('starting the posting loop...')
while(True):
    print('getting new top today posts from r/meirl...')
    posts = reddit.subreddit('meirl').top(time_filter= 'day')
    queue = []
    #adds to queue only pictures
    print('adding compatible posts to the queue...')
    while(len(queue) < 8):
        for i in posts:
            if i.url.endswith('.jpg'):
                queue.append(i)
    #post items in queue
    print('queue started!')
    count = 0
    for i in queue:
        count +=1
        print('downloading post '+ str(count) + '...')
        urllib.request.urlretrieve(i.url, i.url[18:])
        #make caption variable here with hashtags and stuff
        print('download succesful!')
        print('uploading post '+ str(count) + '...')
        bot.photo_upload(i.url[18:],caption= i.title + '\n' + hashtags)
        bot.photo_upload_to_story(i.url[18:])
        print('uploaded succesfully at '+ datetime.datetime.now().strftime("%H:%M:%S"))
        print('next post in 3 hours')
        os.remove(i.url[18:])
        print('deleted image '+ str(count))
        sleep(1*60*60)