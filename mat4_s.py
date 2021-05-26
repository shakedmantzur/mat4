# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:42:54 2021

@author: Shaked
"""

import requests
dic_c=dict()
origin1="תל אביב"
api_k='__'
file=open("dests.txt", encoding='utf8')

for line in file:
    try:
        destination2=line.strip()
        url_1="https://maps.googleapis.com/maps/api/distancematrix/json?key=%s&origins=%s&destinations=%s"%(api_k,origin1,destination2)
        try:
            response=requests.get(url_1)
            if not response.status_code==200:
                print("HTTP error", response.status_code)
            else:
                try:
                    response_data=response.json()
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")
            
        d_f_telaviv=response_data['rows'][0]['elements'][0]['distance']['text']
    except:
        print("destination problem")
        continue
    #print(response_data)
    ##########################
    km=d_f_telaviv.find('km')
    if km<1:
        km_F=response_data['rows'][0]['elements'][0]['distance']['value']
        d_f_telaviv=str(km_F/1000)+" km"    
    ###########################
    
    time=response_data['rows'][0]['elements'][0]['duration']['value']
    time1=time
    #print(time)
    hours=int(time/(3600))
    #min=time%60
    mins=round((time-3600*hours)/60)
    #print(hours, mins)
    if hours>=1:
        time1=str(hours)+" hours "+str(mins)+" mins" 
    else:
        time1=str(mins)+" mins"
    
    ##########################################  
    url_2="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(destination2,api_k)
    try:
        response=requests.get(url_2)
        if not response.status_code==200:
            print("HTTP error", response.status_code)
        else:
            try:
                response_data2=response.json()
            except:
                print("Response not in valid JSON format")
    except:
        print("Something went wrong with requests.get")
    
    longitude=response_data2['results'][0]['geometry']['location']['lng']
    latitude=response_data2['results'][0]['geometry']['location']['lat']
        
    tp=('distance from Tel Aviv: '+d_f_telaviv, 'time: '+time1, 'longitude: '+str(longitude), 'latitude: '+str(latitude))
    dic_c[destination2]=tp
#print(dic_c)

for destination in dic_c:
    print("destination:", destination)
    print(dic_c[destination][0])
    print(dic_c[destination][1])
    print(dic_c[destination][2])
    print(dic_c[destination][3],"\n")


dic_distance=dict()
for destination in dic_c:
    d=dic_c[destination][0].split()
    distance=float(d[4].replace(",",""))
    dic_distance[destination]=distance
#print(dic_distance)    
lst=sorted([(distance,destination)for destination,distance in dic_distance.items() ] ,reverse=True)
print( "הערים הכי רחוקות")
for distance,destination in lst[:3]:
    print (destination,distance)