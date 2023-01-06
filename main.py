from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import requests
import lxml

class RealEstate:
    def __init__(self):
        self.property={}


    #this function scraps data from the website
    def get_data(self):
        link='https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.887824249177555%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.662588109642094%2C%22west%22%3A-122.63417331103516%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D'
        headers = {
            "User-Agent": "your headers info",
            "Accept-Language": "your headers info"
        }

        response = requests.get(url=link, headers=headers)
        response.encoding='utf-8'

        soup=BeautifulSoup(response.text,'lxml')
        addresses=soup.find_all(name='a',class_='StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 lpqUkW property-card-link')
        links=soup.find_all(name='a',class_='StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 lpqUkW property-card-link',href=True)
        prices=soup.find_all(name='div',class_='StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 wgiFT')
        #storing address and price info in the dictionary
        for i in range(len(addresses)):
            self.property[i]={
                'address':addresses[i].text,
                'price': prices[i].text,
                'link':  'https://www.zillow.com'+links[i]['href']
            }

        #storing data in a csv file...
        data=pd.DataFrame.from_dict(self.property,orient='index')
        data.to_csv('projects\\Web Scrapping\\Data Entry Job Automation\\results.csv')


    #this function will input those data into the spreadsheet and submit it
    def filling_form(self):
        driver_path='C:\\Python310\\chrome_driver\\chromedriver.exe'
        driver=webdriver.Chrome(executable_path=driver_path)

        for i in range(len(self.property)):
            driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdV48WreFqLABMgqn9rbHl8ygoxBCsV7WGru0i_DaU4qHjWQA/viewform?usp=sf_link')
            time.sleep(3)
            #getting hold of address input
            address=driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address.send_keys(self.property[i]['address'])
            #getting hold of price input
            price=driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price.send_keys(self.property[i]['price'])
            #getting hold of link input
            link=driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
            link.send_keys(self.property[i]['link'])
            #getting hold of submit button
            submit=driver.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit.click()
        


def main():
    real=RealEstate()
    real.get_data()
    # real.filling_form()

if __name__ == '__main__':
    main()

