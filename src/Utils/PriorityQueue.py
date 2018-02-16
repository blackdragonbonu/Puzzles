import heapq
import Queue

__all__=['PriorityQueue']

class PriorityQueue:
	def __init__(self):
		self.Queue=[]
		self.size=0

	def size(self):
		return self.size

	def push(self,item,heappush=heapq.heappush):
		heappush(self.Queue,item)
		self.size+=1

	def pop(self,heappop=heapq.heappop):
		if self.size:
			self.size-=1
			return heappop(self.Queue)
		else :
			raise Exception("Popping An Empty Queue")

	def get_top_element(self):
		return self.Queue[0]

	def get_elements(self,count=1):
		return self.Queue[:count]

	def empty(self):
		return self.size==0

class Queue():
	def __init__(self):
		self.Queue=[]
		self.size=0
	def size(self):
		return self.size

	def push(self,item):
		self.Queue.insert(0,item)
		self.size+=1

	def pop(self,heappop=heapq.heappop):
		if self.size:
			self.size-=1	
			return self.Queue.pop()
		else :
			raise Exception("Popping An Empty Queue")

	def get_top_element(self):
		return self.Queue[0]

	def get_elements(self,count=1):
		return self.Queue[:count]

	def empty(self):
		return self.size==0

if __name__=="__main__":
	Q=PriorityQueue()
	Q.pop()