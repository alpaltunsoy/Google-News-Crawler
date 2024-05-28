import requests
from bs4 import BeautifulSoup 



#Downloading website
webRequest = requests.get("https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr") # taking websites with requests
print("Connecting to Google news...")
webRequest.raise_for_status() #if conenction is failed it will raise an error
webParsing = BeautifulSoup(webRequest.text, "lxml")
    
print("Connection is successfull")
#lets take every topics
all_topics = webParsing.find_all("a", class_="brSCsc")

topics_exclude = ["Sizin için",
                  "Takip edilenler",
                  "Ana Sayfa",
                  ]


for topics in all_topics:
        if topics.get("aria-label") not in topics_exclude:
                print(topics.get("aria-label"), "\n")
                print(topics.get("href"), "\n")


        
       