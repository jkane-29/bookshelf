# Custom Books - Simple Bookshelf Setup

A modern, lightweight alternative to the Calibre-based bookshelf. No database required!

## Quick Start

1. **Install dependencies:**
   ```bash
   bundle install
   ```

2. **Add your books** to `books.json` (see format below)

3. **Add cover images** to the `covers/` folder

4. **Run the app:**
   ```bash
   ruby app_custom.rb
   ```

5. Open your browser to `http://localhost:4567`

## Adding Books

### Step 1: Edit `books.json`

Add book entries in this format:

```json
{
  "books": [
    {
      "title": "Your Book Title",
      "author": "Author Name",
      "author_sort": "Name, Author",
      "description": "A brief description or summary of the book.",
      "pages": 250,
      "series": "Series Name",
      "series_index": 1,
      "cover": "covers/Your_Book_Title.jpg",
      "file_path": "files/your-book.epub"
    }
  ]
}
```

**Required fields:**
- `title` - Book title
- `author` - Author name

**Optional fields:**
- `author_sort` - For sorting (e.g., "Tolkien, J.R.R.")
- `description` - Shows on book back cover
- `pages` - Page count (affects book thickness, defaults to 300)
- `series` - Series name
- `series_index` - Number in series (can be decimal like 1.5)
- `cover` - Path to cover image (relative to books.json location)
- `file_path` - Path to ebook file for downloads (optional)

### Step 2: Add Cover Images

Place cover images in the `covers/` folder. You can:

1. **Specify the path** in the JSON:
   ```json
   "cover": "covers/my_custom_name.jpg"
   ```

2. **Use auto-detection** - name the file based on the title:
   - Title: "The Great Gatsby" → `covers/The_Great_Gatsby.jpg`
   - Title: "1984" → `covers/1984.jpg`

Supported formats: `.jpg`, `.png`

## Getting Cover Images

### Option 1: Free Sources
- [Open Library](https://openlibrary.org/) - Search for a book, download cover
- [Google Books](https://books.google.com/) - Right-click cover → Save image
- [Goodreads](https://www.goodreads.com/) - Book pages have covers

### Option 2: Use Existing Book Covers
If you have ePub files, many contain cover images. Extract them:

```bash
# ePub files are just zip files
unzip your-book.epub
# Look for cover.jpg or cover.png in the extracted files
```

### Option 3: Generate Covers
Use AI tools or design your own simple covers:
- [Canva](https://www.canva.com/) - Free design tool
- [DALL-E](https://openai.com/dall-e) - AI-generated images
- Simple colored rectangles with title text work too!

## Example Setup

```
bookshelf/
├── app_custom.rb
├── custom_books.rb
├── books.json
├── covers/
│   ├── The_Great_Gatsby.jpg
│   ├── 1984.jpg
│   └── To_Kill_a_Mockingbird.jpg
└── files/               # Optional: for downloads
    ├── gatsby.epub
    └── 1984.epub
```

## Features

- **3D animated bookshelf** - Books flip to show covers and back covers
- **Variable book dimensions** - Height based on cover aspect ratio, thickness based on pages
- **Series support** - Books from series show index numbers
- **Search** - By author or series (visit `/author/AuthorName` or `/series/SeriesName`)
- **Downloads** - Optional ebook downloads if you add file paths

## Tips

1. **Page counts** affect book thickness - use realistic numbers (100-800)
2. **Cover aspect ratios** determine height - most book covers are around 0.65 (width/height)
3. **Series indices** can be decimals (e.g., 1.5 for novellas between books 1 and 2)
4. **Descriptions** show on the back cover - keep them concise

## Comparison to Calibre Version

**Pros:**
- ✅ No Calibre installation needed
- ✅ Simple JSON file instead of database
- ✅ Easy to edit and version control
- ✅ Lightweight and modern

**Cons:**
- ❌ Manual entry (but gives you full control)
- ❌ No built-in metadata fetching (but you can find covers easily online)

Enjoy your beautiful 3D bookshelf! 📚

