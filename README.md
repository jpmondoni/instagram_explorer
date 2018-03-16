# Instragram Explorer - Scraping and Learning
A simple & basic package to build social media datasets based on Instagram public posts, using web scraping techniquies with BeautifulSoup.

## Purpose
This repo provides a pack of scraping functions that work with Instagram "Explore" page as of March, 2018.

## Goals
The goal of this project is to provide a tool to analysts, programmer, data scientists and students that need to build datasets from social media posts, such as Instagram. The initial idea was to use Instagram official API, but it's currently not supported an endpoint that retrieves public posts based on hashtags or locations.
The intent is also to create tweaks that help on data augmentation of datasets.

## Usage
This app can be used as of [v0.1.0-beta.2 as ](https://github.com/jpmondoni/instagram_explorer/releases/tag/v0.1.0-beta.2) with 3 types of arguments: [single hashtag](#single-hashtag), [hashtag list from file](#hashtag-list) or [hashtag + hashtag similar words](#hashtag-and-similar-words).

### Single Hashtag
A single hashtag can be passed as an argument on the compiler, such as:
`python read_tags.py -w soccer`
The app will explore only the `sys.argv[1]`, which is `soccer`, and get only it's results.

### Hashtag and Similar Words
[NLTK provides a WordNet Interface](http://www.nltk.org/howto/wordnet.html), which is used to discover similar words based on a given word. As this is still being sharpened, it's not that useful as of [v0.1.0-beta.2 as ](https://github.com/jpmondoni/instagram_explorer/releases/tag/v0.1.0-beta.2), but improvements will come. It [won't work with adjectives](https://stackoverflow.com/questions/13555399/nltk-wordnet-similarity-returns-none-for-adjectives), for instance.

To use this function, the `-wn` argument shall be passed to the compiler, as shwon below:
`python read_tags.py -wn sunshine`
The console will print all the words used to scrap Instagram data. On the sunshine example, the result will be:
```python
words =  [['sunshine', 1.0], ['sunlight', 1.0], ['fair_weather', 0.1]]
```
All words within the list will be scraped individually. Currently there is no distinction between choosen words and generated words on the database to provide some kind of identity, but it will be implemented later.

The second element of each element within the list is the similarity score calculated by NLTK `a.path_similarity(b)` function. Please refer to NLTK documentation for more information. This score will be stored in the database in the future.

### Hashtag List
A list of hashtags can be input in this package by using an argument in command line.

1. Create a textfile with a list of words, containing one word per line, as shown below:
```
soccer
brazil
neymar
worldcup
ronaldinho
dribre
```

2. Use the argument `-f filename.txt` to execute the code, like:
`python read_tags.py -f my_words.txt`
3. The code will read the file and print it's content in a python list format, as:
```python
words = ['soccer','brazil','neymar','worldcup','ronaldinho']
```