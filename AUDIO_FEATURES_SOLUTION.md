# Audio Features Data Collection - Solution

## What We Discovered

**Problem:** Spotify deprecated the audio features API endpoint on November 27, 2024. New applications cannot access audio features (danceability, energy, valence, etc.) through the Spotify API.

**Proof:** We successfully tested our Spotify API credentials and confirmed:
- ✓ Track metadata retrieval: **Working**
- ✓ Artist metadata retrieval: **Working**
- ✗ Audio features retrieval: **HTTP 403 Forbidden**

## What we intended
**Created the File:** `spotify_data_pipeline.py`

This pipeline intended to work for:
- Track metadata (release_date, explicit)
- Artist metadata (popularity, followers, genres)

**Tested with:** 10 songs from our dataset
**Problem:** Retrieved the track and the artist, but audio feature retrieval was refused.

## Our Solution

**Hugging Face - Spotify Tracks Dataset**
- Link: https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset
- 114,000 tracks with audio features
- Organized by genre (125 genres)
- We ended up merging this dataset with our original Kaggle charts.csv dataset
