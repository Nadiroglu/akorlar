#!/usr/bin/env python3
"""
Simple API testing script for Akorlar backend
Run this to test all endpoints before using Postman
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def test_endpoint(method, url, data=None, headers=None, description=""):
    """Test a single endpoint and print results"""
    print(f"\n{'='*60}")
    print(f"Testing: {method} {url}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                if isinstance(json_data, list):
                    print(f"Response: List with {len(json_data)} items")
                    if json_data:
                        print(f"First item keys: {list(json_data[0].keys()) if json_data[0] else 'Empty'}")
                elif isinstance(json_data, dict):
                    print(f"Response: Dict with keys: {list(json_data.keys())}")
                else:
                    print(f"Response: {type(json_data)}")
            except:
                print(f"Response (text): {response.text[:200]}...")
        else:
            print(f"Error Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("🎵 Akorlar Backend API Testing")
    print("=" * 60)
    
    # Test basic connectivity
    test_endpoint('GET', f"{BASE_URL}/", description="Basic connectivity test")
    
    # Test public API endpoints
    print("\n🔓 Testing Public API Endpoints")
    
    test_endpoint('GET', f"{BASE_URL}/api/songs/", description="Get all songs")
    test_endpoint('GET', f"{BASE_URL}/api/songs/?difficulty=beginner", description="Get songs filtered by difficulty")
    test_endpoint('GET', f"{BASE_URL}/api/songs/?is_popular=true", description="Get popular songs")
    test_endpoint('GET', f"{BASE_URL}/api/songs/1/", description="Get specific song")
    
    test_endpoint('GET', f"{BASE_URL}/api/artists/", description="Get all artists")
    test_endpoint('GET', f"{BASE_URL}/api/artists/?country=Turkey", description="Get artists by country")
    
    test_endpoint('GET', f"{BASE_URL}/api/genres/", description="Get all genres")
    
    test_endpoint('GET', f"{BASE_URL}/api/chords/", description="Get all chords")
    test_endpoint('GET', f"{BASE_URL}/api/chords/?root=C", description="Get chords by root note")
    test_endpoint('GET', f"{BASE_URL}/api/chords/?quality=major", description="Get chords by quality")
    
    test_endpoint('GET', f"{BASE_URL}/api/chord-diagrams/", description="Get all chord diagrams")
    test_endpoint('GET', f"{BASE_URL}/api/chord-diagrams/?instrument=guitar", description="Get guitar chord diagrams")
    
    test_endpoint('GET', f"{BASE_URL}/api/song-requests/", description="Get all song requests")
    
    # Test song request creation
    song_request_data = {
        "title": "Test Song Request",
        "artist_name": "Test Artist",
        "genre_name": "Pop",
        "user_name": "Test User",
        "user_email": "test@example.com",
        "message": "Please add this song for testing",
        "priority": "medium"
    }
    test_endpoint('POST', f"{BASE_URL}/api/song-requests/", 
                 data=song_request_data, 
                 description="Create new song request")
    
    # Test admin endpoints (these will likely fail without proper auth)
    print("\n🔐 Testing Admin API Endpoints (Expected to fail without auth)")
    
    test_endpoint('GET', f"{BASE_URL}/api/admin/songs/", description="Get admin songs (should fail)")
    test_endpoint('GET', f"{BASE_URL}/api/admin/artists/", description="Get admin artists (should fail)")
    test_endpoint('GET', f"{BASE_URL}/api/admin/genres/", description="Get admin genres (should fail)")
    
    # Test HTML browsable API
    print("\n🌐 Testing HTML Browsable API")
    headers = {"Accept": "text/html"}
    test_endpoint('GET', f"{BASE_URL}/api/songs/", headers=headers, description="HTML browsable API")
    
    print("\n✅ API Testing Complete!")
    print("\nNext steps:")
    print("1. Use the POSTMAN_TESTING_GUIDE.md for detailed Postman testing")
    print("2. For admin endpoints, you'll need to authenticate first")
    print("3. Check the Django admin at http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
