import requests
import pandas as pd
import json
import numpy as np

def get_start_end(df, start_date, end_date):
    '''
    '''

    for i in range(df.size):
        for key, val in df["timelineObjects"].iloc[i].items():
            # get only activity segments (not place visits)
            if(key == "activitySegment"):
                #print(val["duration"]["startTimestamp"])
                if start_date in val["duration"]["startTimestamp"]:
                    print(i)
                    #print(val["duration"]["startTimestamp"])
                elif end_date in val["duration"]["startTimestamp"]:
                    print(i)
                    #print(val["duration"]["startTimestamp"])


def make_dataframe(df, start, end):
    lst = []

    for i in range(start, end):
        for key, val in df["timelineObjects"].iloc[i].items():
            # get only activity segments (not place visits)
            if(key == "activitySegment"):
            
                lst.append([val["duration"]["startTimestamp"], val["duration"]["endTimestamp"], val["startLocation"]["latitudeE7"], val["startLocation"]["longitudeE7"], val["endLocation"]["latitudeE7"], val["endLocation"]["longitudeE7"], val["distance"], val["activityType"], val["confidence"]])

    new_df = pd.DataFrame(lst, columns=["Start Timestamp", "End Timestamp", "Start Latitude", "Start Longitude", "End Latitude", "End Longitude", "Distance", "Activity", "Confidence"])
    return new_df


def fix_lat_lon_all(df):

    fixed_start_lat_lst = []
    fixed_start_lon_lst = []
    fixed_end_lat_lst = []
    fixed_end_lat_lst = []
    fixed_start_lat = ""

    
    #start lat
    fixed_start_lat_lst = fix_lat_lon(df, "Start Latitude", 2)

    # for i in range(df["Start Latitude"].size):
    #     for j in range(2):
    #         fixed_start_lat += str(df["Start Latitude"].iloc[i])[j]
    #     fixed_start_lat += "."

    #     for k in range(2, len(str(df["Start Latitude"].iloc[i]))):
    #         fixed_start_lat += str(df["Start Latitude"].iloc[i])[k]

    #     fixed_start_lat_lst.append(fixed_start_lat) 
    #     fixed_start_lat = ""

    #start lon
    


    return fixed_start_lat_lst
            

def fix_lat_lon(df, col, decimal_place):

    fixed_lst = []
    fixed = ""

    for i in range(df[col].size):
        if(str(df[col].iloc[i])[0] != "-"):

            for j in range(decimal_place):
                fixed += str(df[col].iloc[i])[j]
            fixed += "."

            for k in range(decimal_place, len(str(df[col].iloc[i]))):
                fixed += str(df[col].iloc[i])[k]
        else:
            for j in range(decimal_place + 1):
                fixed += str(df[col].iloc[i])[j]
            fixed += "."

            for k in range(decimal_place + 1, len(str(df[col].iloc[i]))):
                fixed += str(df[col].iloc[i])[k]


        fixed_lst.append(fixed) 
        fixed = ""
    
    return fixed_lst


# def make_weather_st_url(lat, lon):
#     '''
#     This function takes in a latitue and longitude and creates 
#     a url for finding weather stations near a specified location using the 
#     MeteoStat API. The number of stations is set to 1. The URL is returned.
#     '''

#     meteo_stat_url = "https://meteostat.p.rapidapi.com/stations/nearby"
#     meteo_stat_url += "?lat=" 
#     meteo_stat_url += lat
#     meteo_stat_url += "&lon="
#     meteo_stat_url += lon
#     meteo_stat_url += "&limit=1"

#     return meteo_stat_url

# def make_url_lst(df):
#     '''
#     This function takes in a dataframe, url for the 
#     MeteoStat Weather API, and headers to request data.
#     '''
#     url_lst =[]
#     # loop to generate urls
#     for i in range(df["Start Longitude"].size):
        
#         url_lst.append(make_weather_st_url(str(df.iloc[i]["Start Latitude"]), str(df.iloc[i]["Start Longitude"])))
        
   
#     #print(url_lst)
    
#     return url_lst


# def make_station_lst(url_lst, headers):
#     '''
#     '''
#     # loop through urls and request. add to lst
#     station_lst = []

#     for url in url_lst:
#         # get weather station data from meteostat API
#         response = requests.get(url=url, headers=headers)
        
#         # load results into json format
#         meteo_stat_json_obj = json.loads(response.text)
    
#         station_lst.append(get_station_id(meteo_stat_json_obj))
#     #print(station_lst)
#     return station_lst



# def get_station_id(weather_station_json):
#     '''
#     This function takes in a JSON result set of
#     weather station data at a certain location found using
#     the MeteoStat API. The weather station ID is extracted and returned.
#     '''
#     # grab the data list

#     if"data" in weather_station_json.keys():
        
#         station_data_lst = weather_station_json["data"]

#         # extract a dictionary from the list
#         station_data_dict = station_data_lst[0]
#         # grab the weather station id
#         weather_station_id =  station_data_dict["id"]
#     else:
#         return np.NaN

#     return weather_station_id


def make_daily_weather_url(weather_station_id):
    '''
    This function takes in a weather station ID and generates
    a URL to get daily weather data from the specified station
    during a certain date range (in this case from 2/21/21 to 2/20/22) using the
    MeteoStat API. The URL is returned.
    '''

    daily_weather_url = 'https://meteostat.p.rapidapi.com/stations/daily?station='
    daily_weather_url += weather_station_id
    daily_weather_url += "&start=2022-01-21&end=2022-05-05"
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

def get_time_elapsed(df):
    '''
    '''
    start_time_lst = []
    end_time_lst = []

    for item in df["Start Timestamp"]:
        start_time_lst.append(item.time()) 

    for item in df["End Timestamp"]:
        end_time_lst.append(item.time())
    end_time_lst

    time_lst = []
    for i in range(len(start_time_lst)):
        
        time_lst.append([end_time_lst[i].hour - start_time_lst[i].hour, end_time_lst[i].minute - start_time_lst[i].minute, end_time_lst[i].second - start_time_lst[i].second])

    time_lst_min = []

    #calculate time elapsed in minutes
    for i in range(len(time_lst)):
        time_lst_min.append(time_lst[i][0]*60 + time_lst[i][1] + time_lst[i][2]/60)

    time_lst_min
    
    return time_lst_min
