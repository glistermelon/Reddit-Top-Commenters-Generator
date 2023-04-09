import requests
import json
import time
from datetime import datetime
import random

class Post():
    def __init__(self,post,*,subreddit):
        self.title = post['title']
        self.time = post['created_utc']
        self.pid = post['id']
        self.subreddit = subreddit

class Comment():
    total = 0
    def __init__(self,comment):
        Comment.total += 1
        self.author = comment['author']
        self.score = comment['score']
        self.time = comment['created_utc']

class Requester: # class to restrict requests to 1/sec
    last = 0     # to avoid rate limiting errors
    agent = None
    def get(link):
        while time.time() - Requester.last < 1:
            pass
        ret = requests.get(link,headers={'User-Agent':Requester.agent})
        Requester.last = time.time()
        return ret
    def post(link,*,headers=None):
        while time.time() - Requester.last < 1:
            pass
        ret = requests.post(link,headers={'User-Agent':Requester.agent})
        Requester.last = time.time()
        return ret
    def init():
        Requester.agent = ''.join([chr(65+int(random.random()*26)) for _ in range(20)])

def get_posts(*,after,before,subreddit):
    after -= 1 # Pushshift API treats after/before exclusively,
    before +=1 # but inclusivity is preferable for convenience
    data = []
    while True:
        fail = True
        res = requests.get(f"https://api.pushshift.io/reddit/search/submission?size=500&sort=created_utc&sort_type=asc&subreddit={subreddit}&after={after}&before={before}")
        while fail:
            try:
                chunk = json.loads(res.content)['data']
                fail = False
            except:
                res = requests.get(f"https://api.pushshift.io/reddit/search/submission?size=500&sort=created_utc&sort_type=asc&subreddit={subreddit}&after={after}&before={before}")
                # To account for timeout errors and rate limiting errors
        for post in chunk:
            data.append(Post(post,subreddit=subreddit))
        if len(chunk) == 0:
            break
        before = chunk[-1]['created_utc']
    return data

headers = {"User-Agent":"glistermelon"}

def scan_post(post:Post):
    data = []
    res = Requester.get(f"https://www.reddit.com/r/{post.subreddit}/comments/{post.pid}/.json?limit=1000")
    global comments
    comments = json.loads(res.content)[1]['data']['children']
    more = []
    while True:
        replies = []
        for comment in comments:
            if comment["kind"] == "more":
                more += comment["data"]["children"]
            else:
                comment = comment["data"]
                data.append(Comment(comment))
                if comment["replies"] != "":
                    for reply in comment["replies"]["data"]["children"]:
                        replies.append(reply)
        if len(more) == 0 and len(replies) == 0:
            break
        comments = [r for r in replies]
        for obj in more:
            res = Requester.post("https://www.reddit.com/api/morechildren?children={}&link_id=t3_{}&api_type=json&limit_children=false".format(
                obj,
                post.pid
                ))
            for part in json.loads(res.content)["json"]["data"]["things"]:
                cid = part["data"]["id"][3:]
                res = Requester.get(f"https://www.reddit.com/r/{post.subreddit}/comments/{post.pid}/comment/{cid}/.json")
                comments += json.loads(res.content)[1]["data"]["children"]
        more = []
    return data

def parse(comments):
    number = {}
    scores = {}
    for comment in comments:
        if comment.author != "[deleted]":
            try:
                scores[comment.author] += comment.score
                number[comment.author] += 1
            except:
                scores[comment.author] = comment.score
                number[comment.author] = 1
    sort_scores = {k:v for k,v in sorted([item for item in scores.items()],reverse=True,key=lambda x:x[1])}

    output = ""
    users = list(sort_scores.keys())
    for i in range(len(users)):
        key = users[i]
        output += f"{i+1}. u/{key} ({sort_scores[key]} points, {number[key]} comments)\n"
    return output[:-1]

def summary(subreddit,after,before,out):

    print("\nGathering posts...\n")
    posts = get_posts(
        after = int(datetime.strptime(after,"%d/%m/%Y %S-%M-%H").timestamp()),
        before = int(datetime.strptime(before,"%d/%m/%Y %S-%M-%H").timestamp()),
        subreddit = subreddit
        )

    comments = []
    for i in range(len(posts)):
        post = posts[i]
        comments += scan_post(post)
        print(f"{i+1} / {len(posts)} processed", end='\r')
    print("\n\n")

    with open(out,'w') as f:
        f.write(parse(comments))

    input("Finished. Press any key to continue...")

def main():
    subreddit = input("Enter subreddit name: ")
    times = 'h'
    while times == 'h':
        times = input("Enter date range (h for help): ")
        if times == 'h':
            print("\nDate Format: day/month/year seconds-minutes-hours")
            print("Data Range Format: [Date] > [Date] (two formatted dates separated by '>'")
            print("(Uses military time!)\n")
    file = input("Enter output file name: ")
    if '.' not in file:
        file += ".txt"

    times = times.split('>')
    after = times[0].strip()
    before = times[1].strip()

    Requester.init()
    summary(subreddit,after,before,file)

main()
