import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://myuser:mypassword@db_books:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
