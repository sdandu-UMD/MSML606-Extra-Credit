import preprocess as pre
import pandas as pd

# Load dataset
df = pre.preprocess_dataset("dataset.csv")

print("Sample Data")
print(df[['artists', 'track_name']].head(10))


print("\nArtist Splitting Data")

# Test first 10 rows, wanted to make sure that we were splitting the artist names properly
for i, row in df.head(10).iterrows():
    raw_artists = row['artists']
    split = pre.split_artists(raw_artists)

    print(f"\nRow {i}")
    print("Raw:", raw_artists)
    print("Split:", split)


print("\nKey Generation Test")
# Wanted to see if we were able to generate keys that combines both the artists and the tracks
for i, row in df.head(10).iterrows():
    track = row['track_name']
    artists = pre.split_artists(row['artists'])

    print(f"\nTrack: {track}")

    for artist in artists:
        key = pre.create_key(artist, track)
        print("Key:", key)

# Real test using the Churchill Downs song to make sure that we could split artists and generate keys well
print("\nChurchill Downs")

# Find all rows related to Churchill Downs
mask = df['track_name'].str.contains("churchill", case=False, na=False)
subset = df[mask]

for _, row in subset.iterrows():
    track = row['track_name']
    artists = pre.split_artists(row['artists'])

    print("\nRaw Artists:", row['artists'])
    print("Clean Track:", track)
    print("Split Artists:", artists)

    for artist in artists:
        key = pre.create_key(artist, track)
        print("Generated Key:", key)