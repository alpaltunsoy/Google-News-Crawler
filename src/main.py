import requests
from bs4 import BeautifulSoup 

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

def finding_news(categories_dictionary,newsHeaders,url_lists,publisher_list,time_lists):

        
        for i  in range(len(categories_dictionary)):
                
                url = "https://news.google.com"+ categories_dictionary[i]["Link"][1:]

                try:
                        webRequestNews = requests.get(url) # taking websites with requests
                except:
                        print("There are some problem on news side and closing program ")
                        exit()

                
                if(webRequestNews.status_code == 200):

                        print("Finding news on " + categories_dictionary[i]["Başlık"]) #status printing
                        newsSoup = BeautifulSoup(webRequestNews.text, "lxml") #creating soup object
                        
                        #finding news headers
                        all_news_raw = newsSoup.find_all("a", class_=lambda x: x and (x.startswith("gPFEn") or x.startswith("JtKRv")))
                        for headers in all_news_raw:
                                newsHeaders.append(headers.contents[0].strip())
                                url_lists.append("news.google.com"+headers.get("href")[1:])

                        #finding publishers
                        all_news_raw = newsSoup.find_all("div", class_="vr1PYe")
                        for publisher in all_news_raw:
                                publisher_list.append(publisher.contents[0].strip())
                                
                        all_news_raw = newsSoup.find_all("time", class_="hvbAAd")
                        for times in all_news_raw:
                                time_lists.append(times.get("datetime"))

def main():
    
        categories_dictionary = [] #defining list for main_categories of news
        newsHeaders=[]
        url_lists = []
        publisher_list = []
        time_lists = []
        finding_categories(categories_dictionary) #adding categories to our list 
        print("\n")
        finding_news(categories_dictionary, newsHeaders,url_lists,publisher_list, time_lists)
        
        print("Bulunan yayımcı sayısı : ",len(publisher_list))
        print("Bulunan başlık sayısı : ",len(newsHeaders))
        print("Bulunan url sayısı : ", len(url_lists))
        print("Bulunan zaman sayısı : ", len(time_lists))

        with open("haberler.txt","w", encoding="utf-8") as file:
                for x in range(len(url_lists)):
                        file.write(str(x)+","+newsHeaders[x]+","+publisher_list[x]+","+time_lists[x]+","+url_lists[x]+"\n")
if __name__ == "__main__":
    main()