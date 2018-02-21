
import numpy as np
import os
import sys
import copy
from collections import defaultdict


sudoku_input_location=os.path.join(os.getcwd(),'sudoku_input')

class Sudoku():
    #converts a problem text to a 2d array, useful to solve problems
    def __init__(self,problem_strings):
        self.problem=np.zeros([9,9],dtype=np.int8)
        self.variables={}
        self.solution_guesses=0
        self.move_history=[]
        for i,line in enumerate(problem_strings):
            line=line.replace('-','0')
            self.problem[i]+=map(np.int8,line.split())
            for j,value in enumerate(self.problem[i]):
                if value==0:
                    self.variables[i,j]=np.arange(1,10)
                else:
                    self.variables[i,j]=value
        

def read_problems(path=sudoku_input_location):
    sudoku_problems=[]
    for filename in os.listdir(path):
        file=open(os.path.join(path,filename))
        file_content=file.read().split('\n')
        print '\n'.join(file_content)
        sudoku_problems.append(Sudoku(file_content[:len(file_content)-1]))
    return sudoku_problems
        

def assign_unassignvalues(unassigned_variables):
    for i in range(problem.problem.shape[0]):
        for j in range(problem.problem.shape[1]):
            if problem.problem[i,j]==0:
                #print problem.problem[i,j]
                unassigned_variables.append((i,j))
    return unassigned_variables

def check_consistency_row(problem):
    for row in problem:
        seen_before=set()
        for element in row:
            if element!=0:
                if element in seen_before:
                    return False
                else:
                    seen_before.add(element)
    return True


def check_consistency_column(problem):
    for row in problem.T:
        seen_before=set()
        for element in row:
            if element!=0:
                if element in seen_before:
                    return False
                else:
                    seen_before.add(element)
    return True


def check_box_consisitency(problem):
    for box_i in range(3):
        for box_j in range(3):
            seen_elements=set()
            for i in range(3):
                for j in range(3):
                    if problem[box_i*3+i,box_j*3+j]!=0:
                        if problem[box_i*3+i,box_j*3+j] in seen_elements:
                            return False
                        else:
                            seen_elements.add(problem[box_i*3+i,box_j*3+j])
    return True
                    


def check_consistency(problem):
    #print check_consistency_row(problem),check_box_consisitency(problem), check_consistency_column(problem)
    return check_consistency_row(problem) and check_box_consisitency(problem) and check_consistency_column(problem)

def check_if_problem_solved(problem):
    if (problem==0).any():
        return False
    else:
        return check_consistency(problem)
        


def update_row_forbidden(row,value,forbidden_dict,add=True):
    for i in range(9):
        if add:
            forbidden_dict[row,i].add(value)
        else :
            if value in forbidden_dict[row,i]:
                forbidden_dict[row,i].remove(value)


def update_coloumn_forbidden(column,value,forbidden_dict,add=True):
    for i in range(9):
        if add:
            forbidden_dict[i,column].add(value)
        else:
            if value in forbidden_dict[i,column]:
                forbidden_dict[i,column].remove(value)


def update_square_forbidden(row,column,value,forbidden_dic,add=True):
    start_i=row/3
    start_j=column/3
    for i in range(3):
        for j in range(3):
            if add:
                forbidden_dic[start_i*3+i,start_j*3+j].add(value)
            else :
                if value in forbidden_dic[start_i*3+i,start_j*3+j]:
                    forbidden_dic[start_i*3+i,start_j*3+j].remove(value)

def update_domains_robidden(i,j,forbidden_values,value,add=True):
    if add:
        update_row_forbidden(i,value,forbidden_values)
        update_coloumn_forbidden(j,value,forbidden_values)
        update_square_forbidden(i,j,value,forbidden_values)
    else:
        update_row_forbidden(i,value,forbidden_values,False)
        update_coloumn_forbidden(j,value,forbidden_values,False)
        update_square_forbidden(i,j,value,forbidden_values,False)
    return forbidden_values

def reduce_domain(problem):
    forbidden_values=defaultdict(set)
    for i in range(9):
        for j in range(9):
            if problem.problem[i,j]!=0:
                forbidden_values=update_domains_robidden(i,j,forbidden_values,problem.problem[i,j])
    for i in range(9):
        for j in range(9):
            if problem.problem[i,j]!=0:
                forbidden_values[i,j]=set()
    return forbidden_values

def solve_backtracking_with_MRV(problem):
    if check_if_problem_solved(problem.problem):
        return (True,problem)
    forbidden=reduce_domain(problem)
    var=sorted(forbidden.iteritems(),key=lambda(k,v):-len(v))[0][0]
    for domain_values in problem.variables[var]:
        problem.problem[var]=domain_values
        problem.solution_guesses+=1
        if not domain_values in forbidden[var] :
            problem.move_history.append((var,domain_values))
            forbidden=reduce_domain(problem)
            update_domains_robidden(var[0],var[1],forbidden,domain_values)
            result=solve_backtracking_with_MRV(problem)
            if result[0]:
                return result
        problem.problem[var]=0
        forbidden=reduce_domain(problem)
    return (False,None)

if __name__=='__main__':
    sudoku_problems=read_problems()
    problem=sudoku_problems[0]
    solve_backtracking_with_MRV(problem)
    print problem.move_history