import PriorityQueue as PQ
import Queue
import time


if __name__=="__main__":
	Q=Queue.PriorityQueue()
	MQ=PQ.PriorityQueue()
	start=time.time()
	trials=100000
	for i in range(trials):
		Q.put(i)
	print "Time taken to push {0} elements into their Queue is {1}".format(trials,-start+time.time())
	start=time.time()
	for i in range(trials):
		MQ.push(i)
	print "Time taken to push {0} elements into mine Queue is {1}".format(trials,-start+time.time())

	start=time.time()
	
	while not MQ.empty():
		MQ.pop()
	print "Time taken to pop {0} elements from mine Queue is {1}".format(trials,-start+time.time())
	start=time.time()
	while not Q.empty():
		Q.get()
	print "Time taken to pop {0} elements from their Queue is {1}".format(trials,-start+time.time())
