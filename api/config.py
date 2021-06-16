from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'eyJkYXRhIjoieXRybXlrZXlkYWQhI18rKiJ9.VTcVkm8oR7f97bwJ8B8oSmIa')

    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET_KEY', '@3S32--@#5%^^_JkYXRhIjoibXlrZXlkYWQhI18rKiJ9.Y91JGOp8RqjexyVUfmWAKqJXJr8')
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # 7days

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_BASE_DIR = BASE_DIR

    ADMIN_U = os.environ.get('ADMIN_U', None)
    ADMIN_P = os.environ.get('ADMIN_P', None)
    PAYSTACK_API_KEY = os.environ.get('PAYSTACK_SECRET_KEY', None)
    FRONTEND_ENDPOINT = os.environ.get('FRONTEND_ENDPOINT')

    MAIL_SERVER = os.environ.get('EMAIL_SERVER')
    MAIL_PORT = os.environ.get('EMAIL_PORT')
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI_DEV_POSTGRESQL', '')


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI_PROD', '')