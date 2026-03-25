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

    for row in df.itertuples(index=False):
        track = row.track_name
        artists = pre.split_artists(row.artists)

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

        for artist in artists:
            key = pre.create_key(artist, track)
            hashmap.insert(key, value)

    return hashmap


df = load_data()
hashmap = build_hashmap(df)

# App Dashboard
st.title("Spotify Music Hashing System")

st.sidebar.header("Options")
option = st.sidebar.radio(
    "Choose Operation",
    ["Search Song", "Count Songs by Artist", "View Hash Stats"]
)

# Searching for a Song
if option == "Search Song":
    st.header("Search Song")

    artist = st.text_input("Artist Name")
    track = st.text_input("Track Name")
    artist = pre.clean_text(artist)
    track = pre.clean_text(track)


    if st.button("Search"):
        key = pre.create_key(artist.lower(), track.lower())

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
        artist = artist.lower()
        count = 0

        for item in hashmap.table:
            if item and item != ("__DELETED__", None):
                if artist in item[0]:
                    count += 1

        st.write(f"Total songs by '{artist}': {count}")


# Visualing the Statistics of the HashMap
elif option == "View Hash Stats":
    st.header("Hash Table Statistics")

    stats = hashmap.get_stats()

    st.metric("Load Factor", f"{stats['load_factor']:.4f}")
    st.metric("Avg Insert Probes", f"{stats['avg_insert_probes']:.4f}")
    st.metric("Avg Search Probes", f"{stats['avg_search_probes']:.4f}")
    st.metric("Total Collisions", stats['collisions'])

    st.info("Lower probe counts = more efficient hashing")