"""
Merge Kaggle Charts with Hugging Face Audio Features Dataset
Simple left join on track_id to combine chart data with audio features.
"""

import pandas as pd
from datasets import load_dataset
import time


def load_huggingface_audio_features():
    """Download and load the Spotify audio features dataset from Hugging Face."""
    print("Downloading Spotify audio features from Hugging Face...")
    print("(This may take a minute on first run...)\n")

    dataset = load_dataset("maharshipandya/spotify-tracks-dataset")
    audio_df = pd.DataFrame(dataset['train'])

    print(f"✓ Loaded {len(audio_df):,} tracks with audio features")
    print(f"  Columns: {list(audio_df.columns)}\n")

    return audio_df


def load_charts_data(limit=None):
    """Load the Kaggle charts dataset."""
    print("Loading Kaggle charts data...")

    charts_df = pd.read_csv('data/charts.csv')

    if limit:
        # Get first N unique track IDs for testing
        unique_track_ids = charts_df['track_id'].unique()[:limit]
        charts_df = charts_df[charts_df['track_id'].isin(unique_track_ids)]

    print(f"✓ Loaded {len(charts_df):,} chart entries")
    print(f"  Unique tracks: {charts_df['track_id'].nunique():,}\n")

    return charts_df


def merge_on_track_id(charts_df, audio_df):
    """Perform left join on track_id."""
    print("Merging datasets on track_id...")

    # Left join: keep all chart entries, add audio features where available
    merged_df = pd.merge(
        charts_df,
        audio_df,
        on='track_id',
        how='left',
        suffixes=('_chart', '_audio')
    )

    # Calculate match statistics
    total_entries = len(merged_df)
    matched_entries = merged_df['danceability'].notna().sum()
    match_rate = (matched_entries / total_entries) * 100

    unique_tracks = merged_df['track_id'].nunique()
    unique_matched = merged_df[merged_df['danceability'].notna()]['track_id'].nunique()
    unique_match_rate = (unique_matched / unique_tracks) * 100

    print(f"✓ Merge complete!\n")
    print(f"Match Statistics:")
    print(f"  Total chart entries: {total_entries:,}")
    print(f"  Entries with audio features: {matched_entries:,} ({match_rate:.1f}%)")
    print(f"  Unique tracks: {unique_tracks:,}")
    print(f"  Unique tracks with audio features: {unique_matched:,} ({unique_match_rate:.1f}%)\n")

    return merged_df


def save_results(merged_df, test_mode=True):
    """Save the merged dataset and display summary."""
    output_file = 'data/charts_with_audio_test.csv' if test_mode else 'data/charts_with_audio_full.csv'

    merged_df.to_csv(output_file, index=False)

    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*70}\n")

    # Show audio feature coverage
    audio_features = [
        'danceability', 'energy', 'valence', 'tempo', 'loudness',
        'acousticness', 'instrumentalness', 'liveness', 'speechiness'
    ]

    print("Audio Feature Coverage:")
    for feature in audio_features:
        if feature in merged_df.columns:
            available = merged_df[feature].notna().sum()
            percentage = (available / len(merged_df)) * 100
            print(f"  {feature:20s}: {available:6,} / {len(merged_df):6,} ({percentage:5.1f}%)")

    # Show sample of matched data
    matched_df = merged_df[merged_df['danceability'].notna()]
    if not matched_df.empty:
        print(f"\nSample of merged data with audio features:")
        sample_cols = ['date', 'name', 'artists_chart', 'streams', 'danceability', 'energy', 'valence']
        available_cols = [col for col in sample_cols if col in matched_df.columns]
        print(matched_df[available_cols].head(10).to_string(index=False))

    return output_file


def main(test_mode=True, limit=10):
    """Main pipeline function."""
    start_time = time.time()

    print("="*70)
    print("Spotify Charts + Audio Features Merge Pipeline")
    print("="*70)
    print()

    if test_mode:
        print(f"TEST MODE: Processing first {limit} unique tracks\n")
    else:
        print("FULL MODE: Processing all tracks\n")

    # Load datasets
    audio_df = load_huggingface_audio_features()
    charts_df = load_charts_data(limit=limit if test_mode else None)

    # Merge on track_id
    merged_df = merge_on_track_id(charts_df, audio_df)

    # Save results
    output_file = save_results(merged_df, test_mode=test_mode)

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"✓ Pipeline complete in {elapsed:.1f} seconds!")
    print(f"{'='*70}")

    if test_mode:
        print("\nTo process ALL tracks, run:")
        print("  micromamba run -n seasons-of-sound python merge_charts_with_audio.py --full")

    return merged_df


if __name__ == "__main__":
    import sys

    if '--full' in sys.argv:
        result = main(test_mode=False)
    else:
        result = main(test_mode=True, limit=10)
