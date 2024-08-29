import requests
import os

while True: 
  print("Welcome to IsItDown.py!")
  urls = input('Please write a URL or URLs you want to check. (seperated by comma)\n')
  
  url = urls.split(",")
  for link in url:
    link = link.strip()
    #print("link:",link)
    if not link.endswith('.com'):
      print(f'{link} is not a valid URL.')
      break
    if link.startswith('http'):
      link_ = link
    else:
      link_ = 'https://'+link
    
    try:
      response = requests.get(link_.lower())
      #print(response)
      rs_code = response.status_code
      #print(response.raise_for_status())
      if int(rs_code) ==200 :
        print(f'{link_.lower()} is up!')
      #else :
      #  print(f"{link_.lower()} is down!")
        
    except :
      print(f"{link_.lower()} is down!")
      
  restart = input('Do you want to start over? y/n ')
  if restart == 'y':
    print("you type y")
    os.system('clear')
    pass
  else: 
    if restart == 'n':
      print("K.bye!")
      break
    else: pass #how can i go back to restart..?!
    
