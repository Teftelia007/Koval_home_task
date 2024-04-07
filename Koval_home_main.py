from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import re
import time

def get_soup(url): #Func to get the full data of the requested url, returns soup of the page
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(10)
    Button = driver.find_elements(By.CSS_SELECTOR,".css-v84xw-NakedButton.eml2css7") #clicking on all rates to expand them 
    for btn in Button:
        btn.click()
        
    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    return soup

def get_rooms_name(soup):    #Func to get the room_names, returns list with room_names
    rooms_names_list = []
    rooms_names = soup.findAll('h3',class_="css-19vc6se-Heading-Heading-Text e13es6xl3")
    for name in rooms_names:
        name_txt = name.get_text()
        rooms_names_list.append(name_txt)
    return rooms_names_list

def get_rooms_data_html(soup):    #Func to get the all ROOMS data, returns list with info for each ROOM
    rooms_data = soup.findAll('div',class_="css-1o1uk43-Box e1yh5p92")
    rooms_data_list = []
    for room in rooms_data:
        #data_txt = room.get_text()
        rooms_data_list.append(room)
    return rooms_data_list

def n_guests(soup): #Func to get the OCCUPANCY of each ROOM, return list with occupancies for each ROOM
    guest_info = soup.findAll('span',class_="css-1j7tv8c-Text e1j4w3aq0")
    guest_list = []
    for guest in guest_info:
        guests_w_txt = guest.get_text()
        guest_wout_txt = re.search(r'\d{1}', guests_w_txt) 
        guest_list.append(guest_wout_txt.group())
        
    return guest_list  


def build_data (rooms_data_list,rooms_names_list, n_guests): #Func for collection all RATES for each room and creating JSON, return JSON with all requested data
    for room, data, guest in zip(rooms_names_list,rooms_data_list, n_guests): 
        room_name = room
        n_guest = guest
        currency = data.find('span',class_=  'css-17uh48g-Text e1j4w3aq0').get_text()
        for rate in data:
            single_rate = rate.findAll('div', attrs={'data-testid': 'offer-card-expanded'})
            for rate in single_rate:
                price = rate.find('span',class_= "css-1bjudru e1c6pi2o1").get_text()
                top_deals = rate.find('span',class_= "css-1jr3e3z-Text-BadgeText e34cw120")
                rate_name = rate.find('h3',class_= "css-10yvquw-Heading-Heading-Text e13es6xl3").get_text()
                cancellation_pollicy = rate.find('span', attrs={"data-testid": "cancellation-policy-message"}).get_text()
                if cancellation_pollicy.upper() == "FREE CANCELLATION":
                    cancellation_pollicy_before_date = rate.find('span', attrs={"data-testid": "free-cancellation-before-date"}).get_text() 
                    cancellation_pollicy = cancellation_pollicy + " " + cancellation_pollicy_before_date
                if top_deals:
                    top_deal = True
                else:
                    top_deal = False
                    
                rate = {"Room_name":room_name,"Rate_name":rate_name,"Number of Guests":n_guest,"Cancellation Policy":cancellation_pollicy,"Price":price,"Is_top_deal":top_deal, "Сurrency":currency}
                rates.append(rate) 

    return rates

for i in range(30):
    rates = [] #list with rates(JSON)          
    url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-05-20&checkOut=2024-05-21&children=0&infants=0"
    soup_gl = get_soup(url)        
    (build_data(get_rooms_data_html(soup_gl),get_rooms_name(soup_gl),n_guests(soup_gl)))
    print(rates)

    
    
""" use this code for several ulrs - combination of the ci/co+hotels_id...Put them in the list urls, comment 76-80 string

urls = ["https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-05-20&checkOut=2024-05-21&children=0&infants=0", "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-08-20&checkOut=2024-08-21&children=0&infants=0"] # list with urls
Items = []  #list with lists :)  where we will store the lists with JSONs for each combination of the ci/co
for ur in urls: #cycle for scanning all nessesary urls
    print(ur)
    rates = [] #list with rates(JSON)
    soup_gl = get_soup(ur)  
    item = (build_data(get_rooms_data_html(soup_gl),get_rooms_name(soup_gl),n_guests(soup_gl)))
    Items.append(item)

print(Items)"""