import os
import requests
from bs4 import BeautifulSoup

os.system("clear")

url = "https://www.iban.com/currency-codes"

request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')
table = soup.find("table", {"class":"table"})
tbody = table.find("tbody").find_all("tr")

list=[]

for tr in tbody:
  infos = tr.find_all("td")
  country = (infos[0].text).capitalize()
  co = infos[2].text
  if "No universal currency" not in infos[1]:
    a = {"name":country, "code":co}
    list.append(a)  
  #print(infos)
  #print(country)
  #print(co)
#print("list:",list[0]["name"])

def ask():
  try:
    num = int(input("#: "))
    if num > len(list):
      print("Choose a number from the list.")
      ask()
    else:
      val = list[num]
      print(f"You choose {val['name']}\n That currency code is {val['code']}")
      ask()
  except:
      print("That wasn't a number.")
      ask()

print("Hello! please choose select a country by number:")

for ind, key in enumerate(list):
  print(f"#{ind} {key['name']}")

ask()