##############################################
# Programmer : Carolyn Bozin
# Class      : CPSC222, Fall 2022
# Assignment : quantified self
# Date       : 12/13/22
# Description: file to get daily weather data for Madrid
#              using the Meteostat API   
##############################################

import config
import requests
import json
import pandas as pd

def make_daily_weather_url(weather_station_id):
    '''
    This function takes in a weather station ID and generates
    a URL to get daily weather data from the specified station
    during a certain date range (in this case from 2/21/21 to 2/20/22) using the
    MeteoStat API. The URL is returned.
    '''

    daily_weather_url = 'https://meteostat.p.rapidapi.com/stations/daily?station='
    daily_weather_url += weather_station_id
    daily_weather_url += "&start=2021-02-21&end=2022-02-20"
    daily_weather_url += "&units=imperial"

    return daily_weather_url


def load_2d_list(daily_weather_json):
    '''
    This function takes a daily weather JSON object
    recieved using the MeteoStat API and loads the daily weather 
    data into a 2D list (each day is a list). The list is returned.
    '''
    # get the data portion as a list
    daily_weather_data_lst = daily_weather_json["data"]

    # initialize 2D list to load values into
    daily_weather_2D_lst = []

    #load the values of each dictionary
    # (one dictionary per day) into the 2D list
    for dict in daily_weather_data_lst:
        
        daily_weather_2D_lst.append(dict.values())
    

    return daily_weather_2D_lst


def get_weather_json(headers):
    '''
    This function gets a json object
    of daily weather from madrid.
    '''
    daily_weather_url = make_daily_weather_url("08222")
    # request daily weather data
    response = requests.get(url=daily_weather_url, headers=headers)
    #put weather data int json format
    daily_weather_json = json.loads(response.text)

    return daily_weather_json



def get_weather_df(daily_weather_json):
    '''
    This function sends daily weather data
    for Madrid to a csv file.
    '''
    # get 2d list of daily weather data from json file
    daily_weather_2D_lst = load_2d_list(daily_weather_json)
# make cleaner headers
    daily_weather_headers = ["Date", "Avg Temp", "Min Temp", "Max Temp", "Precip.", "Snow", "Wind Dir.", "Wind Speed", "Peak Wind Gust", "Pressure", "Total Sun"]
# make dataframe from headers and 2d list of data
    weather_df = pd.DataFrame(daily_weather_2D_lst, columns=daily_weather_headers)
    print(weather_df)
    weather_df.to_csv("daily_weather_madrid.csv")



def main():
    my_ms_key = config.key["x-rapidapi-key"]

    headers = { 'x-rapidapi-host': 'meteostat.p.rapidapi.com',
                        "x-rapidapi-key" : my_ms_key }

    # USED METEOSTAT UI TO GET ID (lat =40.4168 lon=3.7038, and limit=1)
    # make url to get daily weather
    weather_json = get_weather_json(headers)
    #send data to csv
    get_weather_df(weather_json)


main()


