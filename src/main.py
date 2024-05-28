import requests
from bs4 import BeautifulSoup 



def finding_categories(categories_dictionary):

        #Downloading website
        webRequest = requests.get("https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr") # taking websites with requests
        print("Connecting to Google news...")
        webRequest.raise_for_status() #if conenction is failed it will raise an error
        webParsing = BeautifulSoup(webRequest.text, "lxml")
        print("Connection is successfull")

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

def main():
    
    
    categories_dictionary = [] #defining list for main_categories of news
    finding_categories(categories_dictionary) #adding categories to our list 
    



if __name__ == "__main__":
    main()
        