require 'json'
require 'rmagick'

class CustomBook
  @@books_data = []
  @@base_path = ""

  def self.load(books_json_path)
    @@base_path = File.dirname(books_json_path)
    data = JSON.parse(File.read(books_json_path))
    @@books_data = data['books']
  end

  def self.all_books
    @@books_data.map.with_index { |book_data, index| CustomBook.new(index) }
      .sort_by { |book| [book.author_sort, book.series, book.series_index] }
  end

  def self.some_books(limit = 10)
    @@books_data.take(limit).map.with_index { |book_data, index| CustomBook.new(index) }
      .sort_by { |book| [book.author_sort, book.series, book.series_index] }
  end

  def self.search_author(query)
    matching_indices = @@books_data.each_with_index.select do |book_data, index|
      book_data['author']&.downcase&.include?(query.downcase)
    end.map(&:last)
    
    matching_indices.map { |index| CustomBook.new(index) }
      .sort_by { |book| [book.series, book.series_index] }
  end

  def self.search_series(query)
    matching_indices = @@books_data.each_with_index.select do |book_data, index|
      book_data['series']&.downcase&.include?(query.downcase)
    end.map(&:last)
    
    matching_indices.map { |index| CustomBook.new(index) }
      .sort_by { |book| [book.series, book.series_index] }
  end

  def initialize(book_index)
    @index = book_index
    @data = @@books_data[@index]
  end

  def id
    @index
  end

  def title
    @data['title'] || 'Untitled'
  end

  def author
    @data['author'] || 'Unknown Author'
  end

  def author_sort
    @data['author_sort'] || @data['author'] || 'Unknown'
  end

  def series
    @data['series'] || ''
  end

  def series_index
    @data['series_index'] || 0
  end

  def series_index_display
    i = series_index
    if i.to_i.to_f == i.to_f
      i.to_i.to_s
    else
      i.to_s
    end
  end

  def description
    @data['description'] || ''
  end

  def book_path
    @data['file_path'] || ''
  end

  def cover
    return @cover unless @cover.nil?
    
    # Check if custom cover is specified
    if @data['cover']
      cover_path = File.join(@@base_path, @data['cover'])
      @cover = cover_path if File.exist?(cover_path)
    end
    
    # Fallback to default naming convention: covers/title.jpg
    unless @cover
      cover_filename = "#{title.gsub(/[^0-9A-Za-z ]/, '').gsub(' ', '_')}.jpg"
      cover_path = File.join(@@base_path, 'covers', cover_filename)
      @cover = cover_path if File.exist?(cover_path)
    end
    
    # Last resort: try png
    unless @cover
      cover_filename = "#{title.gsub(/[^0-9A-Za-z ]/, '').gsub(' ', '_')}.png"
      cover_path = File.join(@@base_path, 'covers', cover_filename)
      @cover = cover_path if File.exist?(cover_path)
    end
    
    @cover
  end

  def cover_color
    return @cover_color unless @cover_color.nil?
    return '#333' unless cover && File.exist?(cover)
    
    begin
      img = Magick::Image.read(cover).first
      img_small = img.resize(0.1)
      color = img_small.pixel_color(2, img.base_rows * 0.025)
      @cover_color = color.to_color(Magick::AllCompliance, false, 8, true)
    rescue
      @cover_color = '#333'
    end
    
    @cover_color
  end

  def cover_contrast
    return @cover_contrast unless @cover_contrast.nil?
    
    color_string = cover_color
    red = color_string[1..2].to_i(16)
    green = color_string[3..4].to_i(16)
    blue = color_string[5..6].to_i(16)
    brightness = (red + green + blue) / 3.0
    
    @cover_contrast = brightness > 128 ? "#111" : "#eee"
  end

  def aspect_ratio
    return @aspect_ratio unless @aspect_ratio.nil?
    return 0.65 unless cover && File.exist?(cover) # Default book aspect ratio
    
    begin
      img = Magick::Image.read(cover).first
      @aspect_ratio = img.base_columns.to_f / img.base_rows
    rescue
      @aspect_ratio = 0.65
    end
    
    @aspect_ratio
  end

  def file_path
    return nil unless @data['file_path']
    File.join(@@base_path, @data['file_path'])
  end

  def page_count
    @data['pages'] || 300
  end

  def nonlinear_thickness
    @thickness ||= [0.85 * (page_count**0.6), 8].max
  end
end

