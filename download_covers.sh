#!/bin/bash

# Helper script to download book covers from Open Library
# Usage: ./download_covers.sh

echo "📚 Book Cover Downloader"
echo "========================"
echo ""
echo "I'll help you download covers for your books."
echo "For each book, I'll show you the Open Library search URL."
echo "Find the book, click on it, then right-click the cover and 'Copy Image Address'"
echo ""

# Function to sanitize filename
sanitize() {
    echo "$1" | sed 's/[^a-zA-Z0-9]/_/g'
}

# Books to download
declare -a books=(
    "Vineland:Thomas Pynchon"
    "Down and Out in Paris and London:George Orwell"
    "Against Everything:Mark Greif"
    "Manias, Panics and Crashes:Charles Kindleberger"
    "Liar's Poker:Michael Lewis"
    "Irrational Exuberance:Robert Shiller"
    "Zen Mind, Beginner's Mind:Shunryu Suzuki"
    "The Ascent of Money:Niall Ferguson"
    "The Essential Keynes:John Maynard Keynes"
    "Thinking, Fast and Slow:Daniel Kahneman"
    "The Power Broker:Robert Caro"
    "Stubborn Attachments:Tyler Cowen"
    "Walden and Other Writings:Henry David Thoreau"
    "Poor Charlie's Almanack:Charlie Munger"
    "An Economist Gets Lunch:Tyler Cowen"
    "Misbehaving:Richard Thaler"
    "Am I Being Too Subtle?:Sam Zell"
    "Barbarians at the Gate:Bryan Burrough"
    "Barbarian Days:William Finnegan"
    "Boomerang:Michael Lewis"
    "Going Infinite:Michael Lewis"
    "Keynes Hayek:Nicholas Wapshott"
    "Burmese Days:George Orwell"
    "Working:Robert Caro"
    "Words Without Music:Philip Glass"
    "Benjamin Franklin:Walter Isaacson"
    "Steve Jobs:Walter Isaacson"
    "The Fran Lebowitz Reader:Fran Lebowitz"
    "What I Talk About When I Talk About Running:Haruki Murakami"
    "High-Risers:Ben Austen"
    "Against the Gods:Peter Bernstein"
    "Fear and Loathing on the Campaign Trail '72:Hunter S. Thompson"
    "Zen and the Art of Motorcycle Maintenance:Robert Pirsig"
    "The Art of Doing Science and Engineering:Richard Hamming"
    "A Peace to End All Peace:David Fromkin"
    "Do Androids Dream of Electric Sheep?:Philip K. Dick"
    "Cherry:Nico Walker"
    "Silence:Shusaku Endo"
    "Homage to Catalonia:George Orwell"
)

for book in "${books[@]}"; do
    IFS=':' read -r title author <<< "$book"
    filename=$(sanitize "$title")
    
    if [ -f "covers/${filename}.jpg" ]; then
        echo "✓ Already have: $title"
    else
        echo ""
        echo "❌ Missing: $title by $author"
        search_query=$(echo "$title $author" | sed 's/ /+/g')
        echo "   Search: https://openlibrary.org/search?q=$search_query"
        echo "   Save as: covers/${filename}.jpg"
    fi
done

echo ""
echo "========================"
echo "Alternative: Use Google Images"
echo "Search: '[book title] book cover' and save high-quality images"
echo "Or visit: https://www.goodreads.com and search for each book"

