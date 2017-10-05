from data.news.news_collector import collect_news
from data.news.news_database.models import add_news_to_db

# Extracts articles from cnn
newsData = collect_news('http://cnn.com')

# Uses the add_to_db method in news_database.models
# to add the articles in the list to the news database
add_news_to_db(newsData)

