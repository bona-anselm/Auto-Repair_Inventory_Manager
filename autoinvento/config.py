import os


class Config:
    SECRET_KEY = os.environ.get('AUTOSTOCK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autostock.db'
