#!/usr/bin/env python3
"""Fetch book summaries from Open Library API"""

import json
import urllib.request
import urllib.parse
import time

# Read books
with open('books.json', 'r') as f:
    data = json.load(f)
    books = data['books']

def fetch_summary(title, author, isbn=None):
    """Fetch book summary from Open Library"""
    try:
        # Search for the book
        query = f"{title} {author}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://openlibrary.org/search.json?q={encoded_query}&limit=3"
        
        with urllib.request.urlopen(url) as response:
            search_data = json.loads(response.read())
        
        best_description = None
        max_length = 0
        
        if search_data.get('docs'):
            for doc in search_data['docs'][:3]:  # Try first 3 results
                # Try to get the work key to fetch full description
                if 'key' in doc:
                    work_key = doc['key']
                    work_url = f"https://openlibrary.org{work_key}.json"
                    
                    try:
                        with urllib.request.urlopen(work_url) as response:
                            work_data = json.loads(response.read())
                        
                        # Get description
                        if 'description' in work_data:
                            desc = work_data['description']
                            # Description might be a dict or string
                            if isinstance(desc, dict):
                                desc = desc.get('value', '')
                            
                            if desc and len(desc) > max_length:
                                best_description = desc
                                max_length = len(desc)
                    except:
                        pass
                
                # Also check for excerpt
                if 'excerpts' in doc and doc['excerpts']:
                    excerpt = doc['excerpts'][0]
                    if isinstance(excerpt, dict):
                        excerpt = excerpt.get('text', '')
                    if len(excerpt) > max_length:
                        best_description = excerpt
                        max_length = len(excerpt)
        
        return best_description
    except Exception as e:
        print(f"  Error fetching summary: {e}")
        return None

print("📚 Fetching book summaries from Open Library...")
print("This may take a minute...\n")

updated = 0
for idx, book in enumerate(books, 1):
    title = book['title']
    author = book['author']
    
    print(f"{idx}. {title} by {author}")
    
    # Skip if already has a good summary
    current_desc = book.get('description', '')
    if current_desc and len(current_desc) > 100:
        print("   ✓ Already has summary")
        continue
    
    summary = fetch_summary(title, author)
    
    if summary:
        book['summary'] = summary
        print(f"   ✓ Found summary ({len(summary)} chars)")
        updated += 1
    else:
        print("   ✗ No summary found")
    
    # Be nice to the API
    time.sleep(0.5)

# Write updated books.json
with open('books.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Updated {updated} books with summaries")
print("\nNow add your personal comments to books.json:")
print('  "personal_comment": "Your thoughts about the book..."')
print("\nThen run: python3 generate_bookshelf.py")

