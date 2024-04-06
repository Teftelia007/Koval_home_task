from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time


url_gl = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-05-20&checkOut=2024-05-21&children=0&infants=0"
def get_soup(url): #Func to get the soup of the requested url
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(10)
    content = driver.page_source
    driver.implicitly_wait(10)
    soup = BeautifulSoup(content,'html.parser')
    return soup
soup_gl = get_soup(url_gl)  


def get_rooms_name(soup):    #Func to get the room__names
    rooms_names_list = []
    rooms_names = soup.findAll('h3',class_="css-19vc6se-Heading-Heading-Text e13es6xl3")
    for name in rooms_names:
        name_txt = name.get_text()
        rooms_names_list.append(name_txt)
    return rooms_names_list

def get_rooms_data_html(soup):    #Func to get the room__rate
    rooms_data = soup.findAll('div',class_="css-1o1uk43-Box e1yh5p92")
    rooms_data_list = []
    for room in rooms_data:
        #data_txt = room.get_text()
        rooms_data_list.append(room)
    return rooms_data_list
def n_guests(soup):
    guest_info = soup.findAll('span',class_="css-1j7tv8c-Text e1j4w3aq0")
    guest_list = []
    for guest in guest_info:
        guests_w_txt = guest.get_text()
        guest_wout_txt = re.search(r'\d{1}', guests_w_txt) 
        guest_list.append(guest_wout_txt.group())
        
    return guest_list  

#rate = {"Room_name":,"Rate_name","Number of Guests","Cancellation Policy","Price","Is_top_deal","Currency"}  

rates = []
def smt(rooms_data_list,rooms_names_list, n_guests):
    count = 0
    for room, data, guest in zip(rooms_names_list,rooms_data_list, n_guests): 
        room_name = room
        n_guest = guest
        currency = data.find('span',class_="css-17uh48g-Text e1j4w3aq0").get_text()
        
        if count == 0:
            price = data.find('span',class_="css-1bjudru e1c6pi2o1").get_text()
            top_deal = False
            if data.find('span',class_="css-1jr3e3z-Text-BadgeText e34cw120").get_text():
                top_deal = True
            rate_name = data.find('h3',class_="css-10yvquw-Heading-Heading-Text e13es6xl3").get_text()
            if "Non-refundable" in rate_name:
                cancellation = "Non-refundable"
            else:
                cancellation = "Free cancelaltion"
            rate = {"Room_name":room_name,"Rate_name":rate_name,"Number of Guests":n_guest,"Cancellation Policy":cancellation,"Price":price,"Is_top_deal":top_deal, "currency":currency}
            rates.append(rate)  
            count+=1   
        
            
        if count >0:
            price = data.findAll('span',class_="css-1bjudru e1c6pi2o1")
            top_deal = data.findAll('span',class_="css-1jr3e3z-Text-BadgeText e34cw120")
            rate_name = data.findAll('h3',class_="css-1negoe1-Heading-Heading-Text e13es6xl3")
            price = price[1:]
            top_deal = top_deal[1:]
            #print(len(price),len(top_deal),len(rate_name))
           # print(price,top_deal,rate_name)
            tp = False
            for pr,td,rn in zip(price,top_deal,rate_name):
                if td:
                    tp = True
                if "Non-refundable" in rn.get_text():
                    cancellation = "Non-refundable"
                else:
                    cancellation = "Free cancelaltion"
                rate = {"Room_name":room_name,"Rate_name":rn.get_text(),"Number of Guests":n_guest,"Cancellation Policy":cancellation,"Price":pr.get_text(),"Is_top_deal":tp, "currency":currency}
                rates.append(rate)  
            count = 0 

    
    return(rates)

#print(smt((get_rooms_data_html(soup_gl)),get_rooms_name(soup_gl)))
print(smt(get_rooms_data_html(soup_gl),get_rooms_name(soup_gl),n_guests(soup_gl)))