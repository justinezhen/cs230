"""
Class: CS230--Section 1
Name: Justine Zhen
Description: (Program that shows data for Skyscrapers in the world. Shows the graph of the amount of floors a building
has and the year that the building was built. Program that includes a bar chart, a pie chart, and sliders.--See below)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""


import pandas as pd
from matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pydeck as pdk


default_min_floor = 90
default_year = 2000

# function to read the data file
def read_data():
    df = pd.read_csv("Skyscrapers2021.csv").set_index("RANK")
    df.dropna()

    return df

# function that filters the data to include the city, floors, and completion
def filter_data(sel_cities, min_floor, sel_year):
    df = read_data()
    df = df.loc[(df['CITY'].isin(sel_cities)) & (df['FLOORS'] > min_floor) & (df['COMPLETION'] > sel_year)]

    return df

# function that appends all cities to a list
def all_cities():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['CITY'] not in lst:
            lst.append(row['CITY'])

    return lst

# function to output the link of a selected Skyscraper
def data_link():
    df = read_data()
    building = st.multiselect("Please select a skyscraper to get the website for it", df["NAME"])
    if len(building) > 0:
        st.write("Here is the link for more information on the " + (building[0]))
        linkForBuilding = df.loc[df["NAME"] == (building[0])]
        st.write(linkForBuilding["Link"])


# function that counts number of buildings in city
def count_building(cities, df):
    return [df.loc[df['CITY'].isin([CITY])].shape[0] for CITY in cities]

# function to iterate through floors and cities of the dataframe and creates a dictionary
def building_floors(df):
    floors = [row['FLOORS'] for ind, row in df.iterrows()]
    cities = [row['CITY'] for ind, row in df.iterrows()]

    dict = {}
    for city in cities:
        dict[city] = []

    for i in range(len(floors)):
        dict[cities[i]].append(floors[i])

    return dict


# function to find the average floors in the data
def avg_floor(dict_floors):
    dict = {}
    for key in dict_floors.keys():
        dict[key] = np.mean(dict_floors[key])

    return dict


# function that creates a pie chart
def pie_chart(counts, sel_cities):
    plt.figure()

    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = 0.1

    plt.pie(counts, labels=sel_cities, explode=explodes, autopct="%.2f")
    plt.title(f"Buildings in Cities: {', '.join(sel_cities)}")
    return plt


# function that creates a bar chart
def bar_chart(dict_avg):
    plt.figure()

    x = dict_avg.keys()
    y = dict_avg.values()
    plt.bar(x, y, color="pink")
    plt.xticks(rotation=45)
    plt.ylabel = ("Floors")
    plt.xlabel = ("Cities")
    plt.title(f"Average Floors for Skyscrapers in the following Cities: {', '.join(dict_avg.keys())}")

    return plt


# function to generate a map
def generate_map(df):
    map_df = df.filter(['NAME', 'Latitude', 'Longitude'])
    pd.to_numeric(df['Latitude'])
    pd.to_numeric(df['Longitude'])
    view_world = pdk.ViewState(latitude=map_df["Latitude"].mean(),
                               longitude=map_df["Longitude"].mean(),
                               zoom=0)
    layer = pdk.Layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[Longitude, Latitude]',
                      get_radius=700000,
                      get_color=[20, 120, 200],
                      pickable=True)
    tool_tip = {'html': 'Building:<br><b>{NAME}</b>', 'style': {'backgroundColor': 'teal', "color": 'white'}}
    map = pdk.Deck(map_style='mapbox://styles/mapbox/streets-v9',
                   initial_view_state=view_world,
                   layers=[layer],
                   tooltip=tool_tip)

    st.pydeck_chart(map)


def main():
    st.title("Skyscraper Data")
    st.write("This is the data for Skyscrapers in 2021.")

    st.sidebar.write("Select the skyscraper you want more information for.")

    data_link()

    cities = st.sidebar.multiselect("Select a city: ", all_cities())
    min_floor = st.sidebar.slider("Min floors: ", 0, 168)
    year = st.sidebar.slider("Year of completion for building: ", 1931, 2020)

    data = filter_data(cities, min_floor, year)
    series = count_building(cities, data)

    if len(cities) > 0 and min_floor > 0 and year > 0:
        st.write("This map shows the building locations")
        st.write("Hover over the point to see the names of the skyscrapers")
        generate_map(data)

        st.write("Below is a bar chart based on the selected data")
        st.pyplot(bar_chart(avg_floor(building_floors(data))))

        st.write("Below is a pie chart based on the selected data")
        st.pyplot(pie_chart(series, cities))


main()

