#-*- coding:utf-8 -*-
import numpy as np
from ConstructionGraph import ConstructionGraph
#from OptimazationProblem import OptimazationProblem
from LoadData import *

class TSPConstructionGraph(ConstructionGraph):
    def __init__(self, h_matrix, configuration, obj_matrix):        
        super().__init__(h_matrix, configuration)
        self.solution = []
        self.num_of_matrix_rows = h_matrix.shape[0]
        self.num_of_matrix_cols = h_matrix.shape[1]
        self.obj_matrix = obj_matrix

    def next_variable(self):
        if(len(self.solution)==0):
            i = np.random.randint(0,self.num_of_matrix_rows)
            return i
        else:
            return self.solution[-1]

    def possible_values_of_var(self, variable):
        all_values = np.array(range(self.num_of_matrix_cols))
        possiable_values = np.array([ value for value in all_values if value not in self.solution and value != variable])
        return possiable_values

    def is_solution_complete(self):
        if(len(self.solution)==self.num_of_matrix_rows):
            return True
        else:
            return False   

    def eval_solution(self, solution):
        tmp = 0.0
        for component in solution:
            tmp += self.obj_matrix[component[0],component[1]]
        return tmp

    def add_component(self, variable, value_of_var):
        self.solution.append(value_of_var)

    def clear(self):
        self.solution = []

    def eval_component(self, variable, value_of_var):
        return self.obj_matrix[variable,value_of_var]

    def release_all(self, solution_components, solution_score):        
        for component in solution_components:
            amount = self.pheromone_release_amount(component[0], component[1], 1/solution_score)
            self.release(component[0], component[1], amount)

'''class TestProblem(OptimazationProblem):
    def __init__(self):        
        cities = load_data('a280.tsp')
        self.row = len(cities)
        self.col = len(cities)
        self.heuristic_matrix = get_dist_matrix(cities)
        #self.heuristic_matrix = np.random.randint(1,50,(self.row, self.col))
        self.values = []
    
    def num_of_variables(self):
        return self.row

    def num_of_values(self):
        return self.col

    def pheromone_release_amount(self):
        return 0.3

    def is_tour_complete(self):
        if(len(self.values)<self.row):    
            return False
        else:
            return True

    def cur_variable(self):
        return len(self.values)

    def values_of_cur_variable(self):
        all_values = np.array(range(self.heuristic_matrix.shape[1]))
        inters = np.intersect1d(all_values, self.values)
        values = np.delete(all_values, inters)
        print(values)
        return values
        #return np.array(range(self.heuristic_matrix.shape[1]))

    def heuristic_info(self, variable):
        return self.heuristic_matrix[self.cur_variable(), :]

    def eval_solution(self, solution):
        tmp = 0.0
        for component in solution:
            tmp += component[1]
        return tmp

    def update_solution(self, variable, value_of_var):
        self.values.append(value_of_var)

    def clear(self):
        self.values = []

    def opt_score(self):
        tmp = 0.0
        for i in range(self.row):
            tmp += np.min(self.heuristic_matrix[i,:])
        return tmp'''