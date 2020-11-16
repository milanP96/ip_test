SECRET_KEY = 'very_very_secure_and_secret'
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CACHE_TYPE = 'redis',
CACHE_KEY_PREFIX= 'fcache',
CACHE_REDIS_HOST =  'redis',
CACHE_REDIS_PORT = '6379',
CACHE_REDIS_URL = 'redis://redis:6379'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}/{db}'.format(user='test',pw='test',host='postgres',db='test')
SQLALCHEMY_TRACK_MODIFICATIONS = False