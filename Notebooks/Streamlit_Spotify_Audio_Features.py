import pickle
import sqlite3
import datetime 
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pyodbc
import requests
import spotipy
import pandas as pd
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import matplotlib.pyplot as plt


#establish engine to make call to sql db
engine = create_engine("sqlite:///sql_db/spotify_features.db")

#get list of genre_ids for user inputs
genre_ids =list(set(pd.read_sql('SELECT * FROM audio_features',engine)['genre']))
genre_ids.sort()


#get the averages for an entire genre
def get_average_features(genre_id):
    genre_df = pd.read_sql(f'SELECT * FROM audio_features WHERE GENRE == "{genre_id}"',engine)
    genre_df.drop_duplicates(subset=['song_name'],inplace=True)
    try:
        avg_df=pd.DataFrame(genre_df.mean())
        avg_df.sort_values(by=[0],inplace=True)
        avg_df=avg_df.reset_index()
        avg_df.set_index('index', inplace=True)
        return avg_df
    except spotipy.exceptions.SpotifyException:
        return f'The genre {genre} does not have playlists'
    

#get the names of playlists for each genre
def get_playlist_names(genre_id):
    genre_df = pd.read_sql(f'SELECT * FROM audio_features WHERE GENRE == "{genre_id}"',engine)
    playlist_options = list(set(genre_df['playlist_name']))
    return playlist_options

#create bar graphs for an entire genre
def create_genre_table(genre_id):
    avg_df = get_average_features(genre_id)
    if avg_df.empty:
        st.write('Sorry, there is no data for this playlist')
    else:
        main_title = st.write(f'averages for {genre_id} playlist features')

        table1_title = st.write('Audio Features')
        plt.xticks(rotation=80, horizontalalignment="center")
        aud_features_chart = st.bar_chart(avg_df[1:9])

        table2_title =st.write('Duration, Key, Loudness, Time Signature')
        plt.xticks(rotation=80, horizontalalignment="center")
        combo= pd.concat([avg_df[0:1],avg_df[9:12]])
        dkt_chart = st.bar_chart(combo)

        table3_title = st.write('Popularity and Temp')
        plt.xticks(rotation=80, horizontalalignment="center")
        pt_chart = st.bar_chart(avg_df[12:-1])

        return (main_title,table1_title,aud_features_chart,table2_title,dkt_chart,table3_title,pt_chart)

#get bar graph for specific playlist
def create_playlist_table(genre,playlist_name):
    genre_df = pd.read_sql(f'SELECT * FROM audio_features WHERE GENRE == "{genre}"',engine)
    new_df = genre_df[genre_df['playlist_name']==playlist_name]
    new_df.drop_duplicates(subset=['song_name'],inplace=True)
    avg_df=pd.DataFrame(new_df.mean())
    avg_df.sort_values(by=[0],inplace=True)
    avg_df=avg_df.reset_index()
    avg_df.set_index('index', inplace=True)
    if avg_df.empty:
        st.write('Sorry, there is no data for this playlist')
    else:
        main_title = st.write(f'averages for {playlist_name} song features')

        table1_title = st.write('Audio Features')
        plt.xticks(rotation=80, horizontalalignment="center")
        aud_features_chart = st.bar_chart(avg_df[1:9])


        table2_title =st.write('Duration, Key, Loudness, Time Signature')
        plt.xticks(rotation=80, horizontalalignment="center")
        combo= pd.concat([avg_df[0:1],avg_df[9:12]])
        dkt_chart = st.bar_chart(combo)

        table3_title = st.write('Popularity and Temp')
        plt.xticks(rotation=80, horizontalalignment="center")
        pt_chart = st.bar_chart(avg_df[12:-1])
    
#start of webpage
st.title('Audio Features for Spotify Playlists')


#checkbox to show explanation of each audio feature
if st.checkbox('Show Audio Feature Explanation'):
    with st.container():
        st.write('Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.')
        st.write('Acousticness: A measure from 0.0 to 1.0 of whether the track is acoustic.')
        st.write('Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.')
        st.write('Instrumentalness: Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.')
        st.write('Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.')
        st.write('Loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track. Values typical range between -14 and 0 db.')
        st.write('Speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.')
        st.write('Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.')
        st.write('Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).')
        st.write('Mode:Indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.')
        st.write("Source [link](https://medium.com/@boplantinga/what-do-spotifys-audio-features-tell-us-about-this-year-s-eurovision-song-contest-66ad188e112a)")

    


#prompt to user to select a genre and check whether or not they want the graphs to show(multi-layered prompt)
user_input =st.selectbox('Select Genre', genre_ids,key='genre',help="Select Genre to display averages of audio features",)
if st.checkbox('Show Genre Audio Features'):
    create_genre_table(user_input)
    if st.checkbox('Show Playlist Audio Features'):
        for genre in genre_ids:
            if user_input == genre:
                playlist_choice = st.selectbox('Choose playlist', get_playlist_names(genre),key='playlist',help = "choose a playlist to display the audio feature averages")
                create_playlist_table(user_input,playlist_choice)
                
    
    
    
                           
                           
                       

