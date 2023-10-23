import redis
import os

# host = os.environ.get('REDIS_HOST')
# port = os.environ.get('REDIS_PORT')
# password = os.environ.get('REDIS_PASSWORD')

# Cloud
# host = 'redis-12162.c1.us-east1-2.gce.cloud.redislabs.com'
# port = 12162
# password = 'yRLHjV5qn1zuHVBESor7F8tbSQQr0BTD'

# Container
host = 'redis'
port = 6379


def testRedis():
    print('Beginning Redis connection test.')
    print('Connecting...')

    r = redis.Redis(
        host=host,
        port=port)

    print('Attempting write...')
    test_data = 'hello'
    r.set('msg', test_data)

    print('Attempting read...')

    if r.get('msg').decode('utf-8') == test_data:
        print('Successful Transaction.')


