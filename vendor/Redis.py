import redis


class Redis:
    def __init__(self, host, port, db=0, password=None, decode_responses=True):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses

    def get_client(self):
        return redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password,
                                 decode_responses=self.decode_responses)


if __name__ == '__main__':
    rds = Redis(host='172.31.21.29', port=6379, password='zg@203&tcl!')
    r = rds.get_client()
    r.incr('heartbeat:https://www.vevor.com', 1)
    r.delete('heartbeat:https://www.vevor.com')
    print(r.get('heartbeat:https://www.vevor.com'))
