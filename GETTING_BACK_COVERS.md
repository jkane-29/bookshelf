# Getting Back Cover Images

Unfortunately, back covers aren't available through automatic APIs like front covers are. Here's the best workflow to get them:

## 🚀 Quick Workflow

### Option 1: Interactive Helper (Easiest)

```bash
python3 find_back_covers.py
```

This script will:
- Open Google Images searches for each book's back cover
- Show you the exact filename to save it as
- Guide you through all 39 books one by one

When you find a good back cover image:
1. Right-click the image
2. "Save Image As..."
3. Save to `covers/` with the suggested filename

### Option 2: Batch Search

Search Google Images for each book manually:
```
"[Book Title]" [Author] book back cover
```

Examples:
- `"Thinking Fast and Slow" Daniel Kahneman book back cover`
- `"The Power Broker" Robert Caro book back cover`

### Option 3: Physical Books

If you own the physical books:
1. Take a photo of the back cover with your phone
2. Transfer to your computer
3. Save in `covers/` folder

## 📝 Naming Convention

Save back covers as:
```
covers/[Title]_Back.jpg
```

Examples:
- `covers/Thinking_Fast_and_Slow_Back.jpg`
- `covers/The_Power_Broker_Back.jpg`
- `covers/Liars_Poker_Back.jpg`

(Remove spaces, commas, apostrophes, and special characters)

## 🔄 After Downloading

Once you have some back covers downloaded:

```bash
# Auto-detect and add them to books.json
python3 add_back_covers.py

# Regenerate your bookshelf
python3 generate_bookshelf.py
```

The `add_back_covers.py` script will automatically find all `*_Back.jpg` files and add them to the right books!

## 📍 Best Places to Find Back Covers

### 1. Google Images
- Search: `"book title" author back cover`
- Look in the "Images" tab
- Usually find scans from people who own the book

### 2. Amazon
- Find the book on Amazon
- Look through the product images
- Some books show back cover in the carousel
- Right-click and save

### 3. Goodreads
- Search for the book
- Some editions show back cover photos from users
- Check different editions

### 4. Publisher Websites
- Visit the publisher's website
- Look for the book in their catalog
- They sometimes have high-res back covers for press/marketing

### 5. Book Review Sites
- Sites that review books sometimes scan both covers
- Search: `"book title" review back cover`

## 💡 Tips

**Image Quality:**
- Aim for at least 400px tall
- JPG or PNG format
- Clean images without watermarks work best

**Don't Have the Book?**
- Try different editions on Amazon/Goodreads
- US vs UK editions often have different back covers
- Paperback vs hardcover may have different backs

**Can't Find It?**
- Leave it without a back cover - the description text looks fine!
- You can always add it later
- Focus on your favorites first

## 📊 Progress Tracking

Check what you have:
```bash
ls covers/*_Back.jpg | wc -l
```

See which books are missing back covers:
```bash
python3 add_back_covers.py
```

## Example: Getting One Back Cover

Let's get the back cover for "Thinking, Fast and Slow":

1. **Search Google Images:**
   ```
   "Thinking Fast and Slow" Daniel Kahneman back cover
   ```

2. **Find a good image** - look for clear photos of the actual book back

3. **Download it** - Right-click → Save Image As...

4. **Save as:** `covers/Thinking_Fast_and_Slow_Back.jpg`

5. **Update books.json:**
   ```bash
   python3 add_back_covers.py
   ```

6. **Regenerate:**
   ```bash
   python3 generate_bookshelf.py
   ```

7. **View it** - Click the book twice to see the back cover!

---

You don't need to get all 39 at once - start with your favorites and add more over time!

