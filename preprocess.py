import pandas as pd
import re

# Cleaning text to make it easier to search for songs and artists
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower() # Lower Case
    text = re.sub(r'[^a-z0-9 ;]', '', text) # Remove all special characters besides numbers, letters, and semicolons (Used to split artists)
    return text.strip()

# Building on Cleaning text by taking out the feature part of tracks, that way we reduce the duplicate information in the dataframe
def clean_track(text):
    text = clean_text(text)
    text = re.sub(r'feat.*', '', text)  # remove "feat..."
    return text.strip()

# We split up artists so that we can have multiple keys with each artist being assosciated with the same track.
# However, this allows us to track the count of the songs that each artist has made better.
def split_artists(artist_string):
    return [clean_text(a) for a in re.split(r'[;,/&]', artist_string) if a.strip()]

# Here, we combine the artist and track to create a key for lookups
def create_key(artist, track):
    return f"{artist}::{track}"

# Preprocessing the dataset via clean_text and making sure that our dataframe has no duplicates.
def preprocess_dataset(path):
    df = pd.read_csv(path)

    df['track_name'] = df['track_name'].apply(clean_track)
    df['artists'] = df['artists'].apply(clean_text)

    df = df.drop_duplicates(subset=['track_name', 'artists'])
    return df