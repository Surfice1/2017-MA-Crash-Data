"""
Name: Alex Mazelsky
CS230: Section 5
Data: 2017 MA Car Crash Data
URL: https://2017-ma-crash-data-dssrrssbh7vagviaxvahgm.streamlit.app/

Description: Uses the 2017 Mass car crash data to demonstrate varius things.

"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import random

# https:\\docs.streamlit.io\library\api-reference
st.set_option('deprecation.showPyplotGlobalUse', False)

# function creates a list of lists of random numbers, and returns it and the parameters [PY1][PY2][PY3]
def create_random_lists(list_num, parameters=[10, 1, 100]):
    # parameters = length, min, max
    return [[random.randint(parameters[1], parameters[2]) for x in range(parameters[0])] for x in range(list_num)], parameters


def main():
    # Title
    st.title("MA Car Crashes in 2017")
    st.divider()

    # imports and cleans the dataframe [DA1]
    crashes_df = pd.read_csv("2017_crashes_modified.csv", index_col="CRASH_NUMB")
    crashes_df.dropna(inplace=True)
    # turns the city/town names into first letter caps for each word
    crashes_df["CITY_TOWN_NAME"] = crashes_df["CITY_TOWN_NAME"].str.title()
    # turns the CRASH_DATETIME into a new column HOURS, takes just the hours from datetime [DA9]
    crashes_df["HOURS"] = crashes_df["CRASH_DATETIME"].str[11:13].astype(int)
    # list comprehension to set the max speed limit at 70 [PY4]
    crashes_df["SPEED_LIMIT"] = [min(value, 70) for value in crashes_df["SPEED_LIMIT"]]

    # shows the data we imported
    # st.dataframe(crashes_df)

    # creates a sorted list with all the unique city/town names [DA2]
    city_town_list = sorted(crashes_df["CITY_TOWN_NAME"].unique())
    # select box for selecting the city/town [ST1]
    city_town_selected = st.selectbox("Select a city/town to display crashes for:", city_town_list, index=301)

    # creates a dictionary with the city/town names and the average latitude/longitude for all accidents
    mean_location_dict = crashes_df.groupby(["CITY_TOWN_NAME"]).mean(numeric_only=True).loc[:, ["LAT", "LON"]].to_dict(orient="index")

    # map stuff [VIZ1], scatterplot_layer data has filtering [DA4], view_state accesses dictionary values inside dictionary values twice [PY5]
    view_state = pdk.ViewState(latitude=mean_location_dict[city_town_selected]["LAT"], longitude=mean_location_dict[city_town_selected]["LON"], zoom=13)
    crashes_selected_town = crashes_df[crashes_df["CITY_TOWN_NAME"] == city_town_selected]
    scatterplot_layer = pdk.Layer(type="ScatterplotLayer", data=crashes_selected_town, get_position=["LON", "LAT"], get_radius=25, pickable=True, getColor=[0, 0, 255])
    crash_map = pdk.Deck(initial_view_state=view_state, layers=[scatterplot_layer], tooltip={"text": "{NUMB_VEHC} vehicles involved\n{NUMB_NONFATAL_INJR} nonfatal injuries\n{NUMB_FATAL_INJR} fatal injuries"})
    st.pydeck_chart(crash_map)
    st.divider()

    # select towns to compare data with [ST2]
    towns_to_compare = st.multiselect("Select which towns you want to compare data for:", city_town_list)

    # pivot table [DA6]
    st.caption("This table shows the averages for each crash in the selected towns")
    comparison_pt_mean = pd.pivot_table(data=crashes_df, index="CITY_TOWN_NAME", values=["NUMB_NONFATAL_INJR", "NUMB_FATAL_INJR", "NUMB_VEHC"], aggfunc="mean")
    comparison_pt_mean.rename(columns={"NUMB_NONFATAL_INJR": "Average Nonfatal Injuries", "NUMB_FATAL_INJR": "Average Fatal Injuries", "NUMB_VEHC": "Average Vehicle Amount"}, inplace=True)
    comparison_pt_mean.index.names = ["Town Name"]
    st.dataframe(comparison_pt_mean[comparison_pt_mean.index.isin(towns_to_compare)])

    # pivot table [DA6]
    st.caption("This table shows the totals for all crashes in the selected towns")
    comparison_pt_sum = pd.pivot_table(data=crashes_df, index="CITY_TOWN_NAME", values=["NUMB_NONFATAL_INJR", "NUMB_FATAL_INJR", "NUMB_VEHC"], aggfunc="sum")
    comparison_pt_sum.rename(columns={"NUMB_NONFATAL_INJR": "Total Nonfatal Injuries", "NUMB_FATAL_INJR": "Total Fatal Injuries", "NUMB_VEHC": "Total Vehicle Amount"}, inplace=True)
    comparison_pt_sum.index.names = ["Town Name"]
    st.dataframe(comparison_pt_sum[comparison_pt_mean.index.isin(towns_to_compare)])

    # graphs [VIZ1][VIZ2]
    st.divider()
    st.write("Graphs")
    st.bar_chart(crashes_df.sort_values(by="HOURS"), x="HOURS", y="NUMB_VEHC")
    st.bar_chart(crashes_df, x="HOURS", y="NUMB_FATAL_INJR")

    # double filter [DA5]
    st.divider()
    st.write("Car crashes with fatal injuries with a speed limit of under 30")
    st.dataframe(crashes_df[(crashes_df["NUMB_FATAL_INJR"] > 0) & (crashes_df["SPEED_LIMIT"] < 30)])

    # last graphs [VIZ3]
    st.divider()
    st.write("See if you can figure out what the sliders do")
    length1 = st.slider("Length 1", 1, 100, 10)
    min1 = st.slider("Minimum 1", 1, 100)
    max1 = st.slider("Maximum 1", 1, 100, 100)
    lists1 = create_random_lists(2, [length1, min1, max1])
    plt.plot(lists1[0][0], lists1[0][1])
    st.pyplot()

    st.divider()
    st.write("This one works a little differently")
    length2 = st.slider("Length 2", 1, 100, 50)
    min2 = st.slider("Min 2", 1, 100)
    max2 = st.slider("Max 2", 1, 100, 100)
    lists1 = create_random_lists(2, [length2, min2, max2])
    plt.plot(sorted(lists1[0][0]), lists1[0][1])
    st.pyplot()

    pass


main()
