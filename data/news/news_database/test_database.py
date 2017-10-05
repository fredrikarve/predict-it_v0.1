from data.news.news_database import models
from data.news.news_database.models import get_keywords, get_five_article_titles, add_category, get_title, \
    get_categories

# Prints the titles of all articles currently in the news database
for a in models.News.query.all():
    print(a)

# Prints the keywords for the given article title
print(get_keywords(models.News.query.first()))

add_category(get_title(models.News.query.first()), "sports")

print(get_categories(models.News.query.first()))

print(get_five_article_titles())