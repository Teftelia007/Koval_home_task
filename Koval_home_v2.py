import requests
import pandas as pd
import re

#URLs for getting a responce
urls = ['https://www.qantas.com/hotels/api/ui/properties/18442/availability?checkIn=2024-05-01&checkOut=2024-05-03&adults=2&children=0&infants=0&payWith=cash']

#headers for request response
headers = {                                                                     
'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
'DNT': '1' ,
'sec-ch-ua-mobile': '?0' ,
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' ,
'qh-meta': '{"qhUserId":"f6bfc6d6-b229-4478-85f9-ef44bf996eae"}' ,
'Accept': "application/json, text/plain, */*" ,
'Referer': "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-04-16&checkOut=2024-04-17&children=0&infants=0" ,
'sec-ch-ua-platform': "Windows" }

def geting_responce(url):           
    #Function for getting the response with rooms data from site                                        
    response = requests.get(url, headers=headers)
    
    #Converting response into JSON(dictionary)
    response_JSON = response.json()   
    
    #Managing the not avaiable hotels p1.
    if response_JSON.get('roomTypes') == []:
        return False
                                 
    full_room_data = response_JSON.get("roomTypes")
    
    #Func returns data in JSON format
    return full_room_data                                                   

#Function for collecting and assembling all requested fields, response list with offers as input
def rates_building(response):   
    #List where rates will be collected 
    rates = []  
    
    #Managing the not avaiable hotels p2.        
    if not response:
        return print("Not avaiable for select date")
    
    #Code below collects each requested field
    for single_room_data in response:                                       
        room_name = single_room_data.get("name")
        
        #Getting number of MAX guests for room(OCCUPANCY)
        number_of_guests = single_room_data.get("maxOccupantCount")         
        
        full_rates_data = single_room_data.get("offers")
        for rate in full_rates_data:
            rate_name = rate.get("description")
            
            charges = rate.get("charges")
            total_price_currency = charges.get("total")
            total_price = float(total_price_currency.get("amount"))
            currency = total_price_currency.get("currency")
            
            cancellation_policy_full = rate.get("cancellationPolicy")
            cancellation_policy_decription = cancellation_policy_full.get("description")
            
            #Regular expresion for extracting only a main part of the cancellation policy
            cancellation_policy = re.search(r'Cancellations or changes made.*penalty',cancellation_policy_decription) 
            cancellation_policy = cancellation_policy.group()
            
            #Condition for non-refundable cancellation
            if 'NON-REFUNDABLE' in rate_name.upper():
                cancellation_policy = 'Non - refundable'
            
            promotions = rate.get("promotion")
            
            #Condition for case when any promotion is absent
            if promotions:
                promotion_description = promotions.get("name")
                
                #If condition for checking is our rate is TOP DEAl
                if "TOP DEAL" in promotion_description.upper():                                    
                    is_top_deal = True
                else:
                    is_top_deal = False
            else:
                is_top_deal = False
                
            #Colecting all the data in one JSON    
            single_rooms_rate = rate = {"Room_name":room_name,"Rate_name":rate_name,"Number of Guests":number_of_guests, "Cancellation Policy":cancellation_policy,"Price":total_price,"Is_top_deal":is_top_deal, "Сurrency":currency} 
            
            #Appending JSON with data to list
            rates.append(single_rooms_rate)  
            
    #Func returning list with JSON room's values                                     
    return rates                                                           

#Here will be printed list for each url from the list URLS
for i in urls:
    print(f"{rates_building(geting_responce(i))}\n")
