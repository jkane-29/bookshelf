#!/bin/bash

# Download all book covers using ISBNs
cd covers

echo "📚 Downloading book covers from Open Library..."

curl -L "https://covers.openlibrary.org/b/isbn/9780141180632-L.jpg" -o Vineland.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780156262248-L.jpg" -o Down_and_Out_in_Paris_and_London.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781101871157-L.jpg" -o Against_Everything.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780471389453-L.jpg" -o Manias_Panics_and_Crashes.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780393338690-L.jpg" -o Liars_Poker.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780691173122-L.jpg" -o Irrational_Exuberance.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781590308493-L.jpg" -o Zen_Mind_Beginners_Mind.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780143116172-L.jpg" -o The_Ascent_of_Money.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781846148132-L.jpg" -o The_Essential_Keynes.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780374275631-L.jpg" -o Thinking_Fast_and_Slow.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780394720241-L.jpg" -o The_Power_Broker.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781732265134-L.jpg" -o Stubborn_Attachments.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780679783343-L.jpg" -o Walden_and_Other_Writings.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781578645015-L.jpg" -o Poor_Charlies_Almanack.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780452298842-L.jpg" -o An_Economist_Gets_Lunch.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780393352795-L.jpg" -o Misbehaving.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781591848233-L.jpg" -o Am_I_Being_Too_Subtle.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780061655555-L.jpg" -o Barbarians_at_the_Gate.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780143109396-L.jpg" -o Barbarian_Days.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780393343441-L.jpg" -o Boomerang.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781324105817-L.jpg" -o Going_Infinite.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780393343632-L.jpg" -o Keynes_Hayek.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780063344365-L.jpg" -o Burmese_Days.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780525656340-L.jpg" -o Working.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781631491436-L.jpg" -o Words_Without_Music.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780743258074-L.jpg" -o Benjamin_Franklin.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg" -o Steve_Jobs.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780679761808-L.jpg" -o The_Fran_Lebowitz_Reader.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780307389831-L.jpg" -o What_I_Talk_About_When_I_Talk_About_Running.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780062235077-L.jpg" -o High_Risers.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780471121046-L.jpg" -o Against_the_Gods.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781451691573-L.jpg" -o Fear_and_Loathing_on_the_Campaign_Trail.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780060839871-L.jpg" -o Zen_and_the_Art_of_Motorcycle_Maintenance.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781732265172-L.jpg" -o The_Art_of_Doing_Science_and_Engineering.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780805088090-L.jpg" -o A_Peace_to_End_All_Peace.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780345404473-L.jpg" -o Do_Androids_Dream_of_Electric_Sheep.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780525435938-L.jpg" -o Cherry.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9781250082244-L.jpg" -o Silence.jpg 2>/dev/null &
curl -L "https://covers.openlibrary.org/b/isbn/9780156421171-L.jpg" -o Homage_to_Catalonia.jpg 2>/dev/null &

wait

echo ""
echo "✅ Download complete!"
echo ""
echo "Checking downloaded files..."
ls -lh *.jpg | wc -l
echo "covers downloaded"

