import worker
import math
from math import sqrt
from numpy import arange
import pickle
import time

def f(x):
	return sqrt(x)

def g(x):
	return math.pow(x, 2)+f(abs(x))

def dot(f, g):
	return lambda x: f(g(x))

def test(*args):
		c = worker.Caller("ipc://clientend")
		print c.eval(*args)
		c.shutdown()

if __name__ == '__main__':
	import gevent
	jobs = [gevent.spawn(test, time.sleep, i) for i in range(10)]
	gevent.joinall(jobs)