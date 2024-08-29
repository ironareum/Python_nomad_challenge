from flask import Flask, render_template, request, redirect, send_file
from SO_extractor import get_job as SO_job
from WW_extractor import get_job as WW_job
from RM_extractor import get_job as RM_job
from save_to_csv import save_to_csv

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

db={}
app = Flask("Job_search")

@app.route('/')
def home():
  return render_template("home.html")

# 웹 캐시(cache)때문에 export 관련 로직이 무시되는 문제가 발생.
# 아래는 웹 캐시를 사용하지 않게 하는 코드. 
# IE 나 Chrome에서만 작동.
@app.after_request
def add_header(rqst):
    rqst.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    rqst.headers["Pragma"] = "no-cache"
    rqst.headers["Expires"] = "0"
    rqst.headers['Cache-Control'] = 'public, max-age=0'
    return rqst


@app.route('/search')
def search():
  word = request.args.get("word")
  if word is False:
     return redirect('/')
  if word: 
    print(f"chaning word '{word}' to '{word.lower()}'")
    word = word.lower()
    print(f"searching '{word}' in list: existing Jobs")
    existingJobs = db.get(word)
    if existingJobs:
      print(f"found '{word}' list: excisting Jobs")
      all_jobs = existingJobs
    else: 
      try: 
        print(f"{word} not in the list. searching {word} from each sites..")
        #call each sites' data
        SO= SO_job(word)
        print("searching from 'stackoverflow' ===> done")
        WW= WW_job(word)
        print("searching from 'weworkremotely ===> done")
        RM= RM_job(word)
        print("searching from 'remoteok' ========> done")
        #saving datas from each site in a list
        site=[SO, WW, RM]
        print(f"All '{word}' jobs from {len(site)} sites saved successfully in a list")
        #set all datas in a list
        all_jobs=[]
        for jobs in site:
          for job in jobs: 
            all_jobs.append(job)
        db[word] = all_jobs
        print(f"now you have final '{word}' jobs in a main data dict.")
      except: 
        #if word has 0 found.
        return render_template("error.html") 
  print("Done!")
  return render_template("search.html", jobs =all_jobs, word=word, num=len(all_jobs) )

@app.route('/export')
def export():
  word = request.args.get("word")
  print(f"//export// the word is {word}")
  if not word:
    raise Exception()
  word = word.lower()
  all_jobs = db.get(word)
  if not all_jobs:
    raise Exception()
  save_to_csv(all_jobs,word)
  print("saved to csv")
  return send_file("Jobs.csv", as_attachment=True, attachment_filename=word)

app.run(host="0.0.0.0")
