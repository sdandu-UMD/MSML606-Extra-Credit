import pandas as pd
import re

# Cleaning text to make it easier to search for songs and artists
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9 ;]', '', text)
    return text.strip()

def clean_track(text):
    text = clean_text(text)
    text = re.sub(r'feat.*', '', text)  # remove "feat..."
    return text.strip()

def split_artists(artist_string):
    return [clean_text(a) for a in re.split(r'[;,/&]', artist_string) if a.strip()]

def create_key(artist, track):
    return f"{artist}::{track}"

def preprocess_dataset(path):
    df = pd.read_csv(path)

    df['track_name'] = df['track_name'].apply(clean_track)
    df['artists'] = df['artists'].apply(clean_text)

    df = df.drop_duplicates(subset=['track_name', 'artists'])
    return df