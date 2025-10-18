#!/usr/bin/env python3
"""Generate a static HTML bookshelf from books.json"""

import json
import os
from PIL import Image

def get_dominant_color(image_path):
    """Extract dominant color from image"""
    try:
        img = Image.open(image_path)
        # Resize for faster processing
        img = img.resize((50, 50))
        # Convert to RGB if needed
        img = img.convert('RGB')
        
        # Get color from top-left area of cover (like the original app does)
        # Sample from top 2.5% of image
        width, height = img.size
        sample_height = max(1, int(height * 0.025))
        crop_box = (2, 0, width, sample_height)
        sample = img.crop(crop_box)
        
        # Get average color from sample
        pixels = list(sample.getdata())
        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    except Exception as e:
        print(f"  Warning: Could not extract color from {image_path}: {e}")
        # Return random color as fallback
        import random
        return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

def get_contrast_color(hex_color):
    """Get contrasting text color (black or white)"""
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Calculate brightness
    brightness = (r + g + b) / 3.0
    return '#111' if brightness > 128 else '#eee'

def is_light_cover(hex_color):
    """Check if cover is very light/white and needs a border"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # If all RGB values are high (> 220), it's a light cover
    return r > 220 and g > 220 and b > 220

def get_spine_font(book_title):
    """Get consistent font for a book based on its title"""
    # Classic book spine fonts
    fonts = [
        'Garamond, serif',
        'Baskerville, serif',
        'Didot, serif',
        'Bodoni MT, serif',
        'Caslon, serif',
        'Futura, sans-serif',
        'Helvetica, Arial, sans-serif',
        'Gill Sans, sans-serif',
        'Optima, sans-serif',
        'Palatino, serif'
    ]
    # Use hash of title to consistently select a font
    import hashlib
    hash_val = int(hashlib.md5(book_title.encode()).hexdigest(), 16)
    return fonts[hash_val % len(fonts)]

def get_spine_text_position(book_title):
    """Get consistent text position for a book (top, center, or bottom aligned)"""
    import hashlib
    hash_val = int(hashlib.md5(book_title.encode()).hexdigest(), 16)
    # Generate a value between 0 and 100 representing % from top
    # Bias towards center but allow some variation
    positions = [15, 20, 25, 35, 40, 45, 50, 55, 60, 65, 75, 80]
    return positions[hash_val % len(positions)]

def get_text_color_from_cover(image_path, bg_color):
    """Extract a visible text color from the cover image"""
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img = img.convert('RGB')
        
        # Sample colors from different areas of the cover
        pixels = list(img.getdata())
        
        # Get unique colors (with some tolerance)
        color_counts = {}
        for pixel in pixels:
            r, g, b = pixel
            # Round to reduce similar colors
            key = (r // 20 * 20, g // 20 * 20, b // 20 * 20)
            color_counts[key] = color_counts.get(key, 0) + 1
        
        # Sort by frequency
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Parse background color
        bg_hex = bg_color.lstrip('#')
        bg_r = int(bg_hex[0:2], 16)
        bg_g = int(bg_hex[2:4], 16)
        bg_b = int(bg_hex[4:6], 16)
        
        # Find a color with good contrast
        for color, count in sorted_colors:
            r, g, b = color
            # Calculate contrast ratio (simplified)
            bg_brightness = (bg_r + bg_g + bg_b) / 3.0
            text_brightness = (r + g + b) / 3.0
            contrast = abs(bg_brightness - text_brightness)
            
            # Need good contrast (at least 80 difference)
            if contrast > 80:
                return f'#{r:02x}{g:02x}{b:02x}'
        
        # Fallback to simple contrast
        return get_contrast_color(bg_color)
    except:
        return get_contrast_color(bg_color)

# Read books
with open('books.json', 'r') as f:
    data = json.load(f)
    books = data['books']

# Filter books that have covers
books_with_covers = []
for book in books:
    cover = book.get('cover', '')
    if cover and os.path.exists(cover):
        books_with_covers.append(book)

print(f"Found {len(books_with_covers)} books with covers out of {len(books)} total")

# First pass: calculate dimensions and partition into 2 rows
max_height = 0
book_data = []

for idx, book in enumerate(books_with_covers):
    # Get actual dimensions from cover image
    try:
        img = Image.open(book['cover'])
        width, img_height = img.size
        # Calculate height based on 200px width
        aspect = width / img_height
        height = int(200 / aspect)
    except:
        # Fallback to default if image can't be read
        aspect = 0.65
        height = int(200 / aspect)
    
    pages = book.get('pages', 300)
    thickness = max(0.85 * (pages ** 0.6), 8)
    
    book_data.append({
        'book': book,
        'idx': idx,
        'height': height,
        'thickness': thickness
    })
    
    if height > max_height:
        max_height = height

# Partition books into 2 rows to balance total width
# Sort by thickness (largest first) for better partitioning
sorted_books = sorted(book_data, key=lambda x: x['thickness'], reverse=True)

row1 = []
row2 = []
row1_width = 0
row2_width = 0

# Greedy partition: always add to the row with less width
for book_info in sorted_books:
    if row1_width <= row2_width:
        row1.append(book_info)
        row1_width += book_info['thickness']
    else:
        row2.append(book_info)
        row2_width += book_info['thickness']

# Sort each row by original order (or alphabetically)
row1.sort(key=lambda x: x['book']['author_sort'])
row2.sort(key=lambda x: x['book']['author_sort'])

print(f"Row 1: {len(row1)} books, width: {row1_width:.1f}px")
print(f"Row 2: {len(row2)} books, width: {row2_width:.1f}px")

# Generate books for each row
def generate_books_for_row(row_books, row_num):
    elements = []
    offset = 0
    
    for book_info in row_books:
        book = book_info['book']
        idx = book_info['idx']
        height = book_info['height']
        thickness = book_info['thickness']
        
        # Calculate font size based on both thickness and title length
        base_font_size = min(int(0.9 * thickness), 12)
        
        # Estimate how much vertical space we need for title + author
        title_length = len(book['title'])
        author_length = len(book['author'])
        
        # Available height with margins (leave 10% margin on each end - more generous)
        available_height = height * 0.85
        
        # Rough calculation for vertical text: char_width ≈ font_size * 0.6 (less aggressive)
        estimated_title_height = base_font_size * 0.6 * title_length
        estimated_author_height = (base_font_size - 1) * 0.6 * author_length
        total_estimated = estimated_title_height + estimated_author_height + 10  # 10px for spacing
        
        # Scale down if needed, but not too much
        if total_estimated > available_height:
            scale_factor = available_height / total_estimated
            # Don't scale down more than 70% of base size
            scale_factor = max(scale_factor, 0.7)
            title_font_size = max(int(base_font_size * scale_factor), 8)  # Minimum 8px (more readable)
        else:
            title_font_size = base_font_size
        
        # Extract actual color from cover image
        print(f"Row {row_num} - Processing: {book['title']} (height: {height}px, thickness: {thickness:.1f}px)")
        color = get_dominant_color(book['cover'])
        
        # Get text color from cover that contrasts with spine background
        text_color = get_text_color_from_cover(book['cover'], color)
        
        # Add border for light/white covers
        cover_border = "border: 1px solid #ddd;" if is_light_cover(color) else ""
        
        # Get consistent font for this book
        spine_font = get_spine_font(book['title'])
        
        # Keep old contrast for back cover
        contrast = get_contrast_color(color)
        
        book_html = f'''
  <!-- {book['title']} -->
  <div class="book-container" style="transform: translateX({offset + thickness/2}px) translateY({max_height - height}px);">
    <div id="book{row_num}_{idx}" class="book" style="transform: rotateY(90deg);" onclick="toggleBook(this.id)">
      <img class="cover" src="{book['cover']}" style="width: 200px; height: {height}px; display: block; object-fit: cover; object-position: bottom; transform: translateZ({thickness/2}px); {cover_border}">
      <div class="spine" style="width: {thickness}px; height: {height}px; background: {color} linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 20%, rgba(255,255,255,0.1) 80%, rgba(255,255,255,0) 100%); line-height: {thickness}px; transform: translateX(-{thickness/2}px) translateY(-{height}px) rotateY(-90deg);">
        <div class="spinetext" style="width:100%; height: {height}px">
          <span class="title" style="font-size: {title_font_size+1}px; line-height: {thickness}px; font-family: {spine_font}; color: {text_color};">{book['title']}</span>&emsp;
          <span class="author" style="font-size: {title_font_size}px; line-height: {thickness}px; font-family: {spine_font}; color: {text_color};">{book['author']}</span>
        </div>
      </div>
      <div class="back" style="color: {contrast}; width: 200px; height: {height}px; background:{color}; transform: translateY(-{height*2}px) translateZ(-{thickness/2}px) rotateY(180deg); overflow: hidden; box-sizing: border-box; font-family: {spine_font};">
        {'<img src="' + book.get('back_cover', '') + '" style="width: 200px; height: ' + str(height) + 'px; display: block; object-fit: cover; object-position: bottom; border-radius: 3px; ' + cover_border + '">' if book.get('back_cover') and os.path.exists(book.get('back_cover', '')) else '<div style="width: ' + str(200-16) + 'px; height: ' + str(height-24) + 'px; overflow: hidden; padding: 8px 0;">' + (('<div style="font-size: 8px; line-height: 1.3; margin-bottom: 6px;">' + book.get('summary', book.get('description', '')) + '</div>') if book.get('summary') or book.get('description') else '') + (('<div style="font-size: 8px; line-height: 1.3; color: ' + ('#FFD700' if contrast == '#111' else '#FF6B6B') + '; font-style: italic; border-top: 1px solid ' + contrast + '; padding-top: 4px; margin-top: 4px;">"' + book.get('personal_comment', '') + '"</div>') if book.get('personal_comment') else '') + '</div><div style="width: ' + str(200-16) + 'px; height: 16px; text-align: center; padding: 4px 0; border-top: 1px solid rgba(255,255,255,0.2);"><span style="float:left; font-size: 7px;">' + str(book.get('pages', 300)) + ' pages</span></div>'}
      </div>
      <div class="pages" style="width: {thickness-1}px; height: {height-6}px; background: #f1f1f1; transform: translateY(-{height*3 - 3}px) translateX({200-thickness/2-3}px) rotateY(90deg);"></div>
    </div>
  </div>'''
        
        elements.append(book_html)
        offset += thickness
    
    return elements, offset

# Generate both rows
row1_elements, row1_total_width = generate_books_for_row(row1, 1)
row2_elements, row2_total_width = generate_books_for_row(row2, 2)

# Generate complete HTML
html = f'''<!DOCTYPE html>
<html>
<head>
<title>My 3D Bookshelf</title>
<style>
body {{
  font-family: sans-serif;
  background: #f5f5f5;
  margin: 0;
  padding: 40px;
}}

h1 {{
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  font-size: 3em;
}}

.info {{
  color: #666;
  text-align: center;
  margin-bottom: 40px;
  font-size: 1.2em;
}}

.container,
.book-container,
.book {{
    transform-style: preserve-3d;
    position: absolute;
}}

.spinetext {{
  overflow: hidden;
  text-align: center;
  writing-mode: vertical-rl;
}}

.spinetext .title {{
  font-weight: bold;
  overflow: hidden;
}}

.spinetext .author {{
  font-weight: 300;
}}

.cover {{
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}}

.back {{
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  font-size: 8px;
  box-sizing: border-box;
  padding: 8px;
  overflow: hidden;
}}

/* Animations */
@keyframes bookdisplay {{
  0% {{ transform: translateX(0px) rotateY(90deg);}}
  50% {{ transform: translateZ(210px) rotateY(90deg);}}
  100% {{ transform: translateZ(210px) rotateY(0deg);}}
}}

@keyframes bookflip {{
  0% {{ transform: translateZ(210px) rotateY(0deg);}}
  100% {{ transform: translateZ(210px) rotateY(180deg);}}  
}}

@keyframes bookaway {{
  0% {{ transform: translateZ(210px) rotateY(180deg);}}  
  50% {{ transform: translateZ(210px) rotateY(90deg);}}
  100% {{ transform: translateX(0px) rotateY(90deg);}}
}}

@keyframes bookshowaway {{
  0% {{ transform: translateZ(210px) rotateY(0deg);}}  
  50% {{ transform: translateZ(210px) rotateY(90deg);}}
  100% {{ transform: translateX(0px) rotateY(90deg);}}
}}

.book:hover {{
  transition: transform 1s;
  transform: translateZ(-20px);
}}

.book-show {{
  animation-name: bookdisplay;
  animation-duration: 1.3s;
  animation-timing-function: ease;
  animation-fill-mode: both;
  z-index: 100 !important;
}}

.book-showback {{
  animation-name: bookflip;
  animation-duration: 0.7s;
  animation-timing-function: ease;
  animation-fill-mode: both;
  z-index: 100 !important;
}}

.book-showaway {{
  animation-name: bookshowaway;
  animation-duration: 0.7s;
  animation-timing-function: ease;
  animation-fill-mode: both;
  z-index: 100 !important;
}} 

.book-putaway {{
  animation-name: bookaway;
  animation-duration: 0.7s;
  animation-timing-function: ease;
  animation-fill-mode: both;
  z-index: 100 !important;
}} 
</style>
</head>
<body>

<div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
  <div style="display: flex; flex-direction: column; gap: 120px; align-items: center;">
    <!-- Row 1 -->
    <div class="container" style="perspective: 800px; height: {max_height}px; width: {max(row1_total_width, row2_total_width)+400}px; position: relative; z-index: 1;">
    {"".join(row1_elements)}
    </div>
    
    <!-- Row 2 -->
    <div class="container" style="perspective: 800px; height: {max_height}px; width: {max(row1_total_width, row2_total_width)+400}px; position: relative; z-index: 1;">
    {"".join(row2_elements)}
    </div>
  </div>
</div>

<script>
  function toggleBook(bookId) {{
    var book = document.getElementById(bookId);
    var bookContainer = book.parentElement;
    
    // Give the container a high z-index when book is active
    if (book.className.includes("book-show") || book.className.includes("book-putaway")) {{
      bookContainer.style.zIndex = "1000";
    }}
    
    replaceOtherBooks(book);
    if (book.className == "book") {{
      book.className = "book book-show";
      bookContainer.style.zIndex = "1000";
    }} else if (book.className == "book book-putaway") {{
      book.className = "book book-show";
      bookContainer.style.zIndex = "1000";
    }} else if (book.className == "book book-showaway") {{
      book.className = "book book-show";
      bookContainer.style.zIndex = "1000";
    }} else if (book.className == "book book-show") {{
      book.className = "book book-showback";
      bookContainer.style.zIndex = "1000";
    }} else if (book.className == "book book-showback") {{
      book.className = "book book-putaway";
      // Keep z-index high during putaway animation
      setTimeout(function() {{
        bookContainer.style.zIndex = "";
      }}, 700);
    }} else {{
      book.className = "book";
      bookContainer.style.zIndex = "";
    }}
  }}

  function replaceOtherBooks(book) {{
    var books = document.querySelectorAll('.book');
    for (var i = 0; i < books.length; ++i) {{
      if (books[i] != book) {{
        var otherContainer = books[i].parentElement;
        if (books[i].className == "book book-show") {{
          books[i].className = "book book-showaway";
          setTimeout(function(container) {{
            return function() {{ container.style.zIndex = ""; }};
          }}(otherContainer), 700);
        }} else if (books[i].className == "book book-showback") {{
          books[i].className = "book book-putaway";
          setTimeout(function(container) {{
            return function() {{ container.style.zIndex = ""; }};
          }}(otherContainer), 700);
        }}
      }}
    }}
  }}
</script>

</body>
</html>'''

# Write the file
with open('my_bookshelf.html', 'w') as f:
    f.write(html)

print(f"✅ Created my_bookshelf.html with {len(books_with_covers)} books!")
print(f"📖 Missing covers for {len(books) - len(books_with_covers)} books")
print(f"\nOpen it in your browser:")
print(f"  file://{os.path.abspath('my_bookshelf.html')}")

