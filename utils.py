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
            
                lst.append([val["duration"]["startTimestamp"], val["duration"]["endTimestamp"], val["startLocation"]["latitudeE7"], val["startLocation"]["longitudeE7"], val["endLocation"]["latitudeE7"], val["endLocation"]["longitudeE7"], val["distance"], val["activityType"]])

    new_df = pd.DataFrame(lst, columns=["Start Timestamp", "End Timestamp", "Start Latitude", "Start Longitude", "End Latitude", "End Longitude", "Distance (m)", "Activity"])
    return new_df


            

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
