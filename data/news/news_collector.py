import newspaper
import datetime
import itertools

# Function that gathers news from a news site and returns a list of news and relating data
def collect_news(news_url):

    news_list = []

    paper = newspaper.build(news_url, memoize_articles=True)
    for current_article in itertools.islice(paper.articles, 0, 5):
        current_article.download()
        current_article.parse()
        current_article.nlp()

        news_to_add = {"title": current_article.title,
                       "keywords": current_article.keywords,
                       "url": current_article.url,
                       "source": paper.brand,
                       "collected": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       }
        news_list.append(news_to_add)

    return news_list
