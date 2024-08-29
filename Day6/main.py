import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

url = "https://www.iban.com/currency-codes"
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')
table = soup.find("table", {"class":"table"})
tbody = table.find("tbody").find_all("tr")

list=[]
code=[None,None]
cur=[None]
amount_ = [None]
for tr in tbody:
  infos = tr.find_all("td")
  country = (infos[0].text).capitalize()
  co = infos[2].string
  if "No universal currency" not in infos[1]:
    a = {"name":country, "code":co}
    list.append(a)  

def curruncy_change():
  try:
    amt = int(input("Type a number: "))
    if amt:
      amount_[0]= amt
  except:
      print("That wasn't a number.")

def ask_another():
  try:
    second = int(input("Country B#: "))
    if second > len(list):
      print("Choose a number from the list.") 
    else:
      val = list[second]
      print(f"{val['name']}\n")
      code[1]=val['code']
  except:
      print("That wasn't a number.")

def ask():
  try:
    first = int(input("Country A#: "))
    if first > len(list):
      print("Choose a number from the list.")   
    else:
      first_val = list[first]
      print(f"{first_val['name']}\n")
      #h = first_val['code'].string
      code[0]=first_val['code']
  except:
      print("That wasn't a number.")

for ind, key in enumerate(list):
  print(f"#{ind} {key['name']}")

print("\nWhere are you from? Choose a country by number.\n")
ask()
print("Now choose another country.\n")
ask_another()
print(f"How many {code[0]} do you want to conver to {code[1]}?")  
curruncy_change()

code[0] = code[0].lower()
code[1] = code[1].lower()

#cur_url = "https://transferwise.com/gb/currency-converter/usd-to-eur-rate?amount=100"
cur_url = f"https://transferwise.com/gb/currency-converter/{code[0]}-to-{code[1]}-rate?amount={amount_[0]}"
request_cur = requests.get(cur_url)
soup_cur = BeautifulSoup(request_cur.text, 'html.parser')
cur_info = soup_cur.find("span",{"class":"text-success"}).string
cur_info = float(cur_info)
#print (cur_info, type(cur_info))
#print(amount_[0], type(amount_[0]))
total = int(amount_[0]*cur_info)
#print("total:", total)
change =format_currency(total, code[1].upper(), locale="ko_KR")
print(f"{code[0].upper()} {amount_[0]} is {change}")

