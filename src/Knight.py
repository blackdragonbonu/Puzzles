from __future__ import division
import numpy as np
import Utils.PriorityQueue as Queue 
import time
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

allowed_moves=np.array([[ 1,  2],
       [ 2,  1],
       [-1,  2],
       [ 2, -1],
       [ 1, -2],
       [-2,  1],
       [-1, -2],
       [-2, -1]])

class Knight_moves():
	def __init__(self,start_point=np.array([0,0])):
		self.position=start_point
		self.past_moves=[]

	def possible_moves(self):
		return self.position+allowed_moves

	def move(self,prev_knight_state,new_point):
		self.past_moves=prev_knight_state.past_moves[:]
		self.past_moves.append(prev_knight_state.position)
		self.position=new_point

	def reached_goal(self,goal_point):
		return (goal_point==self.position).all()

def move_knight(knight,new_position):
	new_state=Knight_moves()
	new_state.move(knight,new_position)
	return new_state

class result_info():
	def __init__(self,nodes_expanded=None,time_taken=0,optimal_path=[]):
		self.nodes_expanded=nodes_expanded
		self.time_taken=time_taken
		self.optimal_path=optimal_path
		self.nodes_history=[]
		self.f_cost_history=[]

	def add_history_info(self,node,cost):
		self.nodes_history.append(node)
		self.f_cost_history.append(cost)

	def update_results(self,nodes_expanded,time_taken,optimal_path):
		self.nodes_expanded=nodes_expanded
		self.time_taken=time_taken
		self.optimal_path=optimal_path

possible_moves=np.array([[ 1,  2],
       [ 2,  1],
       [-1,  2],
       [ 2, -1],
       [ 1, -2],
       [-2,  1],
       [-1, -2],
       [-2, -1]])


def odd_even_heuristic(position,goal_point):
	manhattan_distance=np.sum(np.abs(position-goal_point))
	moves_minimum=np.ceil(manhattan_distance/3)
	odd_even_factor=(((np.sum(position)%2)==(np.sum(goal_point)%2))==(moves_minimum%2)==0)*1
	return moves_minimum+odd_even_factor


def heuristic_cost(position,goal_point):
	max_deviation_cordinate=np.max(np.abs(position-goal_point))
	return odd_even_heuristic(position,goal_point)
	

def A_star_possibillities(current_state,current_cost,goal_point):
	return_value=[]
	for position in current_state.possible_moves():
		new_state=move_knight(current_state,position)
		return_value.append((current_cost+1+heuristic_cost(position,goal_point),new_state))
	return return_value

def bfs_possibillities(current_state):
	return_value=[]
	for position in current_state.possible_moves():
		new_state=move_knight(current_state,position)
		return_value.append(new_state)
	return return_value


def A_star_search(starting_point,goal_point,verbose=False):
	#starting state initialized
	current_state=Knight_moves(starting_point)
	#priority Queue for sorting by Fmetric in A star
	Q=Queue.PriorityQueue()
	# We push current state into the Queue
	Q.push((0,0,current_state))
	#iterator to uniquely identify objects
	i=0
	#To handle Duplicates
	evaluated_states=set()
	#Nodes expanded
	nodes_expanded=0
	#Timing the algorithm
	start_time=time.time()

	#results to return
	info=result_info()

	while (not current_state.reached_goal(goal_point)):
		cost,randomvalue,current_state=Q.pop()
		x,y=current_state.position

		#If not a duplicate state
		if not (x,y) in evaluated_states:
			if verbose:
				info.add_history_info(node=(x,y),cost=cost)

			nodes_expanded+=1
			possible_states=A_star_possibillities(current_state,cost,goal_point)
			for f_cost,state in possible_states:
				i+=1
				Q.push((f_cost,i,state))
			evaluated_states.add((x,y))
	time_taken=time.time()-start_time
	info.update_results(time_taken=time_taken,nodes_expanded=nodes_expanded,
		optimal_path=current_state.past_moves[:]+list([goal_point]))
	return info

def breadth_first_search(starting_point,goal_point,verbose=False):
	current_state=Knight_moves(starting_point)
	#priority Queue for sorting by Fmetric in A star
	Q=Queue.Queue()
	# We push current state into the Queue
	Q.push((current_state,0))
	#iterator to uniquely identify objects
	i=0
	#To handle Duplicates
	evaluated_states=set()
	#Nodes expanded
	nodes_expanded=0
	#Timing the algorithm
	start_time=time.time()

	#results to return
	info=result_info()

	while (not current_state.reached_goal(goal_point)):
		current_state,depth=Q.pop()
		x,y=current_state.position

		#If not a duplicate state
		if not (x,y) in evaluated_states:
			if verbose:
				info.add_history_info(node=(x,y),cost=depth)

			nodes_expanded+=1
			possible_states=bfs_possibillities(current_state)
			i+=1
			for state in possible_states:
				Q.push((state,i))
			evaluated_states.add((x,y))
	time_taken=time.time()-start_time
	info.update_results(time_taken=time_taken,nodes_expanded=nodes_expanded,
		optimal_path=current_state.past_moves[:]+list([goal_point]))
	return info


if __name__=='__main__':
	#goal_point=np.array(map(int,raw_input("Enter the points of goal, seperated by space").split()))
	
	goal_point=np.array([2,2])
	start_point=np.array([0,0])
	result=A_star_search(start_point,goal_point,True)
	print result.time_taken,result.nodes_expanded,result.optimal_path
	for x,y in result.optimal_path:
		print x,y
	# for i,node in enumerate(result.nodes_history):
	# 	print node,result.f_cost_history[i]

	# result=breadth_first_search(start_point,goal_point,True)
	# print result.time_taken,result.nodes_expanded,result.optimal_path
	# for i,node in enumerate(result.nodes_history):
	# 	print node,result.f_cost_history[i]