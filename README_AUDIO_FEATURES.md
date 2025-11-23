# Seasons of Sound - Data Collection Summary

## What We Discovered

**Problem:** Spotify deprecated the audio features API endpoint on November 27, 2024. New applications cannot access audio features (danceability, energy, valence, etc.) through the Spotify API.

**Proof:** We successfully tested our Spotify API credentials and confirmed:
- ✓ Track metadata retrieval: **Working**
- ✓ Artist metadata retrieval: **Working**
- ✗ Audio features retrieval: **HTTP 403 Forbidden**

## What We Created

### 1. Spotify API Pipeline (Limited Functionality)
**File:** `spotify_data_pipeline.py`

This pipeline works for:
- Track metadata (release_date, explicit)
- Artist metadata (popularity, followers, genres)

**Tested with:** 10 songs from our dataset
**Output:** Created 3 CSV files with available data in `data/` folder

### 2. Alternative Solution: Merge with External Dataset
**File:** `merge_spotify_music_dataset.py`

This script merges our Kaggle charts data with a pre-existing Spotify dataset that includes audio features.

## How to Get Audio Features

### Step 1: Download the Spotify Music Dataset
1. Go to: https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset
2. Download the CSV file
3. Place it in: `data/spotify_music_dataset.csv`

### Step 2: Run the Merge Script

**Test with 10 songs:**
```bash
micromamba run -n seasons-of-sound python merge_spotify_music_dataset.py
```

**Process all songs:**
```bash
micromamba run -n seasons-of-sound python merge_spotify_music_dataset.py --full
```

### Step 3: Analyze Our Results

The script will create:
- `merged_charts_with_audio_test.csv` (10 songs) or
- `merged_charts_with_audio_full.csv` (all songs)

With columns:
- **From Our Kaggle data:** date, country, position, streams, track_id, name, artists
- **From Spotify Music Dataset:** danceability, energy, valence, tempo, loudness, acousticness, instrumentalness, liveness, speechiness, popularity

## Expected Results

Oour charting songs will match with the Spotify Music Dataset
- Matching is done by track name + artist name
- Not all charting songs will be in the external dataset
- We'll still have a substantial sample for our analysis
