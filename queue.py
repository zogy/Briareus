import zmq


LRU_READY = "\x01"
context = zmq.Context()


class Broker(object):
	def __init__(self, front_addr, back_addr):
		self.frontend = context.socket(zmq.ROUTER)
		self.frontend.bind(front_addr)
		self.backend = context.socket(zmq.DEALER)
		self.backend.bind(back_addr)

	def run(self):
		zmq.device(zmq.QUEUE, self.frontend, self.backend)
		

if __name__ == '__main__':
	Broker("ipc://clientend", "ipc://serverend").run()