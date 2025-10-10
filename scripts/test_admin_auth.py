#!/usr/bin/env python3
"""
Admin authentication helper for testing admin endpoints
This script helps you get authentication tokens for admin API testing
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def get_admin_auth():
    """Get authentication for admin endpoints"""
    print("🔐 Admin Authentication Helper")
    print("=" * 50)
    
    # Test admin login
    login_url = f"{BASE_URL}/api-auth/login/"
    
    print("Testing admin login...")
    print(f"URL: {login_url}")
    print("Username: admin")
    print("Password: admin123")
    
    # Get CSRF token first
    session = requests.Session()
    
    # Get login page to extract CSRF token
    login_page = session.get(login_url)
    print(f"Login page status: {login_page.status_code}")
    
    if login_page.status_code == 200:
        print("✅ Login page accessible")
        print("\nTo authenticate in Postman:")
        print("1. Go to http://localhost:8000/api-auth/login/ in your browser")
        print("2. Login with username: admin, password: admin123")
        print("3. Copy the session cookie from browser dev tools")
        print("4. Use the cookie in Postman headers: Cookie: sessionid=your_session_id")
    else:
        print("❌ Login page not accessible")
    
    # Test Django admin
    admin_url = f"{BASE_URL}/admin/"
    admin_response = session.get(admin_url)
    print(f"\nDjango admin status: {admin_response.status_code}")
    
    if admin_response.status_code == 200:
        print("✅ Django admin accessible")
        print(f"Admin URL: {admin_url}")
    else:
        print("❌ Django admin not accessible")
    
    # Test admin API with session
    print("\nTesting admin API with session...")
    admin_songs_url = f"{BASE_URL}/api/admin/songs/"
    admin_response = session.get(admin_songs_url)
    print(f"Admin songs API status: {admin_response.status_code}")
    
    if admin_response.status_code == 200:
        print("✅ Admin API accessible with session")
        data = admin_response.json()
        print(f"Response: {len(data)} items")
    else:
        print("❌ Admin API requires authentication")
        print("Response:", admin_response.text[:200])

def test_with_basic_auth():
    """Test with basic authentication"""
    print("\n🔑 Testing Basic Authentication")
    print("=" * 50)
    
    # Test with basic auth
    auth = ('admin', 'admin123')
    admin_songs_url = f"{BASE_URL}/api/admin/songs/"
    
    response = requests.get(admin_songs_url, auth=auth)
    print(f"Basic auth status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Basic authentication works!")
        data = response.json()
        print(f"Response: {len(data)} items")
    else:
        print("❌ Basic authentication failed")
        print("Response:", response.text[:200])

def main():
    print("🎵 Akorlar Admin Authentication Testing")
    print("=" * 60)
    
    get_admin_auth()
    test_with_basic_auth()
    
    print("\n📋 Postman Setup Instructions:")
    print("=" * 50)
    print("1. For Session Authentication:")
    print("   - Visit http://localhost:8000/api-auth/login/ in browser")
    print("   - Login with admin/admin123")
    print("   - Copy sessionid cookie from browser dev tools")
    print("   - Add to Postman headers: Cookie: sessionid=your_session_id")
    print()
    print("2. For Basic Authentication:")
    print("   - In Postman, go to Authorization tab")
    print("   - Select 'Basic Auth'")
    print("   - Username: admin")
    print("   - Password: admin123")
    print()
    print("3. Test URLs:")
    print("   - GET http://localhost:8000/api/admin/songs/")
    print("   - GET http://localhost:8000/api/admin/artists/")
    print("   - GET http://localhost:8000/api/admin/genres/")
    print("   - GET http://localhost:8000/api/admin/chord-diagrams/")
    print("   - GET http://localhost:8000/api/admin/song-requests/")

if __name__ == "__main__":
    main()
