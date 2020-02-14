# class Base(object):
#     XX = 123
#
#
# class Pro(Base):  # 上线环境
#     DEBUG = False
#
#
# class Dev(Base):  # 开发环境
#     DEBUG = True
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)  # 设置session超时时间
    SESSION_REFRESH_EACH_REQUEST = True  # 每次请求都保存session


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
