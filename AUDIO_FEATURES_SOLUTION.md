# Audio Features Data Collection - Solution

## The Problem

On **November 27, 2024**, Spotify deprecated the audio features API endpoint (`/v1/audio-features`). New apps or apps without existing extended mode access can no longer retrieve audio features like danceability, energy, valence, etc. through the API.

Your tests confirmed this - we successfully retrieved track and artist metadata, but all audio features requests returned HTTP 403 (Forbidden).

## Available Solutions

### Option 1: Download Pre-existing Dataset with Audio Features (RECOMMENDED)

Download the **Spotify Music Dataset** from Kaggle which includes:
- Audio features: danceability, energy, valence, tempo, loudness, acousticness, instrumentalness, liveness, speechiness
- Track metadata: artist name, album name, release date
- Popularity scores (0-100 based on streaming data)

**Steps:**
1. Go to https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset
2. Download the CSV file
3. Place it in `data/spotify_music_dataset.csv`
4. Run the merge script (see below)

**Pros:**
- Has all the audio features you need
- No API restrictions
- Includes popularity data

**Cons:**
- May not match all tracks in your Kaggle charts dataset
- Match rate depends on track name + artist name matching

### Option 2: Use Alternative Datasets

**Hugging Face - Spotify Tracks Dataset**
- Link: https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset
- 114,000 tracks with audio features
- Organized by genre (125 genres)
- We already tested this - 0% match with your current dataset

**Spotify 160k+ Tracks Dataset (1921-2020)**
- Available on Kaggle and GitHub
- Historical data with audio features
- May have better match rate for older charting songs

### Option 3: Use Your Current Dataset Without Audio Features

Modify your research approach to:
- Focus on artist-level features (genres, popularity, followers)
- Use track metadata (explicit, duration, release_date)
- Analyze streaming patterns and chart positions without audio features

## Recommended Approach: Merge with Spotify Music Dataset

I've created a script that will:
1. Download or load the Spotify Music Dataset
2. Match tracks from your charts with tracks in the dataset using:
   - Track ID (if available)
   - Track name + Artist name
3. Merge the audio features into your chart data
4. Report match statistics

### Expected Match Rate

Based on the different track IDs and song catalogs, expect:
- **10-30% match rate** for track ID matching (different datasets use different IDs)
- **40-70% match rate** for name + artist matching (depends on data cleaning and normalization)

This means you'll have audio features for a portion of your charting songs, which may still be sufficient for your analysis.

## Next Steps

1. Download the Spotify Music Dataset from Kaggle
2. Place it in `data/spotify_music_dataset.csv`
3. Run: `micromamba run -n seasons-of-sound python merge_spotify_music_dataset.py`

## References

- [Spotify API Audio Features Deprecation Discussion](https://community.spotify.com/t5/Spotify-for-Developers/Web-API-Get-Track-s-Audio-Features-403-error/td-p/6654507)
- [Spotify Music Dataset on Kaggle](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset)
- [Hugging Face Spotify Tracks Dataset](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset)
- [Research: Prediction of Spotify Chart Success](https://arxiv.org/html/2508.11632)
