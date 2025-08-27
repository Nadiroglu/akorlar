# WSL Commands for Akorlar Backend Setup

## 🚀 **Quick Setup (Recommended)**

```bash
# Navigate to backend directory
cd backend

# Make the setup script executable
chmod +x setup_wsl.sh

# Run the complete setup
./setup_wsl.sh
```

## 🔧 **Manual Setup (Step by Step)**

### 1. **Navigate to Backend Directory**
```bash
cd backend
```

### 2. **Activate Virtual Environment**
```bash
source venv/bin/activate
```

### 3. **Install Dependencies (if needed)**
```bash
pip install -r requirements.txt
```

### 4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **Run Master Seeds**
```bash
python run_seeds.py
```

### 6. **Start Django Server**
```bash
python manage.py runserver
```

## 🌱 **Individual Seed Files (if needed)**

If you want to run seeds individually:

```bash
# Genres
python manage.py shell < api/seeds/seeds_genre.py

# Artists  
python manage.py shell < api/seeds/seeds_artist.py

# Songs
python manage.py shell < api/seeds/seeds_song.py

# Chord Diagrams
python manage.py shell < api/seeds/seeds_chord_diagram.py

# Chords
python manage.py shell < api/seeds/seeds_chord.py

# Search Queries
python manage.py shell < api/seeds/seeds_search_query.py
```

## 🎯 **What Will Be Created**

- **20+ Genres**: Pop, Rock, Folk, Jazz, Classical, Türk Halk Müziği, Arabesk, etc.
- **20 Artists**: Barış Manço, Sezen Aksu, Tarkan, Neşet Ertaş, etc.
- **20 Songs**: Dağlar Dağlar, Şımarık, Gül Pembe, etc.
- **25+ Chord Diagrams**: All major, minor, 7th chords with proper fingerings
- **Chord Progressions**: Each song with proper bar/beat positioning
- **Search Queries**: Sample search data for analytics

## 🔍 **Verify Setup**

After running the seeds, you can verify:

```bash
# Check Django admin
python manage.py createsuperuser  # Create admin user
python manage.py runserver         # Start server
# Visit http://localhost:8000/admin/

# Or check via shell
python manage.py shell
>>> from api.models import Song, Artist, Genre, Chord
>>> print(f"Songs: {Song.objects.count()}")
>>> print(f"Artists: {Artist.objects.count()}")
>>> print(f"Genres: {Genre.objects.count()}")
>>> print(f"Chords: {Chord.objects.count()}")
```

## 🚨 **Troubleshooting**

### **Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Database Issues**
```bash
# Reset database (WARNING: This will delete all data)
rm db.sqlite3
python manage.py migrate
python run_seeds.py
```

### **Permission Issues**
```bash
# Fix file permissions
chmod +x setup_wsl.sh
chmod +x run_seeds.py
```
