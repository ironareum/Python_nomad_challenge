import requests
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript", 
    "python", 
    "reactjs", 
    "reactnative", 
    "programming", 
    "css",
    "golang", 
    "flutter", 
    "rust", 
    "django"
]

db = {}
post_list = []
def get_post(list_, key):
    for post in list_:
        voteNum = str(post.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).string)
        if not voteNum:
            voteNum = 0
        if "k" in voteNum:
            voteNum = int(float(voteNum.strip("k")) * 1000)
        else:
            try:
                voteNum = int(voteNum)
            except:
                voteNum = 0
        print("got NUM data")
        title = post.find("div", {
            "class": "_2FCtq-QzlfuN-SwVMUZMM3"
        }).find("h3", {
            "class": "_eYtD2XCVieq6emjKBH3m"
        }).string
        print("got TITLE data")
        link = post.find(
            "div", {
                "class": "y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE"
            }).find("a")["href"]
        link = f"https://www.reddit.com{link}"
        print("got LINK data")
        post_ = {"voteNum": voteNum, "title": title, "link": link, "key": key}
        post_list.append(post_)
    return post_list


def subreddit_list(key):
    try:
        url = f"https://www.reddit.com/r/{key}/top/?t=month"
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")
        key_lists = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
        #print("{key} lists checked successfully")
        list_ = key_lists.find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})
        #print("{key} list checked successfully")
        #Get post data
        post_list = get_post(list_, key)
        #print("======post_list: ", post_list)
        #print("get data successfully")
        #Sorting
        sorted_list = sorted(post_list, key=(lambda x: -x['voteNum']))
        #print("sorting successfully")
        #Save in db[key]
        db[key] = sorted_list
        #call_DB
        subreddit_posts = db[key]
        return subreddit_posts
    except:
        return redirect('/')


app = Flask("DayEleven")


@app.route('/')
def home():
    return render_template("home.html", subreddits=subreddits)


@app.route('/read')
def read():
    keys = request.args.to_dict().keys()
    for key in keys:
      existing_DB = list(db.keys())
      print("DB HAS: ",existing_DB)
      print(f"===Searching {key} posts...")
      subreddit = subreddit_list(key)
      print(f"===Found {len(subreddit)} of {key} posts...")
    print("====SAVED IN MY DB: ", list(db.keys()))
  
    return render_template("read.html", keys=keys, subreddit=subreddit)


app.run(host="0.0.0.0")
