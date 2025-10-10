# 🎵 Akorlar Backend API Testing Guide for Postman

## 📋 **Base Configuration**

### **Base URL**
```
http://localhost:8000
```

### **Headers for JSON requests**
```
Content-Type: application/json
Accept: application/json
```

### **Headers for HTML browsable API**
```
Accept: text/html
```

---

## 🔓 **Public API Endpoints (No Authentication Required)**

### **1. Songs API**
```bash
# Get all songs
GET http://localhost:8000/api/songs/

# Get songs with filters
GET http://localhost:8000/api/songs/?difficulty=beginner
GET http://localhost:8000/api/songs/?genre=Pop
GET http://localhost:8000/api/songs/?is_popular=true
GET http://localhost:8000/api/songs/?chords_available=true

# Get specific song
GET http://localhost:8000/api/songs/{id}/

# Get popular songs
GET http://localhost:8000/api/songs/popular/

# Search songs
GET http://localhost:8000/api/songs/search/?q=love&genre=Pop&difficulty=beginner

# Get chords for a song
GET http://localhost:8000/api/songs/{id}/chords/
```

### **2. Artists API**
```bash
# Get all artists
GET http://localhost:8000/api/artists/

# Get artists with filters
GET http://localhost:8000/api/artists/?country=Turkey
GET http://localhost:8000/api/artists/?search=Sezen

# Get specific artist
GET http://localhost:8000/api/artists/{id}/
```

### **3. Genres API**
```bash
# Get all genres
GET http://localhost:8000/api/genres/

# Get specific genre
GET http://localhost:8000/api/genres/{id}/
```

### **4. Chords API**
```bash
# Get all chords
GET http://localhost:8000/api/chords/

# Get chords with filters
GET http://localhost:8000/api/chords/?root=C
GET http://localhost:8000/api/chords/?quality=major
GET http://localhost:8000/api/chords/?song=1
GET http://localhost:8000/api/chords/?measure=1
GET http://localhost:8000/api/chords/?key_context=C

# Get specific chord
GET http://localhost:8000/api/chords/{id}/
```

### **5. Chord Diagrams API**
```bash
# Get all chord diagrams
GET http://localhost:8000/api/chord-diagrams/

# Get chord diagrams with filters
GET http://localhost:8000/api/chord-diagrams/?instrument=guitar
GET http://localhost:8000/api/chord-diagrams/?difficulty=beginner
GET http://localhost:8000/api/chord-diagrams/?tuning=standard
GET http://localhost:8000/api/chord-diagrams/?capo_friendly=true

# Get specific chord diagram
GET http://localhost:8000/api/chord-diagrams/{id}/
```

### **6. Song Requests API**
```bash
# Get all song requests
GET http://localhost:8000/api/song-requests/

# Get specific song request
GET http://localhost:8000/api/song-requests/{id}/

# Create new song request
POST http://localhost:8000/api/song-requests/
Content-Type: application/json

{
    "title": "Test Song Request",
    "artist_name": "Test Artist",
    "genre_name": "Pop",
    "user_name": "Test User",
    "user_email": "test@example.com",
    "message": "Please add this song",
    "priority": "medium"
}
```

---

## 🔐 **Admin API Endpoints (Authentication Required)**

### **Authentication Setup**
First, you need to create a superuser and get authentication token:

```bash
# Create superuser (run in terminal)
cd /Users/nile/Projects/akorlar/backend
source venv/bin/activate
python manage.py createsuperuser

# Get authentication token (if using token auth)
POST http://localhost:8000/api-auth/login/
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

### **Admin Headers**
```
Authorization: Token your_token_here
# OR for session auth:
# Cookie: sessionid=your_session_id
```

### **1. Admin Songs API**
```bash
# Get all songs (admin view)
GET http://localhost:8000/api/admin/songs/

# Create new song
POST http://localhost:8000/api/admin/songs/
Content-Type: application/json

{
    "title": "New Test Song",
    "artist": 1,
    "genre": 1,
    "key": "C",
    "difficulty": "beginner",
    "year": 2024,
    "lyrics": "Test lyrics here",
    "chords_available": true,
    "tabs_available": false,
    "is_popular": false,
    "time_signature": "4/4",
    "duration": "03:30"
}

# Update song
PUT http://localhost:8000/api/admin/songs/{id}/
PATCH http://localhost:8000/api/admin/songs/{id}/

# Delete song
DELETE http://localhost:8000/api/admin/songs/{id}/

# Bulk create songs
POST http://localhost:8000/api/admin/songs/bulk_create/
Content-Type: application/json

{
    "songs": [
        {
            "title": "Song 1",
            "artist_name": "Artist 1",
            "genre_name": "Pop",
            "key": "C",
            "difficulty": "beginner"
        },
        {
            "title": "Song 2", 
            "artist_name": "Artist 2",
            "genre_name": "Rock",
            "key": "G",
            "difficulty": "intermediate"
        }
    ]
}
```

### **2. Admin Artists API**
```bash
# Get all artists (admin view)
GET http://localhost:8000/api/admin/artists/

