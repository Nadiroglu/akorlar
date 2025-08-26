# Akorlar Backend API

A Django REST API backend for the Akorlar Turkish music application.

## Features

- **Music Management**: Songs, artists, genres, and chords
- **User System**: Authentication, favorites, and history tracking
- **Advanced Search**: Filter by genre, difficulty, key, and more
- **RESTful API**: Full CRUD operations with proper serialization
- **PostgreSQL Database**: Robust and scalable database backend

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd akorlar/backend
```

### 2. Create virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

#### Create database and user:
```sql
CREATE DATABASE akorlar_db;
CREATE USER akorlar_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE akorlar_db TO akorlar_user;
```

#### Or use psql command line:
```bash
psql -U postgres
CREATE DATABASE akorlar_db;
CREATE USER akorlar_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE akorlar_db TO akorlar_user;
\q
```

### 5. Configure environment variables

Copy the `.env.example` file to `.env` and update the values:
```bash
cp .env.example .env
```

Edit `.env` file:
```env
# Database Configuration
DB_NAME=akorlar_db
DB_USER=akorlar_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
```

### 6. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Run the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

### Songs
- `GET /api/songs/` - List all songs
- `GET /api/songs/{id}/` - Get song details
- `GET /api/songs/popular/` - Get popular songs
- `GET /api/songs/search/?q=query` - Search songs
- `GET /api/songs/{id}/chords/` - Get chords for a song

### Artists
- `GET /api/artists/` - List all artists
- `GET /api/artists/{id}/` - Get artist details
- `GET /api/artists/{id}/songs/` - Get songs by artist

### Genres
- `GET /api/genres/` - List all genres
- `GET /api/genres/{id}/` - Get genre details
- `GET /api/genres/{id}/songs/` - Get songs by genre

### Chords
- `GET /api/chords/` - List all chords
- `GET /api/chords/{id}/` - Get chord details
- `GET /api/chord-diagrams/` - List chord diagrams

### User Features
- `GET /api/favorites/` - Get user favorites
- `POST /api/favorites/toggle/` - Toggle favorite status
- `GET /api/history/` - Get user history
- `POST /api/history/record/` - Record user action

## Database Models

### Core Models
- **Song**: Main music entity with metadata
- **Artist**: Performer information
- **Genre**: Music categorization
- **Chord**: Musical chord data
- **ChordDiagram**: Visual chord representations

### User Models
- **UserFavorite**: User's favorite songs
- **UserHistory**: User activity tracking
- **SearchQuery**: Search analytics

## Development

### Running tests
```bash
python manage.py test
```

### Creating migrations
```bash
python manage.py makemigrations api
```

### Applying migrations
```bash
python manage.py migrate
```

### Shell access
```bash
python manage.py shell
```

### Admin interface
Access Django admin at `http://localhost:8000/admin/`

## Configuration

### Environment Variables
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of CORS origins

### Database Settings
The application uses PostgreSQL with the following optimizations:
- Connection pooling
- Proper indexing on search fields
- JSON fields for complex data (chord diagrams)

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL/HTTPS
- [ ] Configure database connection pooling
- [ ] Set up static file serving
- [ ] Configure logging
- [ ] Set up monitoring

### Docker Support
```bash
docker build -t akorlar-backend .
docker run -p 8000:8000 akorlar-backend
```

## Support

For support and questions:
- Email: support@akorlar.com
- Documentation: [API Docs](http://localhost:8000/api/docs/)
- Issues: GitHub repository issues

## License

This project is licensed under the MIT License.
