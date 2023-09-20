import os


class Config:
    SECRET_KEY = os.environ.get('AUTOINVENTO_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autostock.db'
    
    # Configure Flask-Mail using your email provider's settings
    MAIL_SERVER = 'smtp.googlemail.com'  
    MAIL_PORT = 587  
    MAIL_USE_TLS = True 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
