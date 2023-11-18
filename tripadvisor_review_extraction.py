import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)
from datetime import datetime




def get_ratings():
        
    data_collection=[]
    
    for page in range(0,63):
        
        url = "https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&wrap=true&skipLocation=true&page={}&sort=alphabetical".format(page)
        
        payload = {}
        headers = {
          'authority': 'www.tripadvisor.com',
          'accept': '*/*',
          'accept-language': 'en-US,en;q=0.9',
           'referer': 'https://www.tripadvisor.com/Airlines',
          'sec-ch-device-memory': '8',
          'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
          'sec-ch-ua-arch': '"x86"',
          'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.124", "Chromium";v="119.0.6045.124", "Not?A_Brand";v="24.0.0.0"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-model': '""',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
          'x-puid': '69148f99-34f5-46cd-8216-ad1081fb5a38',
          'x-requested-with': 'XMLHttpRequest'
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content=soup.find('div',attrs={"class":"mainColumnContent"})
        
        cards=soup.find_all('div',attrs={"class":"prw_rup prw_airlines_airline_lander_card"})
        
        for card in cards:
            data_dict={}
            try:
             data_dict['AirLine Logo']=card.find('img',attrs={"class":"logoImage"})['src']
            except: data_dict['AirLine Logo']=''
            
            try:
             data_dict['AirLine Name']=card.find('div',attrs={"class":"airlineName"}).text
            except: data_dict['AirLine Name']=''
            
            try:  data_dict['Reviews Count']=card.find('div',attrs={"class":"airlineReviews"}).text
            except:  data_dict['Reviews Count']=''
            
            try: data_dict['Ratings']=card.find('span',attrs={"style":"font-size:14px;"})['alt']
            except:  data_dict['Ratings']=''
            
            
            
          
            
            try:
                reviews=card.find('div',attrs={"class":"reviews"}).find_all('p')
                data_dict['reviews']=[]
                for review in reviews:
                  data_dict['reviews'].append(review.text)
            except:
                data_dict['reviews']=[]
                
                
            data_collection.append(data_dict)
            print(len(data_collection))
   
    return data_collection


@app.route('/trip_advisor_ratings', methods=['GET'])
def ratings():
    
    json_data=get_ratings()
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M')

    return {"status":"success","extracted_at":formatted_datetime,"data":json_data }



if __name__ == '__main__':
    app.run()





