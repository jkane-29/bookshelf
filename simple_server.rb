#!/usr/bin/env ruby
# Simple bookshelf server without heavy dependencies

require 'webrick'
require 'json'
require 'erb'

# Load books
books_data = JSON.parse(File.read('books.json'))

# Simple book class
class Book
  attr_reader :data, :index
  
  def initialize(data, index)
    @data = data
    @index = index
  end
  
  def id; @index; end
  def title; @data['title'] || 'Untitled'; end
  def author; @data['author'] || 'Unknown'; end
  def author_sort; @data['author_sort'] || author; end
  def series; @data['series'] || ''; end
  def series_index; @data['series_index'] || 0; end
  def description; @data['description'] || ''; end
  def page_count; @data['pages'] || 300; end
  
  def series_index_display
    i = series_index
    i.to_i.to_f == i.to_f ? i.to_i.to_s : i.to_s
  end
  
  def cover
    return @cover if @cover
    if @data['cover'] && File.exist?(@data['cover'])
      @cover = @data['cover']
    end
    @cover
  end
  
  def aspect_ratio
    return @aspect_ratio if @aspect_ratio
    @aspect_ratio = 0.65 # default
    if cover && File.exist?(cover)
      # Simple image dimension reading would require rmagick
      # For now, use default
      @aspect_ratio = 0.65
    end
    @aspect_ratio
  end
  
  def cover_color
    # Default colors - in real app this extracts from image
    @cover_color ||= sprintf("#%06x", (rand * 0xffffff).to_i)
  end
  
  def cover_contrast
    @cover_contrast ||= rand > 0.5 ? "#111" : "#eee"
  end
  
  def nonlinear_thickness
    [0.85 * (page_count**0.6), 8].max
  end
end

# Convert to book objects
books = books_data['books'].each_with_index.map { |data, i| Book.new(data, i) }
             .sort_by { |b| [b.author_sort, b.series, b.series_index] }

# Create server
server = WEBrick::HTTPServer.new(Port: 4567)

# Serve static files
server.mount "/css", WEBrick::HTTPServlet::FileHandler, "public/css"
server.mount "/fonts", WEBrick::HTTPServlet::FileHandler, "public/fonts"
server.mount "/covers", WEBrick::HTTPServlet::FileHandler, "covers"

# Main page
server.mount_proc '/' do |req, res|
  @books = books.take(40)
  template = ERB.new(File.read('views/index.erb'))
  res.body = template.result(binding)
end

trap('INT') { server.shutdown }

puts "🎉 Bookshelf server starting on http://localhost:4567"
puts "📚 Loaded #{books.size} books"
puts "Press Ctrl+C to stop"

server.start

