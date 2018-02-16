from __future__ import division
import Tkinter as tk
import numpy as np
import src.Knight as knight

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

def initialize_window():
	global root
	global user_input_x
	global user_input_y
	global list_box_algorithm,variable,c,speed

	root = tk.Tk()

	c = tk.Canvas(root, height=500, width=500, bg='white')
	root.minsize(width=600,height=500)
	

	#button_grid=tk.Button(root,height=3,width=10,text="Create grid",command= create_grid)
	#button_grid.place(x=500,y=120)
	
	user_input_x=tk.Entry(root)
	user_input_x.place(x=500,y=100,width=50)

	user_input_y=tk.Entry(root)
	user_input_y.place(x=550,y=100,width=50)

	label_prompt1=tk.Label(text="Enter Goal Coordinate",justif=tk.CENTER,wraplength=90)
	label_prompt1.place(x=500,y=50)
	
	
	label_prompt2=tk.Label(text="Algorithm To Use",justif=tk.CENTER,wraplength=90)
	label_prompt2.place(x=500,y=120)
	variable = tk.StringVar(root)
	variable.set("A *") # default value
	list_box_algorithm = tk.OptionMenu(root, variable, "A *", "BFS")
	list_box_algorithm.place(x=500,y=150)
	
	label_prompt3=tk.Label(text="Speed",justif=tk.CENTER,wraplength=90)
	label_prompt3.place(x=500,y=190)
	speed=tk.StringVar(root)
	speed.set("slow")
	list_box_delay=tk.OptionMenu(root,speed,"slow","medium","fast")
	list_box_delay.place(x=500,y=210)

	button_grid2=tk.Button(root,height=3,width=10,text="Run Alorithm",command=run_algo)
	button_grid2.place(x=500,y=240)



	#button_grid.grid(row=2,column=5)
	c.place(relx=0,rely=0,height=500,width=500)

	return root

def get_inputs():
	user_inputs={}
	global goal_width
	global goal_height
	global user_input_x,user_input_y,list_box_algorithm

	goal_width=int(user_input_x.get())
	goal_height=int(user_input_y.get())
	algorithm=variable.get()
	return algorithm

def create_grid():
	global goal_width
	global goal_height
	global column_side_length
	global origin_x_start
	global origin_x_end
	global origin_y_start
	global origin_y_end,c

	grid_width=np.abs(goal_width)+4
	grid_height=np.abs(goal_height)+4

	w = c.winfo_width() # Get current width of canvas
	h = c.winfo_height() # Get current height of canvas
	c.delete('grid_line') # Will only remove the grid_line
	c.delete('start')
	c.delete('stop')
	c.delete('solution')

	column_side_length=np.min([w//(2*grid_width+1),h//(2*grid_height+1)])
	# Creates all vertical lines at intevals of 100
	for i in range(0, w, column_side_length):
		c.create_line([(i, 0), (i, h)], tag='grid_line')

	# Creates all horizontal lines at intevals of 100
	for i in range(0, h, column_side_length):
		c.create_line([(0, i), (w, i)], tag='grid_line')

	coordinate_max=np.max([(2*grid_width+1),(2*grid_height+1)])
	origin_x_start=(coordinate_max//2)*column_side_length
	origin_y_start=(coordinate_max//2)*column_side_length
	origin_x_end=((coordinate_max//2)+1)*column_side_length
	origin_y_end=((coordinate_max//2)+1)*column_side_length

	c.create_rectangle([(origin_x_start,origin_y_start),(origin_x_end,origin_y_end)],fill='black',
		tag='start',stipple="gray12")

	goal_x_start=origin_x_start+(goal_width*column_side_length)
	goal_x_end=goal_x_start+column_side_length
	goal_y_end=origin_y_start-((goal_height-1)*column_side_length)
	goal_y_start=goal_y_end-column_side_length,
	print(goal_y_end,goal_x_start,goal_width,goal_height,column_side_length,goal_height*column_side_length)
	c.create_rectangle([(goal_x_start,goal_y_start),(goal_x_end,goal_y_end)],fill='red',
		tag='stop')

	for i in range(0,w,column_side_length):
		for j in range(0,h,column_side_length):
			x=(origin_x_start-j)//column_side_length
			y=(i-origin_y_start)//column_side_length
			c.create_text(i+(column_side_length//2),j+(column_side_length//2),
				text=str((x,y)),font=("Purisa",(column_side_length//6)),tag='grid_line')

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

def run_algo():
	global c,speed
	algo=get_inputs()
	create_grid()

	start_point=np.array([0,0])
	goal_point=np.array([goal_width,goal_height])
	if algo=="A *":
		results=knight.A_star_search(start_point,goal_point,True)
	elif algo=="BFS":
		results=knight.breadth_first_search(start_point,goal_point,True)
	set_speed()
	square_highlighting(results.nodes_history,results.optimal_path[1:len(results.optimal_path)-1])




if __name__=="__main__":
	root=initialize_window()
	root.mainloop()