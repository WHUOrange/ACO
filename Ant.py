#-*- coding:utf-8 -*-

import numpy as np
import sys
from ConstructionGraph import ConstructionGraph
from Error import Error

class Ant:
    def __init__(self, solution_score = sys.float_info.max):
        self.solution_score = solution_score
        self.solution_components = []

    def reset(self):
        self.solution_components.clear()
        self.solution_score = sys.float_info.max

    def choose_value(self, probability):
        rnd = np.random.ranf()
        tmp = 0.0
        for k in probability:
            tmp += probability[k]
            if(tmp>rnd):
                return k

    def add_component(self, variable, value_of_var):
        self.solution_components.append([variable, value_of_var])

    def update_solution_score(self, score):
        self.solution_score = score

    def construct_solution(self, construction_graph, alpha, beta):
        try:
            while(not construction_graph.is_solution_complete()):
                variable = construction_graph.next_variable()
                probability = construction_graph.get_transition_probability(variable)
                value_of_var = self.choose_value(probability)
                self.add_component(variable, value_of_var)
                construction_graph.add_component(variable, value_of_var)
            score = construction_graph.eval_solution(self.solution_components)
            self.update_solution_score(score)
            construction_graph.clear()
            return [self.solution_components, self.solution_score]
        except Error as e:
            raise e

    def local_search(self, construction_graph):
        num = len(self.solution_components)
        for i in range(num):
            for j in range(num-1, i, -1):
                first = self.solution_components[i]
                second = self.solution_components[j]
                third = self.solution_components[(j+1)%num]
                dist_now = construction_graph.eval_component(first[0],first[1]) \
                    + construction_graph.eval_component(second[0],second[1]) \
                    + construction_graph.eval_component(third[0],third[1])
                new_first = [first[0],second[1]]
                new_second = [third[0],first[1]]
                new_third = [second[0],third[1]]
                dist_opt = construction_graph.eval_component(new_first[0],new_first[1]) \
                    + construction_graph.eval_component(new_second[0],new_second[1]) \
                    + construction_graph.eval_component(new_third[0],new_third[1])
                if(dist_opt<dist_now):
                    self.solution_components[i] = new_first
                    self.solution_components[j] = new_second
                    self.solution_components[(j+1)%num] = new_third
        self.solution_score = construction_graph.eval_solution(self.solution_components)


    def get_solution(self):
        return self.solution_components

    def get_solution_score(self):
        return self.solution_score

    def update_solution(self, solution_info):
        self.solution_components = solution_info[0]
        self.solution_score = solution_info[1]



class ACSAnt(Ant):
    def __init__(self, solution_score = sys.float_info.max, q0 = 0.9):
        super().__init__(solution_score)
        self.q0 = q0

    def make_choice(self, probability):
        rnd = np.random.ranf()
        if(rnd >= self.q0):
            return min(probability,probability.get)
        else:
            k = self.choose_value(probability)
            return k


    def construct_solution(self, construction_graph, alpha, beta):
        try:
            while(not construction_graph.is_solution_complete()):
                variable = construction_graph.next_variable()
                probability = construction_graph.get_transition_probability(variable)
                value_of_var = self.make_choice(probability)
                self.add_component(variable, value_of_var)
                construction_graph.add_component(variable, value_of_var)
            score = construction_graph.eval_solution(self.solution_components)
            self.update_solution_score(score)
            construction_graph.clear()
            return [self.solution_components, self.solution_score]
        except Error as e:
            raise e
