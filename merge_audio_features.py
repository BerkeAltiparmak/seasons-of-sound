"""
Alternative Data Pipeline - Merge Kaggle Charts with Hugging Face Audio Features
Since Spotify deprecated the audio features API endpoint on Nov 27, 2024,
we'll use the maharshipandya/spotify-tracks-dataset from Hugging Face instead.
"""

import pandas as pd
from datasets import load_dataset
import time


def load_huggingface_spotify_data():
    """Load the Spotify tracks dataset from Hugging Face."""
    print("Loading Spotify audio features from Hugging Face...")
    print("This may take a few minutes on first run...")

    # Load the dataset
    dataset = load_dataset("maharshipandya/spotify-tracks-dataset")

    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset['train'])

    print(f"Loaded {len(df):,} tracks with audio features")
    print(f"Columns: {list(df.columns)}")

    return df


def load_kaggle_charts(limit=None):
    """Load the Kaggle charts dataset."""
    print("\nLoading Kaggle charts data...")
    df = pd.read_csv('data/charts.csv')

    if limit:
        # Get unique track IDs
        unique_tracks = df['track_id'].unique()[:limit]
        df = df[df['track_id'].isin(unique_tracks)]

    print(f"Loaded {len(df):,} chart entries ({df['track_id'].nunique():,} unique tracks)")

    return df


def merge_datasets(charts_df, audio_features_df, test_mode=True):
    """
    Merge Kaggle charts with audio features from Hugging Face.

    Strategy:
    1. First try matching by track_id (if available in both datasets)
    2. Fall back to matching by track name + artist name
    """
    print("\nMerging datasets...")

    # Check if Hugging Face dataset has track_id column
    if 'track_id' in audio_features_df.columns:
        print("Attempting merge by track_id...")
        merged = pd.merge(
            charts_df,
            audio_features_df,
            on='track_id',
            how='left'
        )
        match_rate = (merged['danceability'].notna().sum() / len(merged)) * 100
        print(f"  Match rate by track_id: {match_rate:.1f}%")

        if match_rate > 50:
            return merged

    # Prepare for name-based matching
    print("Preparing for name-based matching...")

    # Clean and normalize names for better matching
    def clean_name(name):
        if pd.isna(name):
            return ""
        return str(name).lower().strip()

    # Create normalized columns
    charts_df['name_clean'] = charts_df['name'].apply(clean_name)
    audio_features_df['track_name_clean'] = audio_features_df['track_name'].apply(clean_name)

    # For artists, we need to handle the list format in charts_df
    def extract_first_artist(artist_str):
        if pd.isna(artist_str):
            return ""
        # Handle string representation of list
        artist_str = str(artist_str).strip("[]'\"")
        # Get first artist
        first_artist = artist_str.split(',')[0].strip("'\"")
        return clean_name(first_artist)

    charts_df['artist_clean'] = charts_df['artists'].apply(extract_first_artist)
    audio_features_df['artist_clean'] = audio_features_df['artists'].apply(clean_name)

    # Merge on track name + artist
    print("Attempting merge by track name + artist...")
    merged = pd.merge(
        charts_df,
        audio_features_df,
        left_on=['name_clean', 'artist_clean'],
        right_on=['track_name_clean', 'artist_clean'],
        how='left',
        suffixes=('_kaggle', '_hf')
    )

    match_rate = (merged['danceability'].notna().sum() / len(merged)) * 100
    print(f"  Match rate by name+artist: {match_rate:.1f}%")

    # Clean up temporary columns
    merged = merged.drop(columns=['name_clean', 'track_name_clean', 'artist_clean'], errors='ignore')

    return merged


def create_combined_dataset(limit=10):
    """
    Create a combined dataset with chart data and audio features.

    Args:
        limit: Number of unique tracks to process (None for all)
    """
    start_time = time.time()

    # Load data
    audio_features_df = load_huggingface_spotify_data()
    charts_df = load_kaggle_charts(limit=limit)

    # Merge datasets
    merged_df = merge_datasets(charts_df, audio_features_df)

    # Select relevant columns for analysis
    output_columns = [
        # Chart data
        'date', 'country', 'position', 'streams', 'track_id',
        'name', 'artists',
        # Audio features
        'danceability', 'energy', 'valence', 'tempo', 'loudness',
        'acousticness', 'instrumentalness', 'liveness', 'speechiness',
        'duration_ms', 'key', 'mode', 'time_signature',
        # Metadata
        'explicit', 'popularity'
    ]

    # Keep only columns that exist
    output_columns = [col for col in output_columns if col in merged_df.columns]
    result_df = merged_df[output_columns].copy()

    # Save results
    output_file = f'data/merged_data_test.csv' if limit else 'data/merged_data_full.csv'
    result_df.to_csv(output_file, index=False)

    # Report statistics
    print(f"\n{'='*60}")
    print(f"Results Summary:")
    print(f"{'='*60}")
    print(f"Total chart entries: {len(result_df):,}")
    print(f"Unique tracks: {result_df['track_id'].nunique():,}")
    print(f"Tracks with audio features: {result_df['danceability'].notna().sum():,}")
    print(f"Match rate: {(result_df['danceability'].notna().sum() / len(result_df)) * 100:.1f}%")
    print(f"\nMissing data by feature:")
    for col in ['danceability', 'energy', 'valence', 'tempo', 'acousticness']:
        missing = result_df[col].isna().sum()
        print(f"  {col}: {missing:,} missing ({(missing/len(result_df))*100:.1f}%)")

    print(f"\nOutput saved to: {output_file}")
    print(f"Time elapsed: {time.time() - start_time:.1f} seconds")

    # Show sample
    print(f"\nSample of merged data:")
    print(result_df[['name', 'danceability', 'energy', 'valence']].head(10))

    return result_df


if __name__ == "__main__":
    # Test with 10 unique tracks
    print("Testing data merge pipeline with 10 tracks...")
    print("="*60)

    result = create_combined_dataset(limit=10)

    print("\n✓ Pipeline test complete!")
    print("\nTo process all tracks, modify the script to call:")
    print("  create_combined_dataset(limit=None)")
