from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import ForeignKey, desc
from sqlalchemy.orm import relationship

# Basic settings, where to create the database.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'news.db')
db = SQLAlchemy(app)


# News articles in a table, one touple per article
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)
    source = db.Column(db.String(100))
    collected = db.Column(db.String(20))
    url = db.Column(db.String(250), unique=True)

    def __repr__(self):
        return '%r' % self.title


# Keywords in separate table to keep NF1
class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, ForeignKey(News.id))
    keyword = db.Column(db.String(30))

    article = relationship("News", foreign_keys="Keyword.article_id")

    def __repr__(self):
        return '%r - %r' % (self.article, self.keyword)


# Category in separate table to keep NF1
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, ForeignKey(News.id))
    category = db.Column(db.String(30))

    article = relationship("News", foreign_keys="Category.article_id")

    def __repr__(self):
        return '%r - %r' % (self.article, self.category)


# Takes a list of articles and adds one by one to the database
def add_news_to_db(article_list):
    for art in article_list:
        add_art_to_db(art)


# Adds one article to the database, if no article with that title is in the database
def add_art_to_db(article):
    if News.query.filter_by(title=article.get("title")).first() is None:
        n = News(title=article.get("title"),
                 source=article.get("source"),
                 collected=article.get("collected"),
                 url=article.get("url"))
        db.session.add(n)
        db.session.commit()

        for keyword in article.get("keywords"):
            k = Keyword(article_id=News.query.filter_by(title=article.get("title")).first().id,
                        keyword=keyword)
            db.session.add(k)
        db.session.commit()


# Returns the title of the article in a string
def get_title(art):
    return art.title


# Extract the keywords in a list from the article with the matching title
def get_keywords(title):
    keyword_list = []
    for k in Keyword.query.filter_by(article=title):
        keyword_list.append(k.keyword)
    return keyword_list


# Extract the keywords in a list from the article with the matching title
def get_categories(title):
    category_list = []
    for c in Category.query.filter_by(article=title):
        category_list.append(c.category)
    return category_list


# Adds category to the selected article
def add_category(title, category):
    if Category.query.filter_by(article_id=News.query.filter_by(title=title).first().id).first() is None:
        c = Category(article_id=News.query.filter_by(title=title).first().id,
                     category=category)
        db.session.add(c)
        db.session.commit()


# Returns the five newest article titles in a list of strings
def get_five_article_titles():
    article_list = []
    for a in News.query.order_by(desc(News.id)).limit(5):
        article_list.append(a.title)
    return article_list
