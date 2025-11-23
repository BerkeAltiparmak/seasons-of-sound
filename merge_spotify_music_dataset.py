"""
Merge Kaggle Charts with Spotify Music Dataset
This script merges your Kaggle charts data with a Spotify dataset containing audio features.
"""

import pandas as pd
import numpy as np


def clean_string(s):
    """Clean and normalize strings for matching."""
    if pd.isna(s):
        return ""
    return str(s).lower().strip()


def extract_first_artist(artist_field):
    """Extract first artist from various formats."""
    if pd.isna(artist_field):
        return ""

    artist_str = str(artist_field)

    # Handle list format from Kaggle data: "['Artist Name']"
    if artist_str.startswith('['):
        artist_str = artist_str.strip("[]'\"")
        # Get first artist if multiple
        first_artist = artist_str.split(',')[0].strip("'\"")
        return clean_string(first_artist)

    return clean_string(artist_str)


def load_kaggle_charts(limit=None):
    """Load your existing Kaggle charts data."""
    print("Loading Kaggle charts data...")
    df = pd.read_csv('data/charts.csv')

    if limit:
        # Get unique track IDs for testing
        unique_tracks = df['track_id'].unique()[:limit]
        df = df[df['track_id'].isin(unique_tracks)]
        print(f"  Loaded {len(df):,} chart entries ({df['track_id'].nunique():,} unique tracks)")
    else:
        print(f"  Loaded {len(df):,} chart entries ({df['track_id'].nunique():,} unique tracks)")

    return df


def load_spotify_music_dataset(file_path='data/spotify_music_dataset.csv'):
    """Load the Spotify Music Dataset with audio features."""
    print(f"\nLoading Spotify Music Dataset from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print(f"  Loaded {len(df):,} tracks with audio features")
        print(f"  Columns: {list(df.columns)[:10]}...")  # Show first 10 columns
        return df
    except FileNotFoundError:
        print(f"\n  ERROR: File not found: {file_path}")
        print("\n  Please download the dataset from:")
        print("    https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset")
        print(f"  And place it at: {file_path}")
        return None


def merge_datasets(charts_df, music_df):
    """Merge charts with music dataset using track name + artist matching."""
    print("\nPreparing data for matching...")

    # Create clean columns for matching
    charts_df['track_name_clean'] = charts_df['name'].apply(clean_string)
    charts_df['artist_clean'] = charts_df['artists'].apply(extract_first_artist)

    # Determine column names in music dataset (they may vary)
    music_cols = music_df.columns.tolist()

    # Find track name column
    track_col = None
    for col in ['track_name', 'Track Name', 'name', 'Name', 'song', 'Song']:
        if col in music_cols:
            track_col = col
            break

    # Find artist column
    artist_col = None
    for col in ['artist_name', 'Artist Name', 'artists', 'artist', 'Artist']:
        if col in music_cols:
            artist_col = col
            break

    if not track_col or not artist_col:
        print(f"  ERROR: Could not find track/artist columns in music dataset")
        print(f"  Available columns: {music_cols}")
        return None

    print(f"  Using columns: track='{track_col}', artist='{artist_col}'")

    # Clean music dataset columns
    music_df['track_name_clean'] = music_df[track_col].apply(clean_string)
    music_df['artist_clean'] = music_df[artist_col].apply(clean_string)

    # Perform merge
    print("\nMerging datasets by track name + artist...")
    merged_df = pd.merge(
        charts_df,
        music_df,
        on=['track_name_clean', 'artist_clean'],
        how='left',
        suffixes=('_kaggle', '_spotify')
    )

    # Calculate match rate
    # Check if we have audio features - they could be named differently
    audio_feature_cols = ['danceability', 'Danceability', 'energy', 'Energy']
    matched_col = None
    for col in audio_feature_cols:
        if col in merged_df.columns:
            matched_col = col
            break

    if matched_col:
        matches = merged_df[matched_col].notna().sum()
        match_rate = (matches / len(merged_df)) * 100
        print(f"  ✓ Matched {matches:,} / {len(merged_df):,} entries ({match_rate:.1f}%)")
    else:
        print(f"  Warning: Could not find audio feature columns to verify matches")

    # Clean up temporary matching columns
    merged_df = merged_df.drop(columns=['track_name_clean', 'artist_clean'], errors='ignore')

    return merged_df


def save_results(merged_df, output_file='data/merged_charts_with_audio.csv'):
    """Save merged results and print statistics."""
    # Save full merged dataset
    merged_df.to_csv(output_file, index=False)
    print(f"\n{'='*70}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*70}")

    # Print statistics
    print(f"\nDataset Statistics:")
    print(f"  Total chart entries: {len(merged_df):,}")
    print(f"  Unique tracks: {merged_df['track_id'].nunique():,}")

    # Check which audio features are available
    audio_features = []
    for feature in ['danceability', 'energy', 'valence', 'tempo', 'loudness',
                    'acousticness', 'instrumentalness', 'liveness', 'speechiness']:
        # Check both lowercase and capitalized versions
        if feature in merged_df.columns:
            audio_features.append(feature)
        elif feature.capitalize() in merged_df.columns:
            audio_features.append(feature.capitalize())

    if audio_features:
        print(f"\nAudio Features Available:")
        for feature in audio_features:
            present = merged_df[feature].notna().sum()
            percentage = (present / len(merged_df)) * 100
            print(f"  {feature}: {present:,} tracks ({percentage:.1f}%)")
    else:
        print("\n  Warning: No audio features found in merged dataset")

    # Show sample of merged data
    if audio_features:
        print(f"\nSample of merged data:")
        sample_cols = ['name', 'artists', 'streams'] + audio_features[:3]
        # Only use columns that exist
        sample_cols = [col for col in sample_cols if col in merged_df.columns]
        print(merged_df[sample_cols].head(10).to_string())

    return merged_df


def main(limit=10, full_run=False):
    """Main function to merge datasets."""
    print("="*70)
    print("Spotify Charts + Audio Features Merge Pipeline")
    print("="*70)

    # Load datasets
    charts_df = load_kaggle_charts(limit=None if full_run else limit)
    music_df = load_spotify_music_dataset()

    if music_df is None:
        return None

    # Merge
    merged_df = merge_datasets(charts_df, music_df)

    if merged_df is None:
        return None

    # Save and report
    output_file = 'data/merged_charts_with_audio_full.csv' if full_run else 'data/merged_charts_with_audio_test.csv'
    result = save_results(merged_df, output_file)

    print(f"\n{'='*70}")
    if full_run:
        print("✓ Full merge complete!")
    else:
        print("✓ Test merge complete!")
        print("\nTo process all tracks, run:")
        print("  python merge_spotify_music_dataset.py --full")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    import sys

    # Check for --full flag
    if '--full' in sys.argv:
        result = main(full_run=True)
    else:
        print("\nTesting with 10 unique tracks...")
        print("(Use --full flag to process all tracks)\n")
        result = main(limit=10, full_run=False)
