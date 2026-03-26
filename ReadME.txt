Spotify Music Hashing System

Overview: 

I implement a custom hash table in this project to efficiently store and retrieve Spotify 
song data from a dataset of over 100,000 tracks. As such, this system demonstrates how hashing 
can achieve near constant-time lookup while handling real-world challenges such as inconsistent 
data formatting and multi-artist songs.

Instructions:

Hello! Here are some basic instructions for running this program.

First, you want to make sure that you have downloaded all the dependencies and
libraries necessary for this code. As such, make sure you have pandas and streamlit installed. 
If not, you can install them via the pip install command in your terminal.

After that, make sure that you keep all these files in the same folder, as the main python script,
app.py, relies on both the preprocess.py file and the hashmap.py function to operate, while needing 
dataset.csv to access the data within.

Now, for the cool part. I am using Streamlit as a UI library as such once you have navigated to the folder
that contains all these files on your terminal, you want to type in streamlit run app.py or python -m streamlit run app.py
to use streamlit. When you do this, the terminal will take you to your web browser which will host the streamlit UI and from 
there, you can select the options for what you want to do. If you want to search a song, you can search a song based on the musician
and title and get presented with a whole host of metadata associated with the track. You can also click on the option to search the
number of songs an artist has in the dataset, and by typing in the artist's name, you will see the number of songs associated with him/her/they
in this dataset. Finally, you can view the statistics of the Hash Map which show you what it took to create this HashMap that you're
using and see if it's a good one. 

SideNote: 
The first run may take a few seconds to build the hash table, but any subsequent runs are faster due to caching