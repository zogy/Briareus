from gevent_zeromq import zmq
import ujson as serlib
import snappy


LRU_READY = "\x01"
context = zmq.Context()

def dumps(data):
    return snappy.compress(serlib.dumps(data))

def loads(data):
    return serlib.loads(snappy.decompress(data))

class Netable(object):
    def __init__(self, C):
        self.instance = C()

    def run(self, address):
        self.sock = context.socket(zmq.DEALER)
        self.sock.connect(address)
        while True:
            msg = self.sock.recv_multipart()
            self.sock.close()
            request = loads(msg[2])
            ret = self.handle(request)
            self.sock = context.socket(zmq.DEALER)
            self.sock.connect(address)
            self.sock.send_multipart(msg[:2] + [dumps(ret)])

    def handle(self, message):
        func, args = message
        f = getattr(self.instance, func)
        return f(*args)

    def shutdown(self):
        self.sock.close()


class Client(object):
    def __init__(self, address):
        self.sock = context.socket(zmq.REQ)
        self.sock.connect(address)

    def call(self, func, args):
        self.sock.send(dumps((func, args)))
        return loads(self.sock.recv())

    def shutdown(self):
        self.sock.close()
