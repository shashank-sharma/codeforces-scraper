'''

Scrapy spider to count rated user for particular language.
NOTE: Robots.txt is set to False

How to use

1. Change the PAGE_LIMIT according to your need
   For better performance set PAGE_LIMIT to MAX
   so that every page is visited once

2. Change LANGUAGE to desired one by checking with codeforces language options
   To get one do inspect element in language selection form

'''

from scrapy.http import FormRequest
from urllib.request import urlopen

import scrapy
import json



class QuotesSpider(scrapy.Spider):
    MAX = 2000             # MAX size that is possible in codeforces solutions
    PAGE_LIMIT = MAX       # Change Page limit to get more successful submission
    LANGUAGE = 'python.3'  # Get solutions from the given Language
    name = "cfRateSpider"

    def start_requests(self):
        # Make API call to codeforces server
        html = urlopen('http://codeforces.com/api/problemset.problems').read()

        # Convert given data into JSON format
        jsonData = json.loads(html.decode('utf-8'))

        for data in jsonData['result']['problems']:
            index = data['index']
            contestId = data['contestId']

            yield scrapy.Request(url='http://codeforces.com/problemset/status/'+str(contestId)+'/problem/'+str(index), 
                            callback=self.parse,
                            meta = {'index': index, 'contestId': contestId})

    def get_details(self, response):
        index = response.meta['index']
        contestId = response.meta['contestId']
        tem = response.meta['tem']
        rating = response.meta['rating']
        page = response.meta['page']
        url = 'http://codeforces.com/problemset/status/'+ str(contestId) +'/problem/'+ str(index) +'/page/'+str(tem)+'?order=BY_PROGRAM_LENGTH_ASC'
        try:
            currentPage = response.css('span.page-index.active::attr(pageindex)').extract()[0]
        except:
            page = 1
            currentPage = 1

        if page == currentPage:
            tem += 2000
        else:
            for i in response.css('a.rated-user::attr(title)'):
                data = i.extract().split(' ')
                if len(data) > 2:
                    rank = data[0] + ' ' + data[1]
                else:
                    rank = data[0]
                user = data[-1]
                
                if rank not in rating:
                    rating[rank] = []
                if user not in rating[rank]:
                    rating[rank].append(user)

        tem += 1    # Takes care of pages
        if tem >= self.PAGE_LIMIT:
            yield {
                "contestId": contestId,
                "index": index,
                "rating": rating,
            }
        else:
            yield scrapy.Request(url = url, 
                            callback= self.get_details, 
                            meta = {'index': index, 'contestId': contestId, 'tem': tem, 'page': currentPage, 'rating': rating})

    def parse(self, response):
        rating = {} # Empty dictionary which will have all data
        index = response.meta['index']
        contestId = response.meta['contestId']
        return scrapy.FormRequest.from_response(
                response,
                formxpath='//*[@id="sidebar"]/div/div[4]/form',
                dont_filter = True,
                meta = {'index': index, 'contestId': contestId,'rating': rating, 'tem': 2, 'page': 0},
                callback=self.get_details,
                formdata={'programTypeForInvoker': self.LANGUAGE,
                    'verdictName': 'OK'})
