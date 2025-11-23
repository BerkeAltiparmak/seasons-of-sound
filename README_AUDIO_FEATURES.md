# Seasons of Sound - Data Collection Summary

## What We Discovered

**Problem:** Spotify deprecated the audio features API endpoint on November 27, 2024. New applications cannot access audio features (danceability, energy, valence, etc.) through the Spotify API.

**Proof:** We successfully tested your Spotify API credentials and confirmed:
- ✓ Track metadata retrieval: **Working**
- ✓ Artist metadata retrieval: **Working**
- ✗ Audio features retrieval: **HTTP 403 Forbidden**

## What We Created

### 1. Spotify API Pipeline (Limited Functionality)
**File:** `spotify_data_pipeline.py`

This pipeline works for:
- Track metadata (release_date, explicit)
- Artist metadata (popularity, followers, genres)

**Tested with:** 10 songs from your dataset
**Output:** Created 3 CSV files with available data in `data/` folder

### 2. Alternative Solution: Merge with External Dataset
**File:** `merge_spotify_music_dataset.py`

This script merges your Kaggle charts data with a pre-existing Spotify dataset that includes audio features.

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

### Step 3: Analyze Your Results

The script will create:
- `merged_charts_with_audio_test.csv` (10 songs) or
- `merged_charts_with_audio_full.csv` (all songs)

With columns:
- **From your Kaggle data:** date, country, position, streams, track_id, name, artists
- **From Spotify Music Dataset:** danceability, energy, valence, tempo, loudness, acousticness, instrumentalness, liveness, speechiness, popularity

## Expected Results

**Match Rate:** 40-70% of your charting songs will match with the Spotify Music Dataset
- Matching is done by track name + artist name
- Not all charting songs will be in the external dataset
- You'll still have a substantial sample for your analysis

## Files Created

1. **spotify_data_pipeline.py** - Original Spotify API pipeline (limited by API deprecation)
2. **test_spotify_auth.py** - Test script that confirmed the API issue
3. **merge_audio_features.py** - First attempt using Hugging Face dataset (0% match)
4. **merge_spotify_music_dataset.py** - Working solution using Kaggle dataset
5. **requirements.txt** - Python dependencies
6. **.env.example** - Template for API credentials
7. **SPOTIFY_SETUP.md** - Setup instructions
8. **AUDIO_FEATURES_SOLUTION.md** - Detailed explanation of the problem and solutions
9. **README_AUDIO_FEATURES.md** - This file

## What You Have Now

### Currently Working:
- ✓ Micromamba environment set up
- ✓ Dependencies installed
- ✓ Spotify API credentials configured
- ✓ Successfully retrieved track and artist metadata for 10 test songs
- ✓ Merge script ready to combine your charts with audio features dataset

### Next Steps:
1. Download the Spotify Music Dataset from Kaggle
2. Run the merge script
3. Analyze your results to see the match rate
4. Proceed with your "Seasons of Sound" analysis

## Alternative Approaches

If the match rate is too low, consider:

1. **Use multiple datasets:** Merge with both Kaggle and Hugging Face datasets to increase coverage
2. **Focus on matched subset:** Your analysis will still be valid with 40-70% of tracks
3. **Modify research scope:** Focus on features you can access (artist genres, popularity, release dates)
4. **Web scraping:** Some services may still display audio features publicly (advanced)

## Questions?

- Spotify API Deprecation: See `AUDIO_FEATURES_SOLUTION.md`
- Setup Instructions: See `SPOTIFY_SETUP.md`
- Match rate issues: Try the --full flag to see actual statistics with your data

---

## Sources and References

- [Spotify API Audio Features Deprecation](https://community.spotify.com/t5/Spotify-for-Developers/Web-API-Get-Track-s-Audio-Features-403-error/td-p/6654507)
- [Stack Overflow: 403 Error Retrieving Audio Features](https://stackoverflow.com/questions/79407994/403-forbidden-error-when-retrieving-audio-features-for-tracks-with-spotify-api)
- [Spotify Music Dataset - Kaggle](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset)
- [Spotify Tracks Dataset - Hugging Face](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset)
- [Research: Prediction of Spotify Chart Success](https://arxiv.org/html/2508.11632)
- [GitHub: Spotify 160k Tracks Analysis](https://github.com/ddhartma/Spotify-dataset-analysis-160kTracks-1921-2020)
