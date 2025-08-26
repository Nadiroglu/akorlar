# 🌱 Database Seed Files

This directory contains separate seed files for each model to populate your database with sample data.

## 📁 **Seed Files Structure**

- **`seeds_genre.py`** - Turkish music genres
- **`seeds_artist.py`** - Famous Turkish musicians
- **`seeds_song.py`** - Popular Turkish songs with metadata
- **`seeds_chord.py`** - Chord progressions for songs
- **`seeds_chord_diagram.py`** - Guitar chord diagrams
- **`seeds_search_query.py`** - Sample search analytics
- **`seeds_master.py`** - Master file that runs all seeds in order

## 🚀 **How to Use**

### **Option 1: Run Master Seed File (Recommended)**
```bash
cd backend
python manage.py shell < api/seeds_master.py
```

### **Option 2: Run Individual Seed Files**
```bash
cd backend

# Run in order (due to dependencies):
python manage.py shell < api/seeds_genre.py
python manage.py shell < api/seeds_artist.py
python manage.py shell < api/seeds_song.py
python manage.py shell < api/seeds_chord_diagram.py
python manage.py shell < api/seeds_chord.py
python manage.py shell < api/seeds_search_query.py
```

### **Option 3: Run from Django Shell**
```bash
cd backend
python manage.py shell

# Then in the shell:
from api.seeds_genre import seed_genres
from api.seeds_artist import seed_artists
from api.seeds_song import seed_songs
from api.seeds_chord_diagram import seed_chord_diagrams
from api.seeds_chord import seed_chords
from api.seeds_search_query import seed_search_queries

# Run them:
seed_genres()
seed_artists()
seed_songs()
seed_chord_diagrams()
seed_chords()
seed_search_queries()
```

## 📊 **Data Included**

### **Genres (8)**
- Türk Halk Müziği (Turkish Folk Music)
- Türk Sanat Müziği (Turkish Art Music)
- Arabesk
- Pop, Rock, Jazz, Blues, Country

### **Artists (8)**
- Barış Manço, Sezen Aksu, Tarkan
- Erkan Oğur, Müzeyyen Senar
- Neşet Ertaş, Ahmet Kaya, Zeki Müren

### **Songs (6)**
- Dağlar Dağlar, Gül Pembe, Şımarık
- Kuzu Kuzu, Neredesin Sen, Çoban

### **Chords (12)**
- Chord progressions for 3 songs
- 4 chords per song (Am-F-C-G, C-Am-F-G, G-Em-C-D)

### **Chord Diagrams (10)**
- Common guitar chords: C, G, Am, F, D, Em, Bm, A, E, Dm
- Standard EADGBE tuning
- Fret positions and fingerings

### **Search Queries (100)**
- Sample search analytics over 30 days
- Random search terms and timestamps

## ⚠️ **Important Notes**

1. **Dependencies**: Run seeds in order due to foreign key relationships
2. **Idempotent**: Seeds use `get_or_create` - safe to run multiple times
3. **Sample Data**: This is demo data - replace with real data in production
4. **Database**: Ensure your database is migrated before running seeds

## 🔧 **Customization**

To add your own data:
1. Edit the respective seed file
2. Modify the data arrays
3. Run the seed file again

## 🧪 **Testing**

After seeding, test your API endpoints:
```bash
# Test genres
curl http://localhost:8000/api/genres/

# Test songs
curl http://localhost:8000/api/songs/

# Test popular songs
curl http://localhost:8000/api/songs/popular/
```

## 📝 **Troubleshooting**

- **Import Errors**: Ensure you're in the correct directory
- **Model Errors**: Run migrations first: `python manage.py migrate`
- **Database Errors**: Check your database connection in `.env`
- **Permission Errors**: Ensure Django can write to the database

---

**Happy Seeding! 🌱🎵**
