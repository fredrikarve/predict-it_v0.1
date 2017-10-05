import unittest
import newspaper
import datetime
from data.news.news_database import models
from data.news.news_database.models import get_keywords
from data.news.news_collector import collect_news

class TestStringMethods(unittest.TestCase):

    def test_string_database(self):
        self.assertTrue(isinstance(models.News.query.first().title,str))
        self.assertTrue(isinstance(models.News.query.first().id, int))
        self.assertTrue(isinstance(models.News.query.first().source, str))
        #self.assertTrue(isinstance(models.News.query.first().category, str))
        self.assertTrue(isinstance(models.News.query.first().collected, str))
        self.assertTrue(isinstance(models.News.query.first().url, str))

    def test_news_string(self):
        paper = newspaper.build('http://cnn.com', memoize_articles=True)
        for current_article in paper.articles:
            current_article.download()
            current_article.parse()
            current_article.nlp()
            self.assertLessEqual(len(current_article.title), 150)
            self.assertLessEqual(len(paper.brand), 100)
            #self.assertLessEqual(len(current_article.category), 30)
            self.assertLessEqual(len(current_article.url), 250)
            self.assertLessEqual(len(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 20)
            self.assertLessEqual(len(current_article.keywords), 30)
            print('titel: ' + str(len(current_article.title)))
            print('source: ' + str(len(paper.brand)))
            print('url: ' + str(len(current_article.url)))
            print('collected: ' + str(len(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            print('keywords: ' + str(len(current_article.keywords)))

suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)

