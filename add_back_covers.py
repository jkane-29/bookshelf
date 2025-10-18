#!/usr/bin/env python3
"""Automatically add back_cover references to books.json for downloaded covers"""

import json
import os
import glob

# Read books
with open('books.json', 'r') as f:
    data = json.load(f)
    books = data['books']

# Find all back cover files
back_covers = glob.glob('covers/*_Back.jpg') + glob.glob('covers/*_Back.png')

print(f"Found {len(back_covers)} back cover images\n")

# Create a mapping of possible filenames to actual files
back_cover_map = {}
for bc in back_covers:
    # Extract the base name
    basename = os.path.basename(bc).replace('_Back.jpg', '').replace('_Back.png', '')
    back_cover_map[basename.lower()] = bc

updated_count = 0

# Update books with back covers
for book in books:
    title = book['title']
    # Generate expected filename
    filename = title.replace(' ', '_').replace(',', '').replace(':', '').replace('?', '').replace("'", '')
    
    # Check if we have a back cover for this book
    if filename.lower() in back_cover_map:
        book['back_cover'] = back_cover_map[filename.lower()]
        print(f"✓ Added back cover for: {title}")
        updated_count += 1
    elif 'back_cover' in book and book['back_cover'] and os.path.exists(book['back_cover']):
        print(f"✓ Already has back cover: {title}")
    else:
        print(f"  Missing back cover: {title}")

# Write updated books.json
with open('books.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Updated {updated_count} books with back covers")
print("Run: python3 generate_bookshelf.py")

