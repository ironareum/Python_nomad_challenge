import os
import csv
import requests
from bs4 import BeautifulSoup
#from alba import get_job

os.system("clear")

alba_url = "http://www.alba.co.kr"
request = requests.get(alba_url)
soup = BeautifulSoup(request.text, "html.parser")

def main_page():
  companies = soup.find("div", {"id":"MainSuperBrand"}).find("ul",{"class","goodsBox"})
  companies = companies.find_all("li")
  return companies[:10]

def extract_jobs(companies):
  jobs =[]
  for company in companies:
    print("extracting jobs")
    company_name = company.find("span",{"class":"company"}).text
    file = open(f"{company_name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    
    link = company.find("a")["href"]
    job_request = requests.get(link)
    soup = BeautifulSoup(job_request.text, "html.parser")
    infos = soup.find("div", {"id":"NormalInfo"}).find("tbody").find_all("tr",{"class":""})
    for info in infos:
      try:
        place_ = info.find("td", {"class":"local"}).text
        place_ = place_.replace(u"\xa0",u" ")
        title_ = info.find("td",{"class":"title"}).find("span",{"class":"title"}).string
        time_ = info.find("td",{"class":"data"}).find("span",{"class":"time"}).string
        pay_icon = info.find("td",{"class":"pay"}).find("span",{"class":"payIcon"}).string
        pay_number = info.find("td",{"class":"pay"}).find("span",{"class":"number"}).string
        date_ = info.find("td",{"class":"regDate"}).string
      except:
        continue
      job = {
        "place": place_,
        "title": title_,
        "time": time_,
        "pay":  f"{pay_icon} {pay_number}",
        "date": date_}
      writer.writerow(job.values())
      jobs.append(job)
  
  return jobs

def get_job():
  mainpage = main_page()
  jobs = extract_jobs(mainpage)
  return jobs

jobs = get_job()
print(jobs)




