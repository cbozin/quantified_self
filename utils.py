##############################################
# Programmer : Carolyn Bozin
# Class      : CPSC222, Fall 2022
# Assignment : quantified self
# Date       :  12/13/22
# Description:  utility functions   
##############################################

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


def load_data():
    '''
    This function creates a
    dataframe using my Semantic Location data from
    January-August of 2022. It returns the dataframe
    '''
    jan_aug_df = pd.DataFrame()

    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST"]

    # concatenate data from all months
    for item in months:
        jan_aug_df = pd.concat([jan_aug_df, pd.read_json("Semantic Location History/2022/2022_" + item + ".json")])

    return jan_aug_df

def get_start_end(df, start_date, end_date):
    '''
    This function takes a dataframe and 
    start and end dates. It then parses through
    my Google Maps timelineObject dataframe and prints
    indeces of instances from the desired dates.
    '''
    #iterate through df
    for i in range(df.size):
        for key, val in df["timelineObjects"].iloc[i].items():
            # get only activity segments (not place visits)
            if(key == "activitySegment"):
                #print indeces of instances w/start or end date 
                if start_date in val["duration"]["startTimestamp"]:
                    print(i)
                elif end_date in val["duration"]["startTimestamp"]:
                    print(i)



def make_dataframe(df, start, end):
    '''
    This function takes in a dataframe plus
    start and end indices and makes a new 
    dataframe with just the instances in the given
    range. The new dataframe is returned.
    '''
    lst = []

    #parse through df in given range
    for i in range(start, end):
        for key, val in df["timelineObjects"].iloc[i].items():
            # get only activity segments (not place visits)
            if(key == "activitySegment"):
                
                #append start/end timestamps, lat/lon, distance, and activity type to list
                lst.append([val["duration"]["startTimestamp"], val["duration"]["endTimestamp"], val["startLocation"]["latitudeE7"], val["startLocation"]["longitudeE7"], val["endLocation"]["latitudeE7"], val["endLocation"]["longitudeE7"], val["distance"], val["activityType"]])

    #make new df
    new_df = pd.DataFrame(lst, columns=["Start Timestamp", "End Timestamp", "Start Latitude", "Start Longitude", "End Latitude", "End Longitude", "Distance (m)", "Activity"])
    
    return new_df


def make_date_col(df):
    '''
    This dataframe takes in a dataframe.
    It takes datetime objects from
    a TimeStamp column, parses for the date,
    converts it to a string, and appends it
    to a list. the list is returned.
    '''
    date_lst = []

    for item in df["Start Timestamp"]:
        date_lst.append((item.date().strftime("%Y-%m-%d")))
    date_lst

    return date_lst

def fix_lat_lon_all(df):
    ''''
    This function takes in a dataframe, it
    then calls fix_lat_lon on all of the lat/long
    columns in the dataframe. The old columns are replaced with
    the fixed ones.
    '''
    fixed_start_lat_lst = fix_lat_lon(df, "Start Latitude", 2)
    df["Start Latitude"] = fixed_start_lat_lst

    fixed_start_lon_lst = fix_lat_lon(df, "Start Longitude", 1)
    df["Start Longitude"] = fixed_start_lon_lst

    fixed_end_lat_lst = fix_lat_lon(df, "End Latitude", 2)
    df["End Latitude"] = fixed_end_lat_lst

    fixed_end_lon_lst = fix_lat_lon(df, "End Longitude", 1)
    df["End Longitude"] = fixed_end_lon_lst
    


            

def fix_lat_lon(df, col, decimal_place):
    '''
    This function takes in a dataframe, column name,
    and a decimal_place number. It then converts the given column
    (which has lat/lon data) by adding a decimal point
    to the chosen position. Negative values are accounted for.
    '''

    fixed_lst = []
    # temp value to hold fixed values
    fixed = ""

    # go through column
    for i in range(df[col].size):
        # if value is negative, "decimal place" value
        # remains the same
        if(str(df[col].iloc[i])[0] != "-"):

            # add decimal to correct spot
            for j in range(decimal_place):
                fixed += str(df[col].iloc[i])[j]
            fixed += "."

            #add rest of letters
            for k in range(decimal_place, len(str(df[col].iloc[i]))):
                fixed += str(df[col].iloc[i])[k]
        # if not negative value, iterate once more
        else:   
            #add decimal
            for j in range(decimal_place + 1):
                fixed += str(df[col].iloc[i])[j]
            fixed += "."
            #add remaining values
            for k in range(decimal_place + 1, len(str(df[col].iloc[i]))):
                fixed += str(df[col].iloc[i])[k]

        #add fixed lat/lon value to list
        fixed_lst.append(fixed) 
        # reset temp value
        fixed = ""
    
    return fixed_lst

