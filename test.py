import worker
import math
from math import sin
from numpy import arange
import pickle
import time
import gevent

def f(x):
	for i in xrange(1000000):
		x += sin(x)
	return x

def g(x):
	return math.pow(x, 2)+f(abs(x))

def dot(f, g):
	return lambda x: f(g(x))

def test(i):
	c = worker.Caller("tcp://localhost:8858")
	h = dot(f,g)
	print c.eval(h, i)
	c.shutdown()

if __name__ == '__main__':
	jobs = [gevent.spawn(test, i) for i in xrange(2)]
	gevent.joinall(jobs)
