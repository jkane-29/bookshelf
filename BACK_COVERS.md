# Adding Back Cover Images

Your bookshelf now supports **actual back cover images** instead of just text!

## How It Works

### Default (Text Description)
By default, when you flip a book, the back shows:
- Book description
- Page count
- Background color matches the front cover

### With Back Cover Image
If you add a `back_cover` image, it will display the actual back cover of the book instead!

## Adding a Back Cover

### Step 1: Get the Back Cover Image

Options:
1. **Scan your physical book** - Take a photo of the back cover
2. **Google Images** - Search `"[book title] back cover"`
3. **Amazon** - Some books show back cover in additional images
4. **Publisher websites** - Often have high-res back covers

### Step 2: Save the Image

Save back cover images to a folder like:
```
back_covers/Book_Title_Back.jpg
```

Or mix them with front covers:
```
covers/Book_Title_Back.jpg
```

### Step 3: Add to books.json

Add the `back_cover` field to your book entry:

```json
{
  "title": "Thinking, Fast and Slow",
  "author": "Daniel Kahneman",
  "author_sort": "Kahneman, Daniel",
  "description": "A groundbreaking tour...",
  "pages": 499,
  "cover": "covers/Thinking_Fast_and_Slow.jpg",
  "back_cover": "covers/Thinking_Fast_and_Slow_Back.jpg"
}
```

### Step 4: Regenerate

```bash
python3 generate_bookshelf.py
```

Refresh your browser and flip the book - you'll see the actual back cover!

## Example Setup

```
bookshelf/
├── covers/
│   ├── Book_Title.jpg          ← Front cover
│   └── Book_Title_Back.jpg     ← Back cover
└── books.json
```

## Tips

- **Resolution**: Match the front cover size for best results
- **Aspect ratio**: Should be similar to front cover
- **Optional**: You can mix - some books with back covers, others with text
- **Format**: JPG or PNG both work

## Color Extraction

The bookshelf now **automatically extracts colors** from your cover images!

- Spine color matches the dominant color from the top of the front cover
- Text color (black/white) automatically adjusts for readability
- No manual color configuration needed!

Just add covers and the app does the rest! 🎨