def encode_column(df, col_name):
    '''
    This function takes in a dataframe
    and column name and encodes the column
    values to numeric values. A list
    of these values is returned.
    '''
    le = LabelEncoder()

    le.fit(df[col_name])
    arr = le.transform(df[col_name])

    return arr


def split_col(df2, col_name, size0):
    '''
    This function takes in a dataframe, column name,
    and the size of another dataframe. Based on this size 
    items in the given dataframe column are added to two smaller
    lists (meant for smaller dataframes). The lists are returned.
    '''
    df0_lst = []
    df1_lst = []

    # add values for first df
    for i in range(size0):
        df0_lst.append(df2[col_name].iloc[i])

    # add values for 2nd df
    for i in range(size0, df2[col_name].size):
        df1_lst.append(df2[col_name].iloc[i])
    
    return df0_lst, df1_lst

  


def get_time_elapsed(df):
    '''
    This function takes in a dataframe,
    it then gets the difference between
    the End timestamp and Start timestamp
    columns, converts this to minutes, and 
    returns a series.
    '''
    # get difference of the timestamps
    dif_ser = df["End Timestamp"] - df["Start Timestamp"]

    dif_sec_lst= []

    #make a list of the total seconds of each time difference
    for i in range(dif_ser.size):
        dif_sec_lst.append(dif_ser.iloc[i].total_seconds())

    #convert to minutes, make series
    dif_ser_min = pd.Series(dif_sec_lst)
    dif_ser_min/= 60

    return dif_ser_min

def dist_plot(first_half, second_half):
    '''
    This function takes in two dataframes, 
    it then groups them by date and plots
    daily total distance (km) per activity segment
    ''' 
    # convert from m to km
    daily_total_distance_first= first_half.groupby("Date")["Distance (m)"].sum()
    daily_total_distance_first /= 1000

    daily_total_distance_last= second_half.groupby("Date")["Distance (m)"].sum()
    daily_total_distance_last /= 1000

    plt.figure()

    #labels
    plt.title("Daily Total Distance (km) Spent on Activity Segments in Madrid")
    plt.xlabel("Date")
    plt.ylabel("Distance (km)")
    plt.xticks([])

    #plot
    plt.scatter(daily_total_distance_first.index, daily_total_distance_first, color="red")
    plt.scatter(daily_total_distance_last.index, daily_total_distance_last, color="blue")
    plt.show()


def make_weekend_col(df):
    '''
    this function makes
    a column that labels weekends
    and weekdays
    '''
    weekend_lst = []
    for i in range(df["Activity"].size):
        if(df["Day of Week"].iloc[i] == "Friday" or df["Day of Week"].iloc[i] == "Saturday" or df["Day of Week"].iloc[i] == "Sunday"):
            weekend_lst.append(True)
        else:
            weekend_lst.append(False)

    return weekend_lst

def kNN(X_train, y_train, X_test, y_test):
    '''
    function to fit a kNN classifier
    '''
    
    knn_clf = KNeighborsClassifier(n_neighbors=2, metric="euclidean")

    knn_clf.fit(X_train, y_train)
    y_predicted = knn_clf.predict(X_test)

    acc = accuracy_score(y_test, y_predicted)
    print("accuracy :", acc)


def decision_tree(X, X_train, y_train, X_test, y_test):
    '''
    function to fit and plot
    a decision tree
    '''
    dt_clf = tree.DecisionTreeClassifier(max_depth=3, random_state=0)
    dt_clf.fit(X_train, y_train) # "train"
    y_predicted = dt_clf.predict(X_test)
    acc = accuracy_score(y_test, y_predicted)
    #print(y_predicted)
    print("accuracy :", acc)

    #plot tree
    plt.figure(figsize=[20, 20])
    tree.plot_tree(dt_clf, feature_names=X.columns, class_names={True:"Weekend", False:"Weekday"}, filled=True)