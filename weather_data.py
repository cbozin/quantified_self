##############################################
# Programmer : Carolyn Bozin
# Class      : CPSC222, Fall 2022
# Assignment : 
# Date       : 
# Description:      
##############################################

import utils
import config
import requests
import json
import pandas as pd

def get_weather_json(headers):
    daily_weather_url = utils.make_daily_weather_url("08222")
    # request daily weather data
    response = requests.get(url=daily_weather_url, headers=headers)
    #put weather data int json format
    daily_weather_json = json.loads(response.text)

    return daily_weather_json



def get_weather_df(daily_weather_json):
    '''
    '''
    # get 2d list of daily weather data from json file
    daily_weather_2D_lst = utils.load_2d_list(daily_weather_json)
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
    get_weather_df(weather_json)


main()


    # #make url for madrid
# # url = utils.make_weather_st_url("40.4168", "-3.7038")

# # response = requests.get(url=url, headers=headers)

# # # load results into json format
# # meteo_stat_json_obj = json.loads(response.text)
# # # get the station id
# # weather_station_id = utils.get_station_id(meteo_stat_json_obj)
# # print(weather_station_id)
