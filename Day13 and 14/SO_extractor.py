import requests 
from bs4 import BeautifulSoup


def get_last_page(url):
  so_requests = requests.get(url)
  soup = BeautifulSoup(so_requests.text, "html.parser")
  try: 
    pages = soup.find_all("a", {"class":"s-pagination--item"})
    last_page = str(pages[-2].text).strip()
  except:
    print("Error from pagination.")
  return last_page


def extract__each_job(job):
  title = job.find("h2",{"class":"mb4"}).find("a")["title"]
  link = job.find("h2",{"class":"mb4"}).find("a")["href"]
  link = f"https://stackoverflow.com{link}"
  company, location = job.find("h3",{"class":"fc-black-700"}).find_all("span", recursive=False )
  if company:
    company = str(company.string).strip()
  else:
    company = ""
  if location:
    location = str(location.string).strip()
  else:
    location = ""
  upload = str(job.find("div",{"class":"fs-caption"}).find("div").string)
  if "d" in upload:
    upload = upload.replace("d", "days")
  if "h" in upload:
    upload = upload.replace("h", "hours")

  if not upload:
    upload =""  
  return {
    "title":title,
    "company": company,
    "link": link,
    "location": location,
    "upload": upload,
    "from": "stackoverflow.com"
  }


def extract_jobs(last_page, url):
  jobs_list =[]
  pages = int(last_page)
  for page in range(pages): 
    #print(f"Searching jobs in page{page+1}..")
    url = f"{url}&r=true&pg={page}"
    jobs_requests = requests.get(url)
    soup = BeautifulSoup(jobs_requests.text, "html.parser") 
    jobs = soup.find("div", {"class":"listResults"}).find_all("div",{"class":"-job"})
    for job in jobs:
      job = extract__each_job(job) 
      jobs_list.append(job)
  return jobs_list


def get_job(word_):
  URL = f"https://stackoverflow.com/jobs?r=true&q={word_}"
  last_page = get_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs