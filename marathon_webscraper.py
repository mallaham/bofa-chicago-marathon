import pandas as pd
from requests import get
from bs4 import BeautifulSoup

year=[str(i) for i in range(1996,2015)]


# In[7]:

'''
Multi-page Webscraper
'''
plc_overall=[]
plc_gender=[]
plc_division=[]
name=[] #split it by FName and LName
city_state=[] #split it
bib=[]
division=[]
age=[]
half_t=[]
finish_t=[]
participant=[]
year_df = [] #df to track years.

from IPython.core.display import clear_output
from time import sleep
from random import randint
from time import time
from warnings import warn

#tracking requests
start_time = time()
requests = 0

#looping year
for y in year:
    #looping page
    url= 'http://chicago-history.r.mikatiming.de/'+y+'/?page=1&event=MAR_999999107FA3090000000079&event_main_group='+y+'&lang=EN_CAP&pid=search&search_sort=name'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    #getting the max number of pages for each year
    max_page = html_soup.find('div',class_='pages')
    max_page= max([int(index.text) for index in max_page.find_all('a',class_='')])
    pages = [str(i) for i in range(1,max_page+1)]

    for p in pages:
        #making a request
        url= 'http://chicago-history.r.mikatiming.de/'+y+'/?page='+p+'&event=MAR_999999107FA3090000000079&event_main_group='+y+'&lang=EN_CAP&pid=search&search_sort=name'
        response = get(url)

        #pausing the script
        sleep(randint(2,5))
        
        #tracking requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        #clear_output(wait = True)
              
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
       
        #html parser
        html_soup = BeautifulSoup(response.text, 'html.parser')

        results_container = html_soup.find('table', class_='list-table')
        results_container = results_container.find_all('tr') #saves all tr's in a list
        for r in results_container:
            for j in r.find_all('td'):
                #print (type(j.text))
                participant.append(j.text)
            if(participant!=[]):
            	year_df.append(participant[0])
            	#type of race is at index 1 (i.e, Marathon)
                plc_overall.append(participant[2])
                plc_gender.append(participant[3])
                plc_division.append(participant[4])
                name.append(participant[5])
                city_state.append(participant[6])
                bib.append(participant[7])
                division.append(participant[8])
                age.append(participant[9])
                half_t.append(participant[10])
                finish_t.append(participant[11])
            participant=[]
marathon_results=pd.DataFrame({'Place_Overall': plc_overall,
                      'Place_Gender': plc_gender,
                      'Place_Division': plc_division,
                      'Name': name,
                      'City_State': city_state,
                      'BIB':bib,
                      'Division':division,
                      'Age':age,
                      'Half':half_t,
                      'Finish':finish_t,
                      'Year':year_df})


marathon_results.to_csv('Marathon_data.csv',index=False,encoding='utf-8')
print("Running Time: ",time()-start_time)
