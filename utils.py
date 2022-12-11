import requests
import pandas as pd
import json

def make_weather_st_url(lat, lon):
    '''
    This function takes in a latitue and longitude and creates 
    a url for finding weather stations near a specified location using the 
    MeteoStat API. The number of stations is set to 1. The URL is returned.
    '''

    meteo_stat_url = "https://meteostat.p.rapidapi.com/stations/nearby"
    meteo_stat_url += "?lat=" 
    meteo_stat_url += lat
    meteo_stat_url += "&lon="
    meteo_stat_url += lon
    meteo_stat_url += "&limit=1"

    return meteo_stat_url

def make_url_lst(df):
    '''
    This function takes in a dataframe, url for the 
    MeteoStat Weather API, and headers to request data.
    '''
    url_lst =[]
    # loop to generate urls
    for i in range(df["Start Longitude"].size):
        
        url_lst.append(make_weather_st_url(str(df.iloc[i]["Start Latitude"]), str(df.iloc[i]["Start Longitude"])))
        
   
    #print(url_lst)
    
    return url_lst


def make_station_lst(url_lst, headers):
    '''
    '''
    # loop through urls and request. add to lst
    station_lst = []

    #for url in url_lst:
        # get weather station data from meteostat API
    response = requests.get(url=url_lst[2], headers=headers)
        
        # load results into json format
    meteo_stat_json_obj = json.loads(response.text)
    
    station_lst.append(get_station_id(meteo_stat_json_obj))
    print(station_lst)



def get_station_id(weather_station_json):
    '''
    This function takes in a JSON result set of
    weather station data at a certain location found using
    the MeteoStat API. The weather station ID is extracted and returned.
    '''
    # grab the data list
    station_data_lst = weather_station_json["data"]
    # extract a dictionary from the list
    station_data_dict = station_data_lst[0]
    # grab the weather station id
    weather_station_id =  station_data_dict["id"]

    return weather_station_id