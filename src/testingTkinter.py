from __future__ import division
import Tkinter as tk
import numpy as np
import Knight as Knight
import time


goal_width=0
goal_height=0
coloumns_side=0
origin_x_start=0
origin_y_start=0
origin_x_end=0
origin_y_end=0

def run_algo(event=None):
	label_prompt1=tk.Label(text=variable.get(),justif=tk.CENTER,wraplength=90)
	label_prompt1.place(x=500,y=300)
	start_point=np.array([0,0])
	goal_point=np.array([goal_width,goal_height])
	solution=Knight.find_path(start_point,goal_point,True)
	print goal_point,solution[1]
	square_highlighting(solution[1],solution)
	

def display_final_solution(solution):
	for x,y in solution:
		intermediate_x_start=origin_x_start+(x*coloumns_side)
		intermediate_x_end=intermediate_x_start+coloumns_side
		intermediate_y_end=origin_y_start-((y-1)*coloumns_side)
		intermediate_y_start=intermediate_y_end-coloumns_side
		print intermediate_x_start,intermediate_x_end,intermediate_y_start,intermediate_y_end
		c.create_rectangle([(intermediate_x_start,intermediate_y_start),(intermediate_x_end,intermediate_y_end)],
			fill='green',tag='solution')


def square_highlighting(square_coordinates,solution):
		if not square_coordinates:
			display_final_solution(solution[0]['past_moves'])
		c.delete('intermediate')
		x,y =square_coordinates[0]
		intermediate_x_start=origin_x_start+(x*coloumns_side)
		intermediate_x_end=intermediate_x_start+coloumns_side
		intermediate_y_end=origin_y_start-((y-1)*coloumns_side)
		intermediate_y_start=intermediate_y_end-coloumns_side
		print intermediate_x_start,intermediate_x_end,intermediate_y_start,intermediate_y_end
		c.create_rectangle([(intermediate_x_start,intermediate_y_start),(intermediate_x_end,intermediate_y_end)],
			fill='blue',tag='intermediate')
		#c.after(500,c.delete('intermediate'))
		c.after(10,square_highlighting,square_coordinates[1:],solution)
		#c.delete('intermediate')


def create_grid(event=None):
	global goal_width
	global goal_height
	global coloumns_side
	global origin_x_start
	global origin_x_end
	global origin_y_start
	global origin_y_end

	goal_width=int(user_input_x.get())
	grid_width=np.abs(goal_width)+4
	goal_height=int(user_input_y.get())
	grid_height=np.abs(goal_height)+4
	w = c.winfo_width() # Get current width of canvas
	h = c.winfo_height() # Get current height of canvas
	c.delete('grid_line') # Will only remove the grid_line
	coloumns_side=np.min([w//(2*grid_width+1),h//(2*grid_height+1)])
	# Creates all vertical lines at intevals of 100
	for i in range(0, w, coloumns_side):
		c.create_line([(i, 0), (i, h)], tag='grid_line')

	# Creates all horizontal lines at intevals of 100
	for i in range(0, h, coloumns_side):
		c.create_line([(0, i), (w, i)], tag='grid_line')

	coordinate_max=np.max([(2*grid_width+1),(2*grid_height+1)])
	origin_x_start=(coordinate_max//2)*coloumns_side
	origin_y_start=(coordinate_max//2)*coloumns_side
	origin_x_end=((coordinate_max//2)+1)*coloumns_side
	origin_y_end=((coordinate_max//2)+1)*coloumns_side

	c.create_rectangle([(origin_x_start,origin_y_start),(origin_x_end,origin_y_end)],fill='black',
		tag='start')
	goal_x_start=origin_x_start+(goal_width*coloumns_side)
	goal_x_end=goal_x_start+coloumns_side
	goal_y_end=origin_y_start-((goal_height-1)*coloumns_side)
	goal_y_start=goal_y_end-coloumns_side,
	print(goal_y_end,goal_x_start,goal_width,goal_height,coloumns_side,goal_height*coloumns_side)
	c.create_rectangle([(goal_x_start,goal_y_start),(goal_x_end,goal_y_end)],fill='red',
		tag='stop')


root = tk.Tk()

c = tk.Canvas(root, height=500, width=500, bg='white')
root.minsize(width=600,height=500)
#c.bind('<Configure>', create_grid)
button_grid=tk.Button(root,height=3,width=10,text="Create grid",command= create_grid)
button_grid.place(x=500,y=120)
user_input_x=tk.Entry(root)
user_input_x.place(x=500,y=100,width=50)
user_input_y=tk.Entry(root)
user_input_y.place(x=550,y=100,width=50)
label_prompt1=tk.Label(text="Enter Goal Coordinate",justif=tk.CENTER,wraplength=90)
label_prompt1.place(x=500,y=50)
variable = tk.StringVar(root)
variable.set("one") # default value

list_box_algorithm = tk.OptionMenu(root, variable, "one", "two", "three")
list_box_algorithm.place(x=500,y=175)
button_grid2=tk.Button(root,height=3,width=10,text="Run Alorithm",command=run_algo)
button_grid2.place(x=500,y=210)

#button_grid.grid(row=2,column=5)
c.place(relx=0,rely=0,height=500,width=500)
root.mainloop()

