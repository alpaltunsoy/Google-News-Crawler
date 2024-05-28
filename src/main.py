import requests
from bs4 import BeautifulSoup 



#Downloading website
webRequest = requests.get("https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr") # taking websites with requests
webRequest.raise_for_status() #if conenction is failed it will raise an error
webParsing = BeautifulSoup(webRequest.text, "lxml")
    
print("Connection is successfull")
#lets take every topics
all_topics = webParsing.find_all("a", class_="brSCsc")


for topics in all_topics:
        if (topics.get("aria-label")  != "Sizin için"   ) and (topics.get("aria-label")  != "Takip Edilenler"   ) and (topics.get("aria-label")  != "Ana Sayfa"   )  and (topics.get("aria-label")  != "Takip edilenler"   ):
                print(topics.get("aria-label"), "\n")
                print(topics.get("href"), "\n")
       