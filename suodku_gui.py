from __future__ import division
import Tkinter as tk
import numpy as np
import src.sudoku as sudoku
import copy
import os


#global variables for the application
goal_width=0
goal_height=0
column_side_length=0
origin_x_start=0
origin_y_start=0
origin_x_end=0
origin_y_end=0
delay=10
speed=0
sudoku_problems=[]
sudoku_input_location=os.path.join(os.getcwd(),'src')
sudoku_input_location=os.path.join(sudoku_input_location,'sudoku_input')
problem=0


def initialize_window():
	global root
	global user_input_x
	global user_input_y
	global list_box_algorithm,variable,c,speed

	root = tk.Tk()

	c = tk.Canvas(root, height=540, width=540, bg='white')
	root.minsize(width=700,height=540)
	

	button_grid=tk.Button(root,height=3,width=14,text="generate_puzzle",command= generate_puzzle)
	button_grid.place(x=540,y=120)
	

	button_grid2=tk.Button(root,height=3,width=16,text="Run Alorithm",command=solve)
	button_grid2.place(x=540,y=240)



	#button_grid.grid(row=2,column=5)
	c.place(x=0,y=0)

	return root

def generate_puzzle():
	global goal_width
	global goal_height
	global column_side_length
	global origin_x_start
	global origin_x_end
	global origin_y_start
	global origin_y_end,c,sudoku_problems,problem
	
	grid_height=np.abs(goal_height)+4

	w = c.winfo_width() # Get current width of canvas
	h = c.winfo_height() # Get current height of canvas
	c.delete('grid_line') # Will only remove the grid_line
	c.delete('start')
	c.delete('stop')
	c.delete('solution')
	column_side_length=h//9
	# Creates all vertical lines at intevals of 100
	for i in range(0, w, column_side_length):
		c.create_line([(i, 0), (i, h)], tag='grid_line')

	# Creates all horizontal lines at intevals of 100
	for i in range(0, h, column_side_length):
		c.create_line([(0, i), (w, i)], tag='grid_line')
	
	#print sudoku_input_location

	sudoku_problems=sudoku.read_problems(sudoku_input_location)
	#print len(sudoku_problems)
	problem_number=np.random.randint(1,len(sudoku_problems))
	problem=copy.deepcopy(sudoku_problems[problem_number])
	print problem.problem
	for i in range(9):
		for j in range(9):
			if problem.problem[i,j]!=0:
				c.create_text(j*column_side_length+(column_side_length//2),i*column_side_length+(column_side_length//2),
					text=problem.problem[i,j],font=("Times New Roman",(column_side_length//4)),
					tag=['grid_line','checking'])

def rectangle_coordinates(x,y):
	x_start=origin_x_start+(x*column_side_length)
	x_end=x_start+column_side_length
	y_end=origin_y_start-((y-1)*column_side_length)
	y_start=y_end-column_side_length
	return [(x_start,y_start),(x_end,y_end)]

def display_final_solution(solution):
	global c
	for x,y in solution:
		rect_coordinates=rectangle_coordinates(x,y)
		c.create_rectangle([rect_coordinates[0],rect_coordinates[1]],
			fill='green',tag='solution',stipple="gray25")

def square_highlighting(square_coordinates,solution):
		global c,delay
		if not square_coordinates:
			c.delete('intermediate')
			display_final_solution(solution)
			return
		c.delete('intermediate')
		x,y =square_coordinates[0]
		rect_coordinates=rectangle_coordinates(x,y)
		
		c.create_rectangle([rect_coordinates[0],rect_coordinates[1]],
			fill='blue',tag='intermediate')
		
		c.after(delay,square_highlighting,square_coordinates[1:],solution)

def set_speed():
	global delay,speed
	user_speed=speed.get()
	if user_speed=="slow":
		delay=500
	elif user_speed=="medium":
		delay=100
	elif user_speed=="fast":
		delay=10

def solve():
	global c,speed,problem
	sudoku.solve_backtracking_with_MRV(problem)
	display_solving(problem.move_history)

def display_solving(move_history):
	if not move_history:
		return

	x,y=move_history[0][0]
	value=move_history[0][1]
	c.delete(str((x,y)))
	c.create_text(y*column_side_length+(column_side_length//2),x*column_side_length+(column_side_length//2),
				text=value,font=("Times New Roman",(column_side_length//4)),
				tag=['solution',str((x,y))])
	c.after(100,display_solving,move_history[1:])


if __name__=="__main__":
	root=initialize_window()
	root.mainloop()
