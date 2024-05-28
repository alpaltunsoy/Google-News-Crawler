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

        
        
        


def finding_news(categories_dictionary,newsHeaders):

        
        #for i  in range(len(categories_dictionary)):
                
                url = "https://news.google.com"+ categories_dictionary[0]["Link"][1:]

                try:
                        webRequestNews = requests.get(url) # taking websites with requests
                except:
                        print("There are some problem on news side and closing program ")
                        exit()

                #haber başlığı çekme
                if(webRequestNews.status_code == 200):
                        print("Finding news on " + categories_dictionary[0]["Başlık"])
                        newsParsing = BeautifulSoup(webRequestNews.text, "lxml") 
                        all_news_raw = newsParsing.find_all("a", class_="gPFEn")
                       
                
                        for headers in all_news_raw:
                                newsHeaders.append(headers.contents[0].strip())
                
                       
                
      



def main():
    

        categories_dictionary = [] #defining list for main_categories of news
        newsHeaders=[]
        finding_categories(categories_dictionary) #adding categories to our list 
        print("\n")
        finding_news(categories_dictionary, newsHeaders)
        print(newsHeaders)
        
        

    
if __name__ == "__main__":
    main()