#Importing
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

#Assigning the value of the constant
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("/Users/apoorvelous/Downloads/chromedriver")
browser.get(START_URL)

time.sleep(11)

# function definition to identify specific part of the given webpage to extract data from 
def scrape():
    headers = ["Name", "Distance", "Mass", "Radius"]
    #Creating an empty list
    starData = []
    #Running a nested loop
    for i in range(0, 97):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ulTag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
                  liTags = ulTag.find_all("li")   
                  tempList = []     
                  for index, liTag in enumerate(liTags):
                      if index == 0:
                          tempList.append(liTag.find_all("a")[0].contents[0])
                      else:
                          try:
                              tempList.append(liTag.contents[0]) 
                          except:
                              tempList.append("")                             
                  starData.append(tempList) 
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(starData)  
        
#function call
scrape()   

newStarData = []                               

def scrapMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        tempList = [] 
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            tdTags = tr_tag.find_all("td")
            
            for tdTag in tdTags:
                try:
                    tempList.append(tdTag.find_all("div", attrs = {"class" : "value"})[0].contents[0])
                except:
                    tempList.append("") 
                    
        newStarData.append(tempList)               
    
    except:
        time.sleep(1)    
        scrapMoreData(hyperlink)
        
for index, data in enumerate(starData):
    scrapMoreData(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

# [start, stop]
print(newStarData[0:10])

final_star_data = []
        
for index, data in enumerate(starData):
    new_star_data_element = newStarData[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    # From the start to the 7th element.
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)   
    
with open("starData.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(starData)    