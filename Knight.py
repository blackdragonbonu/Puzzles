from __future__ import division
import numpy as np
import Utils.PriorityQueue as Queue 
import time
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


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
	

def possibillities(current_situtaion,current_cost,goal_point):
	point=current_situtaion['point']
	possible_positions=possible_moves+point
	return_value=[]
	for position in possible_positions:
		position_information={}
		position_information['point']=position
		position_information['past_moves']=current_situtaion['past_moves'][:]
		position_information['past_moves'].append(point)
		return_value.append((current_cost+1+heuristic_cost(position,goal_point),position_information))
	return return_value

def find_path(starting_point,goal_point,return_all_moves=False):
	current_position=starting_point
	Q=Queue.PriorityQueue()
	if return_all_moves:
		moves_history=[]
	current_situation={}
	current_situation['point']=current_position
	current_situation['past_moves']=[]
	Q.push((0,0,current_situation))
	i=0
	seen_positions=set()
	nodes_expanded=0
	start_time=time.time()
	while (current_position!=goal_point).any():
		cost,randomvalue,current_situation=Q.pop()
		current_position=current_situation['point']
		if not (current_position[0],current_position[1]) in seen_positions:
			if return_all_moves:
				moves_history.append(current_position)
			nodes_expanded+=1
			cases=[]
			cases=possibillities(current_situation,cost,goal_point)
			for possibility in cases:
				i+=1
				Q.push((possibility[0],i,possibility[1]))
			seen_positions.add((current_position[0],current_position[1]))
	current_situation['nodes_expanded']=nodes_expanded
	current_situation['time_taken']=time.time()-start_time
	if return_all_moves:
		return current_situation,moves_history
	return current_situation

if __name__=='__main__':
	print("This program prints displays a plot for the Knight, problem, you can give number specifying the number of trials")
	trials=int(input("Enter Number of trials : "))
	solution_depth=[]
	time_taken=[]
	nodes_expanded=[]
	starting_point=np.array([0,0])
	min_range=-100
	max_range=100
	for i in range(trials):
		goal_point=np.random.randint(min_range,max_range,2)
		return_value=find_path(goal_point=goal_point,starting_point=starting_point)
		solution_depth.append(len(return_value['past_moves'])-1)
		time_taken.append(return_value['time_taken'])
		nodes_expanded.append(return_value['nodes_expanded'])
		print "iteration {0},goal:{1}, solution depth:{2}, time taken:{3}, nodes expanded:{4}".format(i,goal_point,
			len(return_value['past_moves'])-1,return_value['time_taken'],return_value['nodes_expanded'])

	plt.figure()
	plt.clf()
	plt.scatter(solution_depth,nodes_expanded)
	plt.xlabel("Solution Depth")
	plt.ylabel("Number of nodes Expanded")
	plt.title("Nodes Expanded vs Solution Depth")
	plt.savefig('plot_1')
	plt.figure()
	plt.clf()
	plt.scatter(solution_depth,time_taken,color='r')
	plt.xlabel("Solution Depth")
	plt.ylabel("Time Taken(Seconds)")
	plt.title("Time Taken vs Solution Depth")
	plt.savefig('plot_2')

	
