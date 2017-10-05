import os

from data.news.news_database.models import db


if os.path.exists("news.db"):
    os.remove("news.db")

# Creates a new with current model settings
db.create_all()

