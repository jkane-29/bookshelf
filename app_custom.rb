require 'sinatra'
require_relative 'custom_books.rb'
require_relative 'logos.rb'

## setup
books_file = ARGV[0] || 'books.json'
raise "Cannot find books file: #{books_file}" unless File.exist?(books_file)

CustomBook.load(books_file)

## endpoints

get '/' do
  @books = CustomBook.some_books(25)
  erb :index
end

get '/author/:query' do
  @books = CustomBook.search_author params['query']
  erb :index
end

get '/series/:query' do
  @books = CustomBook.search_series params['query']
  erb :index
end

get '/download/*' do
  filepath = "/" + params['splat'].first
  filepath.gsub!("/../", "/") # try to avoid exposing the whole filesystem
  puts "DEBUG getting #{filepath}"
  
  # For custom books, allow downloads from the books directory
  if File.exist?(filepath) && filepath.start_with?(File.expand_path(File.dirname(books_file)))
    send_file filepath
  else
    raise Sinatra::NotFound
  end
end

