from __future__ import division
import Tkinter as tk
import numpy as np
import src.TSP as TSP

#global variables for the application
goal_width=0
goal_height=0
column_side_length=0
TSP_problem=0
delay=10

def initialize_window():
	global root
	global user_input_x
	global user_input_y
	global list_box_cities,variable,c,num_cities,speed

	root = tk.Tk()

	c = tk.Canvas(root, height=500, width=500, bg='white')
	root.minsize(width=600,height=500)
	

	#button_grid=tk.Button(root,height=3,width=10,text="Create grid",command= create_grid)
	#button_grid.place(x=500,y=120)
	
	label_prompt1=tk.Label(text="Number of cities",justif=tk.CENTER,wraplength=90)
	label_prompt1.place(x=500,y=50)
	num_cities=tk.StringVar(root)
	num_cities.set("1")
	list_box_cities=tk.OptionMenu(root,num_cities,"1","2","3","4","5","6","7","8","9","10")
	list_box_cities.place(x=500,y=80)

	
	#will be used in future after we add more algorithms to travelling salesman problem
	# label_prompt2=tk.Label(text="Algorithm To Use",justif=tk.CENTER,wraplength=90)
	# label_prompt2.place(x=500,y=120)
	# variable = tk.StringVar(root)
	# variable.set("A *") # default value
	# list_box_algorithm = tk.OptionMenu(root, variable, "A *", "BFS")
	# list_box_algorithm.place(x=500,y=150)
	
	label_prompt2=tk.Label(text="Speed",justif=tk.CENTER,wraplength=90)
	label_prompt2.place(x=500,y=190)
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
	global list_box_cities,num_cities

	cities=num_cities.get()
	return cities

def mark_cities(cities_count):
	global column_side_length
	global origin_y_end,c,TSP_problem


	w = c.winfo_width() # Get current width of canvas
	h = c.winfo_height() # Get current height of canvas
	c.delete('cities') # Will only remove the grid_line
	c.delete('start')
	c.delete('stop')
	c.delete('solution')
	#print cities_count
	TSP_problem=TSP.TSP(cities_count)
	#print TSP_problem.cities
	r=3
	for i in range(TSP_problem.num_cities):
		x,y=TSP_problem.cities[i]
		print x,y
		x=x*w
		y=y*h
		fill="blue"
		if i==0:
			fill="black"
		c.create_oval([(x-r,y-r),(x+r,y+r)],fill=fill,tag='cities')
		c.create_text(x,y-10,text="Origin")

	

def rectangle_coordinates(x,y):
	x_start=origin_x_start+(x*column_side_length)
	x_end=x_start+column_side_length
	y_end=origin_y_start-((y-1)*column_side_length)
	y_start=y_end-column_side_length
	return [(x_start,y_start),(x_end,y_end)]

def display_final_solution(solution):
	global c,TSP_problem
	w=c.winfo_width()
	h=c.winfo_height()
	final_path=solution['past_moves']+[solution['point']]
	for i,city in enumerate(final_path[1:]):
			city_x,city_y=TSP_problem.cities[city]
			city_x_start,city_y_start=TSP_problem.cities[final_path[i-1]]
			city_x=city_x*w
			city_y=city_y*h
			city_x_start*=w
			city_y_start*=h
			c.create_line(city_x_start,city_y_start,city_x,city_y,tag='solution',fill='green')



def path_display(path,solution):
	global c,delay,TSP_problem
	w = c.winfo_width() # Get current width of canvas
	h = c.winfo_height()
	c.delete('intermediate')
	if not path:
		c.delete('intermediate')
		display_final_solution(solution)
		return
		#c.delete('intermediate')
	current_path =path[0]
	print current_path
	for i,city in enumerate(current_path[1:]):
		city_x,city_y=TSP_problem.cities[city]
		city_x=city_x*w
		city_y=city_y*h
		city_x_start,city_y_start=TSP_problem.cities[current_path[i]]
		city_x_start*=w
		city_y_start*=h
		print i,city_x,city_y,city_x_start,city_y_start
		c.create_line([(city_x,city_y),(city_x_start,city_y_start)],tag='intermediate',fill='red')
		#c.after(delay,create_line,[(city_x,city_y),(city_x_start,city_y_start)],'intermediate','red')
	
	c.after(delay,path_display,path[1:],solution)

def create_line(coords,tag,fill,path,solution):
	global c
	c.create_line(coords,tag=tag,fill=fill)


def set_speed():
	global delay,speed
	user_speed=speed.get()
	if user_speed=="slow":
		delay=100
	elif user_speed=="medium":
		delay=20
	elif user_speed=="fast":
		delay=5

def run_algo():
	global c,speed,TSP_problem
	cities_count=get_inputs()
	print cities_count
	mark_cities(int(cities_count))
	solution,path=TSP.find_path(0,TSP_problem)
	print path
	set_speed()
	path_display(path,solution)




if __name__=="__main__":
	root=initialize_window()
	root.mainloop()
