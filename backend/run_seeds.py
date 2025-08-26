#!/usr/bin/env python
"""
Simple script to run the master seeds file
Run with: python run_seeds.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Import and run the master seeds
from api.seeds.seeds_master import run_all_seeds

if __name__ == "__main__":
    print("🚀 Starting database seeding...")
    success = run_all_seeds()
    
    if success:
        print("\n🎉 Database seeding completed successfully!")
        print("You can now test your API endpoints with real data.")
    else:
        print("\n💥 Seeding failed. Please check the error messages above.")
        sys.exit(1)
