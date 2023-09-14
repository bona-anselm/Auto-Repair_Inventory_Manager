import os


class Config:
    SECRET_KEY = os.environ.get('AUTOINVENTO_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autostock.db'