# Create new artist
POST http://localhost:8000/api/admin/artists/
Content-Type: application/json

{
    "name": "New Test Artist",
    "bio": "Test artist bio",
    "country": "Turkey",
    "birth_date": "1990-01-01",
    "image": "https://example.com/image.jpg",
    "website": "https://example.com"
}

# Update artist
PUT http://localhost:8000/api/admin/artists/{id}/
PATCH http://localhost:8000/api/admin/artists/{id}/

# Delete artist
DELETE http://localhost:8000/api/admin/artists/{id}/
```

### **3. Admin Genres API**
```bash
# Get all genres (admin view)
GET http://localhost:8000/api/admin/genres/

# Create new genre
POST http://localhost:8000/api/admin/genres/
Content-Type: application/json

{
    "name": "New Test Genre",
    "description": "Test genre description",
    "color": "#FF5733"
}

# Update genre
PUT http://localhost:8000/api/admin/genres/{id}/
PATCH http://localhost:8000/api/admin/genres/{id}/

# Delete genre
DELETE http://localhost:8000/api/admin/genres/{id}/
```

### **4. Admin Chord Diagrams API**
```bash
# Get all chord diagrams (admin view)
GET http://localhost:8000/api/admin/chord-diagrams/

# Create new chord diagram
POST http://localhost:8000/api/admin/chord-diagrams/
Content-Type: application/json

{
    "chord_name": "Cmaj7",
    "alternative_name": "C Major 7th",
    "tuning": "standard",
    "difficulty": "intermediate",
    "instrument": "guitar",
    "capo_friendly": true,
    "fret_positions": [0, 3, 2, 0, 1, 0],
    "finger_positions": [0, 3, 2, 0, 1, 0],
    "notes": "C-E-G-B"
}

# Update chord diagram
PUT http://localhost:8000/api/admin/chord-diagrams/{id}/
PATCH http://localhost:8000/api/admin/chord-diagrams/{id}/

# Delete chord diagram
DELETE http://localhost:8000/api/admin/chord-diagrams/{id}/
```

### **5. Admin Song Requests API**
```bash
# Get all song requests (admin view)
GET http://localhost:8000/api/admin/song-requests/

# Update song request status
PATCH http://localhost:8000/api/admin/song-requests/{id}/
Content-Type: application/json

{
    "status": "approved",
    "admin_notes": "Great suggestion!"
}

# Delete song request
DELETE http://localhost:8000/api/admin/song-requests/{id}/
```

---

## 🧪 **Testing Workflow**

### **Step 1: Test Public Endpoints**
1. Start with basic GET requests to verify data is available
2. Test filtering parameters
3. Test search functionality
4. Test specific resource retrieval

### **Step 2: Test Authentication**
1. Create superuser account
2. Test login endpoint
3. Verify token/session authentication

### **Step 3: Test Admin Endpoints**
1. Test GET requests with authentication
2. Test POST requests to create new resources
3. Test PUT/PATCH requests to update resources
4. Test DELETE requests to remove resources
5. Test bulk operations

### **Step 4: Test Error Handling**
1. Test with invalid IDs (404 errors)
2. Test with missing required fields (400 errors)
3. Test with invalid data types (400 errors)
4. Test without authentication (403 errors)

---

## 📊 **Expected Response Formats**

### **Success Response (200/201)**
```json
{
    "id": 1,
    "title": "Example Song",
    "artist": {
        "id": 1,
        "name": "Example Artist"
    },
    "genre": {
        "id": 1,
        "name": "Pop"
    },
    "created_at": "2024-01-01T00:00:00Z"
}
```

### **Error Response (400/403/404)**
```json
{
    "error": "Error message",
    "detail": "Detailed error information"
}
```

### **List Response (200)**
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/songs/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## 🚀 **Quick Test Commands**

### **Test if server is running**
```bash
curl http://localhost:8000/
```

### **Test basic API**
```bash
curl http://localhost:8000/api/songs/
```

### **Test with filters**
```bash
curl "http://localhost:8000/api/songs/?difficulty=beginner&is_popular=true"
```

### **Test HTML interface**
```bash
curl -H "Accept: text/html" http://localhost:8000/api/songs/
```

---

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **500 Internal Server Error**: Check Django server logs
2. **403 Forbidden**: Authentication required for admin endpoints
3. **404 Not Found**: Check URL path and resource ID
4. **400 Bad Request**: Check request body format and required fields

### **Debug Steps:**
1. Check Django server is running on port 8000
2. Verify database has data (run seeds if needed)
3. Check authentication for admin endpoints
4. Verify request headers and body format
5. Check Django logs for detailed error messages

---

## 📝 **Notes**

- All timestamps are in ISO 8601 format
- Pagination is enabled for list endpoints
- Filtering is case-insensitive for text fields
- Boolean filters accept: `true`, `false`, `1`, `0`
- Date filters accept ISO format: `2024-01-01`
- Search is available on most text fields
- Ordering is supported on most list endpoints

