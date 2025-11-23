"""
Spotify Data Pipeline
Fetches audio features and artist metadata for songs in the Kaggle dataset.
"""

import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Dict, List, Optional
import time


class SpotifyDataPipeline:
    def __init__(self):
        """Initialize Spotify API client with credentials from .env file."""
        load_dotenv()

        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise ValueError(
                "Missing Spotify credentials. Please set SPOTIFY_CLIENT_ID and "
                "SPOTIFY_CLIENT_SECRET in your .env file. "
                "Get credentials from https://developer.spotify.com/dashboard"
            )

        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_audio_features(self, track_id: str) -> Optional[Dict]:
        """
        Fetch audio features for a single track.

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary containing audio features or None if request fails
        """
        try:
            features = self.sp.audio_features([track_id])[0]
            if features:
                return {
                    'track_id': track_id,
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'valence': features['valence'],
                    'tempo': features['tempo'],
                    'loudness': features['loudness'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'speechiness': features['speechiness'],
                    'duration_ms': features['duration_ms'],
                    'key': features['key'],
                    'mode': features['mode'],
                    'time_signature': features['time_signature']
                }
        except Exception as e:
            print(f"Error fetching audio features for track {track_id}: {e}")
            return None

    def get_track_metadata(self, track_id: str) -> Optional[Dict]:
        """
        Fetch track metadata including release date and explicit flag.

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary containing track metadata or None if request fails
        """
        try:
            track = self.sp.track(track_id)
            return {
                'track_id': track_id,
                'release_date': track['album']['release_date'],
                'explicit': track['explicit']
            }
        except Exception as e:
            print(f"Error fetching track metadata for {track_id}: {e}")
            return None

    def get_artist_metadata(self, artist_ids: List[str]) -> List[Dict]:
        """
        Fetch artist metadata including popularity, followers, and genres.

        Args:
            artist_ids: List of Spotify artist IDs

        Returns:
            List of dictionaries containing artist metadata
        """
        artist_data = []
        try:
            # Spotify allows up to 50 artists per request
            for i in range(0, len(artist_ids), 50):
                batch = artist_ids[i:i+50]
                artists = self.sp.artists(batch)['artists']

                for artist in artists:
                    if artist:
                        artist_data.append({
                            'artist_id': artist['id'],
                            'artist_name': artist['name'],
                            'artist_popularity': artist['popularity'],
                            'artist_followers': artist['followers']['total'],
                            'artist_genres': ', '.join(artist['genres']) if artist['genres'] else ''
                        })

                # Rate limiting: small delay between batches
                if i + 50 < len(artist_ids):
                    time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching artist metadata: {e}")

        return artist_data

    def get_track_artist_ids(self, track_id: str) -> List[str]:
        """
        Get artist IDs associated with a track.

        Args:
            track_id: Spotify track ID

        Returns:
            List of artist IDs
        """
        try:
            track = self.sp.track(track_id)
            return [artist['id'] for artist in track['artists']]
        except Exception as e:
            print(f"Error fetching artist IDs for track {track_id}: {e}")
            return []

    def process_tracks(self, track_ids: List[str], output_prefix: str = 'spotify_data') -> pd.DataFrame:
        """
        Process multiple tracks and gather all required data.

        Args:
            track_ids: List of Spotify track IDs
            output_prefix: Prefix for output CSV files

        Returns:
            DataFrame containing combined track and artist data
        """
        print(f"Processing {len(track_ids)} tracks...")

        audio_features_list = []
        track_metadata_list = []
        all_artist_data = {}

        for idx, track_id in enumerate(track_ids, 1):
            print(f"Processing track {idx}/{len(track_ids)}: {track_id}")

            # Get audio features
            audio_features = self.get_audio_features(track_id)
            if audio_features:
                audio_features_list.append(audio_features)

            # Get track metadata
            track_metadata = self.get_track_metadata(track_id)
            if track_metadata:
                track_metadata_list.append(track_metadata)

            # Get artist IDs and metadata
            artist_ids = self.get_track_artist_ids(track_id)
            if artist_ids:
                # Fetch artist data for each artist if not already fetched
                for artist_id in artist_ids:
                    if artist_id not in all_artist_data:
                        artist_metadata = self.get_artist_metadata([artist_id])
                        if artist_metadata:
                            all_artist_data[artist_id] = artist_metadata[0]

            # Rate limiting
            time.sleep(0.1)

        # Create DataFrames
        audio_features_df = pd.DataFrame(audio_features_list)
        track_metadata_df = pd.DataFrame(track_metadata_list)
        artist_metadata_df = pd.DataFrame(list(all_artist_data.values()))

        # Save individual DataFrames
        audio_features_df.to_csv(f'{output_prefix}_audio_features.csv', index=False)
        track_metadata_df.to_csv(f'{output_prefix}_track_metadata.csv', index=False)
        artist_metadata_df.to_csv(f'{output_prefix}_artist_metadata.csv', index=False)

        print(f"\nData saved to:")
        print(f"  - {output_prefix}_audio_features.csv ({len(audio_features_df)} tracks)")
        print(f"  - {output_prefix}_track_metadata.csv ({len(track_metadata_df)} tracks)")
        print(f"  - {output_prefix}_artist_metadata.csv ({len(artist_metadata_df)} artists)")

        # Merge audio features and track metadata
        if not audio_features_df.empty and not track_metadata_df.empty:
            combined_df = pd.merge(audio_features_df, track_metadata_df, on='track_id', how='outer')
            combined_df.to_csv(f'{output_prefix}_combined.csv', index=False)
            print(f"  - {output_prefix}_combined.csv (combined track data)")
            return combined_df

        return audio_features_df


def main():
    """Main function to test the pipeline with 10 songs."""
    # Load the Kaggle dataset
    print("Loading Kaggle dataset...")
    df = pd.read_csv('data/charts.csv')

    # Get unique track IDs (limit to 10 for testing)
    unique_track_ids = df['track_id'].unique()[:10]

    print(f"\nFound {len(df['track_id'].unique())} unique tracks in dataset")
    print(f"Testing with first 10 tracks:\n")

    # Initialize pipeline
    pipeline = SpotifyDataPipeline()

    # Process tracks
    result_df = pipeline.process_tracks(unique_track_ids, output_prefix='data/spotify_test')

    print("\n✓ Pipeline test complete!")
    print(f"\nPreview of combined data:")
    print(result_df.head())


if __name__ == "__main__":
    main()
