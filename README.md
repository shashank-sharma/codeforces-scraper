# codeforces-scraper
Scrapy spider to scrape codeforces site and get all the successful submission for one particular language.

Spider location: cfspider/spiders/cf.py

Python verison: Python 3.6

### How it works ?

At first it makes one request to the given URL with appropriate contestId and index which was fetched from [codeforces API](http://codeforces.com/api/help/). After that it fills out the form to make sure that the result have solutions which are ACCEPTED and the language which was given by user. After this it goes through each page and fetch all submissions id and yield them in proper format. Page limit size can be set in program.

To get data in JSON format run

`scrapy crawl cfSpider -o data.json`

And it will save the data in data.json file.

### Requirements

To run this on your local machine just create one virtual environment and clone this repository and then:

`pip install Scrapy`

And then you can run it successfully.
