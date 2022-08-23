from newsfetch.google import *
from newsfetch.news import *



news = newspaper('https://www.newtv.co.th/news/2')
print(news.article)