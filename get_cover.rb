#!/usr/bin/env ruby
# Helper script to download book covers from Open Library
# Usage: ruby get_cover.rb "Book Title" "Author Name"

require 'net/http'
require 'json'
require 'uri'

def sanitize_filename(filename)
  filename.gsub(/[^0-9A-Za-z ]/, '').gsub(' ', '_')
end

def search_book(title, author = nil)
  query = title
  query += " #{author}" if author
  
  encoded_query = URI.encode_www_form_component(query)
  url = "https://openlibrary.org/search.json?q=#{encoded_query}&limit=1"
  
  puts "Searching for: #{query}"
  
  uri = URI(url)
  response = Net::HTTP.get(uri)
  data = JSON.parse(response)
  
  if data['docs'] && data['docs'].length > 0
    book = data['docs'][0]
    return book
  end
  
  nil
end

def download_cover(book_data, output_path)
  cover_id = book_data['cover_i']
  
  unless cover_id
    puts "❌ No cover found for this book"
    return false
  end
  
  # Use Large size cover
  cover_url = "https://covers.openlibrary.org/b/id/#{cover_id}-L.jpg"
  
  puts "Downloading cover from: #{cover_url}"
  
  uri = URI(cover_url)
  response = Net::HTTP.get_response(uri)
  
  if response.is_a?(Net::HTTPSuccess)
    File.write(output_path, response.body)
    puts "✅ Cover saved to: #{output_path}"
    return true
  else
    puts "❌ Failed to download cover: #{response.code}"
    return false
  end
end

# Main script
if ARGV.length < 1
  puts "Usage: ruby get_cover.rb \"Book Title\" [\"Author Name\"]"
  puts "Example: ruby get_cover.rb \"The Great Gatsby\" \"F. Scott Fitzgerald\""
  exit 1
end

title = ARGV[0]
author = ARGV[1]

book = search_book(title, author)

unless book
  puts "❌ Book not found"
  exit 1
end

puts "\nFound: #{book['title']}"
puts "Author: #{book['author_name']&.join(', ')}" if book['author_name']
puts "First published: #{book['first_publish_year']}" if book['first_publish_year']

filename = sanitize_filename(title) + ".jpg"
output_path = File.join('covers', filename)

# Create covers directory if it doesn't exist
Dir.mkdir('covers') unless Dir.exist?('covers')

if download_cover(book, output_path)
  puts "\n📖 Book info for your books.json:"
  puts JSON.pretty_generate({
    "title" => book['title'],
    "author" => book['author_name']&.first || author,
    "author_sort" => book['author_name']&.first&.split(' ')&.reverse&.join(', ') || author,
    "description" => "Add description here",
    "pages" => 300,
    "cover" => output_path
  })
end

