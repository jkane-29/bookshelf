#!/usr/bin/env python3
"""Helper to find back cover images for your books"""

import json
import webbrowser
import urllib.parse

# Read books
with open('books.json', 'r') as f:
    data = json.load(f)
    books = data['books']

print("📚 Back Cover Finder")
print("=" * 60)
print("\nThis will open Google Images searches for each book's back cover.")
print("Download the image and save it with the suggested filename.\n")

for idx, book in enumerate(books, 1):
    title = book['title']
    author = book['author']
    
    # Suggested filename
    filename = title.replace(' ', '_').replace(',', '').replace(':', '').replace('?', '').replace("'", '')
    suggested_name = f"covers/{filename}_Back.jpg"
    
    print(f"\n{idx}. {title} — {author}")
    print(f"   Save as: {suggested_name}")
    
    # Create Google Images search URL for back cover
    search_query = f'"{title}" {author} book back cover'
    google_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(search_query)}"
    
    print(f"   Search: {google_url}")
    
    # Ask user if they want to open this search
    if idx == 1:
        response = input("\n   Open this search in browser? (y/n/all): ").lower()
        if response == 'all':
            open_all = True
            webbrowser.open(google_url)
        elif response == 'y':
            open_all = False
            webbrowser.open(google_url)
        else:
            open_all = False
    elif open_all:
        webbrowser.open(google_url)
    else:
        response = input("   Open search? (y/n): ").lower()
        if response == 'y':
            webbrowser.open(google_url)
    
    # Wait for user before continuing
    if idx < len(books):
        input("\n   Press Enter for next book...")
    else:
        print("\n" + "=" * 60)
        print("All done! Update books.json with back_cover paths:")
        print('  "back_cover": "covers/Book_Title_Back.jpg"')
        print("\nThen run: python3 generate_bookshelf.py")

