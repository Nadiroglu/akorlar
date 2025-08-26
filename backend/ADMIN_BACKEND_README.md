# 🔧 Admin Backend for Song Management

This document describes the flexible backend logic for admin functionality that enables adding new songs on demand and handling user song requests.

## 🏗️ **Architecture Overview**

The admin backend consists of two main components:
1. **Admin Management Views** - For staff to manage songs, artists, genres, and chord diagrams
2. **Song Request System** - For users to request new songs and admins to process them

## 📁 **File Structure**

```
backend/api/
├── views/
│   ├── admin.py              # Admin management viewsets
│   ├── song_request.py       # Song request handling
│   └── __init__.py           # Updated index
├── serializers/
│   ├── song_request.py       # Song request serializers
│   └── __init__.py           # Updated index
├── models.py                 # Updated with SongRequest model
├── admin.py                  # Django admin configuration
└── urls.py                   # Updated routing
```

## 🎵 **Admin Song Management Features**

### **AdminSongViewSet**
- **Full CRUD operations** for songs
- **Bulk song creation** with automatic artist/genre creation
- **Chord management** - Add chord progressions to songs
- **Popularity toggle** - Mark songs as popular/unpopular
- **Statistics dashboard** - Song counts, genre distribution, difficulty stats

### **Key Endpoints:**
```
POST /api/admin/songs/                    # Create new song
PUT /api/admin/songs/{id}/                # Update song
DELETE /api/admin/songs/{id}/             # Delete song
POST /api/admin/songs/bulk_create/        # Bulk create songs
POST /api/admin/songs/{id}/add_chords/    # Add chords to song
POST /api/admin/songs/{id}/toggle_popular/ # Toggle popularity
GET /api/admin/songs/stats/               # Get statistics
```

### **Bulk Song Creation Example:**
```json
POST /api/admin/songs/bulk_create/
{
  "songs": [
    {
      "title": "Yeni Şarkı",
      "artist_name": "Yeni Sanatçı",
      "genre_name": "Pop",
      "difficulty": "intermediate",
      "key": "C",
      "tempo": 120,
      "chords_available": true
    }
  ]
}
```

## 📝 **Song Request System**

### **User Features:**
- **Submit song requests** without authentication
- **Email confirmation** upon submission
- **Request tracking** with unique ID
- **Rate limiting** (max 5 requests per week per email)

### **Admin Features:**
- **Review and approve/reject** requests
- **Link completed songs** to requests
- **Email notifications** to users on status changes
- **Bulk actions** (approve/reject multiple requests)
- **Statistics dashboard** for request analytics

### **Request Workflow:**
1. User submits request → Status: `pending`
2. Admin reviews → Status: `approved` or `rejected`
3. Admin creates song → Links to request → Status: `completed`
4. User receives email notification

### **Key Endpoints:**
```
# Public endpoints
POST /api/song-requests/                  # Submit request
GET /api/song-requests/{id}/              # Check request status

# Admin endpoints
GET /api/admin/song-requests/             # List all requests
PUT /api/admin/song-requests/{id}/        # Update request
POST /api/admin/song-requests/{id}/approve/    # Approve request
POST /api/admin/song-requests/{id}/reject/     # Reject request
POST /api/admin/song-requests/{id}/complete/   # Mark as completed
GET /api/admin/song-requests/stats/       # Request statistics
```

## 🔐 **Security & Permissions**

### **Admin Views:**
- **IsAdminUser permission** - Only staff users can access
- **Session authentication** required
- **CSRF protection** enabled

### **Public Views:**
- **Song request creation** - No authentication required
- **Rate limiting** by email address
- **Input validation** and sanitization

## 📧 **Email Notifications**

### **User Emails:**
- **Confirmation** upon request submission
- **Status updates** when request is approved/rejected/completed

### **Admin Emails:**
- **New request notifications** with request details
- **Admin dashboard links** for quick access

### **Email Configuration:**
```python
# In .env file
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@turkishmusic.com
ADMIN_EMAIL=admin@turkishmusic.com
SITE_URL=http://localhost:8000
```

## 🎛️ **Django Admin Interface**

### **Song Management:**
- **List view** with filters and search
- **Inline editing** for popular status and features
- **Organized fieldsets** for better UX
- **Bulk actions** for multiple songs

### **Song Request Management:**
- **Status tracking** with color coding
- **Days since request** calculation
- **Bulk approve/reject** actions
- **Linked song management**

## 🚀 **Setup Instructions**

### **1. Install Dependencies:**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **3. Create Superuser:**
```bash
python manage.py createsuperuser
```

### **4. Configure Email (Optional):**
Add email settings to `.env` file for notifications

### **5. Test Admin Interface:**
Visit `/admin/` and log in with superuser credentials

## 📊 **API Usage Examples**

### **Create Song via Admin API:**
```bash
curl -X POST http://localhost:8000/api/admin/songs/ \
  -H "Authorization: Session <session_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Song",
    "artist": 1,
    "genre": 1,
    "difficulty": "beginner",
    "key": "C",
    "tempo": 120
  }'
```

### **Submit Song Request:**
```bash
curl -X POST http://localhost:8000/api/song-requests/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Requested Song",
    "artist_name": "Artist Name",
    "genre_name": "Pop",
    "user_email": "user@example.com",
    "user_name": "User Name",
    "additional_notes": "Please add this song"
  }'
```

### **Approve Song Request:**
```bash
curl -X POST http://localhost:8000/api/admin/song-requests/1/approve/ \
  -H "Authorization: Session <session_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "admin_notes": "Great song, will add soon"
  }'
```

## 🔍 **Monitoring & Analytics**

### **Admin Dashboard Statistics:**
- **Song counts** by genre, difficulty, features
- **Request counts** by status, time period
- **User engagement** metrics
- **Popular content** tracking

### **Request Analytics:**
- **Pending requests** count
- **Processing time** averages
- **Genre preferences** from requests
- **User request patterns**

## 🛠️ **Customization Options**

### **Adding New Admin Features:**
1. Create new ViewSet in `views/admin.py`
2. Add serializer in appropriate serializer file
3. Register in `views/__init__.py`
4. Add URL routing in `urls.py`
5. Configure admin interface in `admin.py`

### **Extending Song Request System:**
1. Add new fields to `SongRequest` model
2. Update serializers for new fields
3. Modify email templates
4. Add new status options if needed

## 🚨 **Troubleshooting**

### **Common Issues:**
- **Email not sending**: Check SMTP configuration
- **Permission denied**: Ensure user has staff status
- **Migration errors**: Check model field changes
- **API 404**: Verify URL routing configuration

### **Debug Mode:**
Set `DEBUG = True` in settings for detailed error messages

## 🔮 **Future Enhancements**

### **Planned Features:**
- **Automated song creation** from approved requests
- **Bulk import** from CSV/Excel files
- **Advanced analytics** dashboard
- **API rate limiting** for admin endpoints
- **Webhook notifications** for external systems

### **Integration Points:**
- **Music notation software** APIs
- **Audio file management** system
- **User feedback** collection
- **Social media** sharing features

---

**🎵 This admin backend provides a robust foundation for managing Turkish music content and handling user requests efficiently!**
