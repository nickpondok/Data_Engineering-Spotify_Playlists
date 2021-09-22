### Abstract

The goal of this project was to create an engineering pipeline to collect,store and vizualize data. For this project I attempted to pull audio features from songs that appear on spotify curated playlists. The goal was to see what features are most prominant on certain types of playlists. The application would be able to help upcoming or existing artists see which features are present on popular playlists so that they can create music that is similar to those playlists. The idea being if these artists are able to get their songs on spotify playlists (which receive millions and millions of streams) then they themselves would gain more notoriety.

### Design

The design of this project consisted of collecting data from Spotify by utlizing their python library, Spotipy. Several functions were created that all called on one another in order to generate a pipeline. The functions included collecting genre types, collecting playlist IDs, and collecting songs and their audio features. Once data was collected it was stored into a sql database locally on my computer which was then called on within my Streamlit script. Streamlit was used to deploy an app that visualized my data. The visualizations consisted of averges of audio features across genres and their specific playlists. 

### Data
Data was collected through the spotify api. I collected between 30-50 playlists for over 50 genres of music. It totaled to over 90,000 songs. The for each playlist, averages were taken for each of the audio features collected through the spotify api. Additionally, averages of the entire genres were calculated as well. 

### Algorithms

The main algorithms for this projected consisted of several key functions that helped collect the data. The first function gathered 60 genres from the spotify api. The next function gathered each spotify curated playlist for a given genre. The third function gathered each track on a given playlist, The fourth function got all the audio features for each given track. Lastly, these were all concatenated and stored into a sql database. On the streamlit side, averages were calculated and bar graphs were created. 

### Algorithms

The main algorithms for this projected consisted of several key functions that helped collect the data. The first function gathered 60 genres from the spotify api. The next function gathered each spotify curated playlist for a given genre. The third function gathered each track on a given playlist, The fourth function got all the audio features for each given track. Lastly, these were all concatenated and stored into a sql database. On the streamlit side, averages were calculated and bar graphs were created. 
