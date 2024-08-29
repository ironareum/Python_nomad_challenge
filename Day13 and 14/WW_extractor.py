import requests 
from bs4 import BeautifulSoup


def extract__each_job(job):
  title = job.find("span",{"class":"title"}).text
  company = job.find("span",{"class":"company"}).text
  location = job.find("span",{"class":"region"})
  if location is not None:
    location = location.text
  else:
    location = ""
  link = job.find("a")["href"]
  link = f"https://weworkremotely.com/{link}"
  upload = job.find("span",{"class":"date"})
  if upload is not None:
    upload = upload.text
  else: upload = "New"
  return {
    "title":title,
    "company": company,
    "link": link,
    "location": location,
    "upload": upload,
    "from": "weworkremotely.com"
  }
  

def extract_jobs(url):
  jobs_list=[]
  request = requests.get(url)
  soup = BeautifulSoup(request.text, "html.parser")
  jobs = soup.find("section",{"id":"category-2"}).find_all("li",{"class":"feature"})
  for job in jobs:
    job = extract__each_job(job)
    jobs_list.append(job)
  return jobs_list

def get_job(word_): 
  ww_url = f"https://weworkremotely.com/remote-jobs/search?term={word_}"
  jobs = extract_jobs(ww_url)
  return jobs