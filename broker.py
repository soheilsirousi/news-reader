import redis


class RedisHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            RedisHandler._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host='127.0.0.1', port=6379):
        self.pool = redis.ConnectionPool(host=host, port=port)
        self.redis = redis.Redis(connection_pool=self.pool, decode_responses=True)
        self.redis.ping
        
    def insert(self, url, visited=False):
        self.redis.set(url, str(visited))

    def get(self, url):
        return self.redis.get(url)

    def delete(self, url):
        self.redis.delete(url)


if __name__ == '__main__':
    pass
