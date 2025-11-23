# Spotify Data Pipeline Setup

This guide will help you set up and run the Spotify data pipeline to gather audio features and artist metadata for your songs.

## Step 1: Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (create one if needed)
3. Click "Create an App"
4. Fill in the app details:
   - App name: "Seasons of Sound Data Pipeline" (or any name)
   - App description: "Gathering audio features for research project"
   - Check the terms of service box
5. Click "Create"
6. On your app's page, you'll see:
   - **Client ID**
   - **Client Secret** (click "Show Client Secret")

## Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_actual_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_client_secret
   ```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Pipeline

For testing with 10 songs:
```bash
python spotify_data_pipeline.py
```

This will create the following files in the `data/` folder:
- `spotify_test_audio_features.csv` - Audio features (danceability, energy, valence, etc.)
- `spotify_test_track_metadata.csv` - Track metadata (release_date, explicit)
- `spotify_test_artist_metadata.csv` - Artist metadata (popularity, followers, genres)
- `spotify_test_combined.csv` - Combined track data

## Data Fields

### Audio Features
- danceability, energy, valence, tempo, loudness
- acousticness, instrumentalness, liveness, speechiness
- duration_ms, key, mode, time_signature

### Track Metadata
- release_date, explicit

### Artist Metadata
- artist_popularity, artist_followers, artist_genres

## Next Steps

After testing with 10 songs, you can modify the script to process all tracks in your dataset by changing line 225 in `spotify_data_pipeline.py`:

```python
# Change this:
unique_track_ids = df['track_id'].unique()[:10]

# To this (process all tracks):
unique_track_ids = df['track_id'].unique()
```

**Note:** Processing all tracks will take considerable time due to API rate limits. Consider processing in batches.
