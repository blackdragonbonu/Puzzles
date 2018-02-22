from __future__ import division
import numpy as np
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import Queue
from collections import Counter

class TSP:
	def __init__(self,num_cities=5):
		self.num_cities=num_cities
		cities_created=0
		max_limit=101
		self.cities=[]
		dict_cities={}
		i=0
		print num_cities
		while cities_created<num_cities:
			new_city=np.random.randint(max_limit,size=2)
			i+=1
			if not dict_cities.get(str(new_city),None):
				self.cities.append(new_city/(max_limit-1))
				dict_cities[str(new_city)]=1
				cities_created+=1
		self.find_edges()
		
	def find_edges(self):
		self.edges=Counter()
		self.edges_duplicate=Counter()
		self.nodes_to_edges={}
		for index1 in range(self.num_cities):
			self.nodes_to_edges[index1]=[]
			for index2 in range(index1+1,self.num_cities):
				self.edges[index1,index2]=np.linalg.norm(self.cities[index1]-self.cities[index2])
				self.edges_duplicate[index1,index2]=self.edges_duplicate[index2,index1]=np.linalg.norm(self.cities[index1]-self.cities[index2])
				
	def minimum_spanning_tree(self,nodes_remaining,start_point):
		Q=Queue.PriorityQueue()
		
		current_node=start_point
		for node in nodes_remaining:
			edge_length=self.edges_duplicate[current_node,node]
			Q.put((edge_length,(current_node,node)))
		MST_cost=0.0
		MST_tree=[]
		while nodes_remaining:
			edge=Q.get()
			MST_cost+=edge[0]
			current_node=edge[1][1]
			if  not current_node in nodes_remaining:
				continue
			MST_tree.append(edge)
			nodes_remaining.remove(current_node)
			for node in nodes_remaining:
				edge_length=self.edges_duplicate[current_node,node]
				Q.put((edge_length,(current_node,node)))
				
		return MST_cost,MST_tree
				
	def TSP_possible_moves(self,starting_point,current_situation,current_cost,verbose=False):
		moves=[]
		if current_situation['nodes_remaining']:
			for node in current_situation['nodes_remaining']:
				g_move=self.edges_duplicate[current_situation['point'],node]
				h_cost=self.minimum_spanning_tree(set(current_situation['nodes_remaining']),starting_point)[0]
				node_information={}
				node_information['point']=node
				node_information['past_moves']=current_situation['past_moves'][:]
				if verbose:
					print "situation {0}, Reamining nodes {1}, Current_node {2}".format(node,current_situation['nodes_remaining'],
																				current_situation['point']  )
				node_information['nodes_remaining']=set(current_situation['nodes_remaining'])
				node_information['past_moves'].append(current_situation['point'])
				node_information['nodes_remaining'].remove(node)
				moves.append((current_cost+g_move+h_cost,node_information))
		else :
			node_information={}
			g_move=self.edges_duplicate[current_situation['point'],starting_point]
			h_cost=0
			node_information['point']=starting_point
			node_information['past_moves']=current_situation['past_moves'][:]
			node_information['nodes_remaining']=set()
			node_information['past_moves'].append(current_situation['point'])
			moves.append((current_cost+g_move+h_cost,node_information))
			
		return moves

def closing_condition(current_situation,starting_point):
	return  current_situation['nodes_remaining'] or not current_situation['point']==starting_point  

def find_path(starting_point,graph,verbose=False):
	current_position=starting_point
	Q=Queue.PriorityQueue()
	path_history=[]
	current_situation={}
	current_situation['point']=current_position
	current_situation['past_moves']=[]
	nodes_reamining=set(range(graph.num_cities))
	nodes_reamining.remove(starting_point)
	current_situation['nodes_remaining']=set(nodes_reamining)
	Q.put((0,0,current_situation))
	i=0
	seen_positions=set()
	nodes_expanded=0
	start_time=time.time()
	while (closing_condition(current_situation,starting_point)):
		cost,randomvalue,current_situation=Q.get()
		if verbose:
			print "Cost : {0} Situation : {1} ".format(cost,current_situation)
		current_position=current_situation['point']
		path_history.append(current_situation['past_moves']+[current_situation['point']])
		nodes_expanded+=1
		cases=[]
		cases=graph.TSP_possible_moves(starting_point=starting_point,current_situation=current_situation,
										  current_cost=cost,verbose=verbose)
		if verbose:
			print cases,i
		for possibility in cases:
			i+=1
			Q.put((possibility[0],i,possibility[1]))
	current_situation['nodes_expanded']=nodes_expanded
	current_situation['time_taken']=time.time()-start_time
	return current_situation,path_history

if __name__=='__main__':
	print "sample evaluation"
	problem=TSP(5)
	sol,path=find_path(0,problem)
	print path


