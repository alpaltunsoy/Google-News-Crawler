import requests
from bs4 import BeautifulSoup
import csv 
import os
import datetime
import schedule
import time
import pandas as pd

def csv_creator_category(headers, kaynak,category, time, url):

        csv_list = [["ID","Headline", "Source","Category", "Time", "URL"]]
        for i in range(len(headers)):
                csv_list.append([str(i+1),headers[i], kaynak[i],category, time[i], url[i]])
    
        with open( os.path.abspath(".")+"\docs\\"+zaman +f"\\All_news_list_{category}.csv"        , mode="w", newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerows(csv_list)

def csv_creator(headers, kaynak,category, time, url):
        csv_list = [["ID","Headline", "Source","Category", "Time", "URL"]]
        for i in range(len(headers)):
                csv_list.append([str(i+1),headers[i], kaynak[i],category[i], time[i], url[i]])
    
        with open(os.path.abspath(".")+"\docs\\"+zaman +f"\\All_news_list_.csv", mode="w", newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerows(csv_list)

def finding_categories(categories_dictionary):
        
                print("Connecting to Google news...")
                try:
                        webRequest = requests.get("https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr") # taking HTML of google news 
                except:
                        print("Program is closing. Link is not correct")
                        exit()

                #checking the status
                if(webRequest.status_code == 200):

                        print("Successfully connected to the Google News")
                        webParsing = BeautifulSoup(webRequest.text, "lxml")
        
                        #lets take every categories
                        all_categories = webParsing.find_all("a", class_="brSCsc")

                        categories_exclude = [
                                "Sizin için",
                                "Takip edilenler",
                                "Ana Sayfa",
                                ]
                        
                        #adding categories to the list
                        for categories in all_categories:
                                if categories.get("aria-label") not in categories_exclude:
                                        categories_dictionary.append({"Başlık":categories.get('aria-label'),"Link":categories.get("href")})
                else:
                        print("Failed to connect google news Try again!!!")

def finding_news(categories_dictionary):

        #defining variables 
        newsHeaders=[] #store all news headers       
        url_lists = [] #store all url lists
        publisher_list = [] #store all publisher for every news
        time_lists = [] #store all time details for every news 
        category_counter = [] #store all categories for every news 

        for i  in range(len(categories_dictionary)):
                url = "https://news.google.com"+ categories_dictionary[i]["Link"][1:] #make an url for news page

                try:
                        webRequestNews = requests.get(url) # taking websites with requests
                except:
                        print("There are some problem on news side and closing program ")
                        exit()

                if(webRequestNews.status_code == 200):
                        #defining temp variables which will be deleted every loop
                        newsHeaders_temp = []
                        publisher_list_temp = []
                        time_lists_temp=[]
                        url_lists_temp=[]

                        print("Finding news on " + categories_dictionary[i]["Başlık"]) #status printing
                        newsSoup = BeautifulSoup(webRequestNews.text, "lxml") #creating soup object
                        
                        #finding news headers and urls
                        all_news_raw = newsSoup.find_all("a", class_=lambda x: x and (x.startswith("gPFEn") or x.startswith("JtKRv"))) #there are two options for taking headers
                        for headers in all_news_raw:
                                newsHeaders.append(headers.contents[0].strip())
                                url_lists.append("news.google.com"+headers.get("href")[1:]) #taking urls too 
                                newsHeaders_temp.append(headers.contents[0].strip())
                                url_lists_temp.append("news.google.com"+headers.get("href")[1:])

                        #finding publishers
                        all_news_raw = newsSoup.find_all("div", class_="vr1PYe")
                        for publisher in all_news_raw:
                                publisher_list.append(publisher.contents[0].strip())
                                publisher_list_temp.append(publisher.contents[0].strip())
                        
                        #publishing time
                        all_news_raw = newsSoup.find_all("time", class_="hvbAAd")
                        for times in all_news_raw:
                                time_lists.append(times.get("datetime"))
                                time_lists_temp.append(times.get("datetime"))
                                category_counter.append(categories_dictionary[i]["Başlık"])

                        
                        #creating csv and change file format
                        csv_creator_category(newsHeaders_temp,publisher_list_temp,categories_dictionary[i]["Başlık"],time_lists_temp,url_lists_temp)
                        csv_to_json(categories_dictionary[i]["Başlık"])

        csv_creator(newsHeaders,publisher_list,category_counter,time_lists,url_lists)
        csv_to_json("")
        
def csv_to_json(category):
        converter = pd.read_csv( os.path.abspath(".")+"\docs\\"+zaman +f"\\All_news_list_{category}.csv")
        converter.to_json(os.path.abspath(".")+"\docs\\"+zaman +f"\\All_news_list_{category}.json")

def create_folder():
        
        #creating docs folder
        if  not (os.path.exists(os.path.abspath(".")+"\docs")):
                os.makedirs(os.path.abspath(".\docs"))
                print("docs folder is created")
        else:
                print("\ndocs folder is already created")

        #creating inside of the docs folder
        if  not (os.path.exists(os.path.abspath(".")+"\docs\\"+zaman)):
                print("\nNew Folder is created as " + zaman+"\n")
                os.makedirs(os.path.abspath(".")+"\docs\\"+zaman)
               
def start():
        print("\nProgram is started")
        #defining global variables for date information to use everywhere
        global today
        today = datetime.datetime.now()

        #defining zaman for using folder operations
        global zaman
        zaman = str(today.day) +"-" + str(today.month) +"-"+  str(today.year) + "  "+ str(today.hour) +" "+ str(today.minute)+" " +str(today.second)
        
        #creating folders for storing datas
        create_folder()

        #creating variables for methods 
        categories_dictionary = [] #defining list for all categories in google news 
        
        finding_categories(categories_dictionary) #adding all categories in google news to list variable
        finding_news(categories_dictionary) #sending categories to method for searching all news 
        return

def main():
        
        schedule.every().hour.at(":00").do(start)
        while True:
               schedule.run_pending()
               time.sleep(1)
                
        
if __name__ == "__main__":
    main()