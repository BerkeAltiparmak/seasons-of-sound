"""
Test Spotify API authentication and permissions.
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print(f"Client ID: {client_id[:10]}..." if client_id else "No Client ID")
print(f"Client Secret: {client_secret[:10]}..." if client_secret else "No Client Secret")
print()

auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Test with a known track ID
test_track_id = "20IvMlpi4U5RuDnAlXSRiV"

print("Testing Spotify API access:")
print("=" * 50)

# Test 1: Track info
print("\n1. Testing track info endpoint...")
try:
    track = sp.track(test_track_id)
    print(f"   ✓ SUCCESS: Got track info for '{track['name']}'")
except Exception as e:
    print(f"   ✗ FAILED: {e}")

# Test 2: Artist info
print("\n2. Testing artist info endpoint...")
try:
    track = sp.track(test_track_id)
    artist_id = track['artists'][0]['id']
    artist = sp.artist(artist_id)
    print(f"   ✓ SUCCESS: Got artist info for '{artist['name']}'")
except Exception as e:
    print(f"   ✗ FAILED: {e}")

# Test 3: Audio features
print("\n3. Testing audio features endpoint...")
try:
    features = sp.audio_features([test_track_id])
    if features and features[0]:
        print(f"   ✓ SUCCESS: Got audio features")
        print(f"     - Danceability: {features[0]['danceability']}")
        print(f"     - Energy: {features[0]['energy']}")
        print(f"     - Valence: {features[0]['valence']}")
    else:
        print(f"   ✗ FAILED: Got None response")
except Exception as e:
    print(f"   ✗ FAILED: {e}")

print("\n" + "=" * 50)
