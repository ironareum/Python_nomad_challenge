import requests 
from bs4 import BeautifulSoup
#import datetime

def extract_each_jobs(job):
  title = job.find("h2",{"itemprop":"title"}).text
  company = job.find("a",{"class":"companyLink"}).find("h3",{"itemprop":"name"}).text
  location = ""
  link = job.find("a",{"class":"preventLink"})["href"]
  link = f"https://remoteok.io{link}"
  upload = str(job.find("td",{"class":"time"}).find("a").text)
  if "d" in upload:
    upload = upload.replace("d", " days ago")
  if "h" in upload:
    upload = upload.replace("h", " hours ago")
  if "mo" in upload:
    upload = upload.replace("mo", " months ago")
  if "yr" in upload:
    upload = upload.replace("yr", " years ago")
  ''' 
  ===========================================================
   Gotta fix it after learn about 'datetime' & sorted later.
  ===========================================================
  upload = str(job.find("td",{"class":"time"}).find("a").find("time")["datetime"])
  month = datetime.datetime(int(upload[5:7]))
  month = datetime.datetime.strftime(month, "%b")
  print(upload, month)
  '''
  return {
    "title": title,
    "company": company,
    "link": link,
    "location": location,
    "upload": upload,
    "from": "remoteok.io"
  }

def extract_jobs(url):
  jobs_list =[]
  requests_ = requests.get(url)
  soup = BeautifulSoup(requests_.text,"html.parser")
  jobs = soup.find_all("tr",{"class":"job"})
  for job in jobs:
    job = extract_each_jobs(job)
    jobs_list.append(job)
  return jobs_list

def get_job(word_):
  url =f"https://remoteok.io/remote-dev+{word_}-jobs"
  jobs = extract_jobs(url)
  return jobs