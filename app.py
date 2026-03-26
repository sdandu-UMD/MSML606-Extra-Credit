import streamlit as st
import time
import re
from hashmap import HashMap
import preprocess as pre

# Loading Data
@st.cache_data
def load_data():
    return pre.preprocess_dataset("dataset.csv")

# Building our HashMap
@st.cache_resource
def build_hashmap(df):
    hashmap = HashMap()

    # We iterate through the rows of the dataframe, storing the most relevant information
    for row in df.itertuples(index=False):
        track = row.track_name 
        artists = pre.split_artists(row.artists) # To deal with multiple artists for one track

        value = {
            "track": track,
            "artists": artists,
            "album": getattr(row, "album_name", None),
            "popularity": getattr(row, "popularity", None),
            "danceability": getattr(row, "danceability", None),
            "energy": getattr(row, "energy", None),
            "tempo": getattr(row, "tempo", None),
            "loudness": getattr(row, "loudness", None)
        }

        for artist in artists: # If we have multiple artists, we make sure to create multiple keys, keeping the track part of the key constant
            key = pre.create_key(artist, track)
            hashmap.insert(key, value)

    return hashmap


df = load_data()
hashmap = build_hashmap(df)

# App Dashboard
st.title("Spotify Music Hashing System")

st.sidebar.header("Options") # This shows us what we can do with this database on the sidebar
option = st.sidebar.radio(
    "Choose Operation",
    ["Search Song", "Count Songs by Artist", "View Hash Stats"]
)

# Searching for a Song
if option == "Search Song":
    st.header("Search Song")

    # No matter what people input, we make sure that it has the same consistent formatting as the data making it easier for the user
    artist = st.text_input("Artist Name")
    track = st.text_input("Track Name")
    artist = pre.clean_text(artist)
    track = pre.clean_text(track)


    if st.button("Search"):
        key = pre.create_key(artist.lower(), track.lower())
        # Calculating the Lookup time for a search
        start = time.perf_counter()
        result = hashmap.search(key)
        end = time.perf_counter()

        st.write(f"Lookup Time: {end - start:.8f} seconds")

        if result:
            st.success("Song Found!")
            st.json(result)
        else:
            st.error("Song Not Found")


# Counting the Number of Songs by an Artist 
elif option == "Count Songs by Artist":
    st.header("Count Songs by Artist")

    artist = st.text_input("Artist Name")

    if st.button("Count"):
        artist = pre.clean_text(artist)
        count = 0

        for item in hashmap.table:
            if item and item != ("__DELETED__", None): # Checks to see if we're not looking at a recently deleted or empty node
                if artist in item[0]:
                    count += 1

        st.write(f"Total songs by '{artist}': {count}")


# Visualing the Statistics of the HashMap
elif option == "View Hash Stats":
    st.header("Hash Table Statistics")

    stats = hashmap.get_stats()
    
    # Helps visualize how efficient our hash table implementation really is.
    st.metric("Load Factor", f"{stats['load_factor']:.8f}")
    st.metric("Avg Insert Probes", f"{stats['avg_insert_probes']:.8f}")
    st.metric("Total Collisions", stats['collisions'])
