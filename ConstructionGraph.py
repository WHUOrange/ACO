import numpy as np
class ConstructionGraph:
    def __init__(self, h_matrix, configuration):
        self.h_matrix = h_matrix
        self.p_matrix = np.zeros(h_matrix.shape)
        self.p_matrix.fill(configuration.pher_init_amount)
        self.alpha = configuration.alpha
        self.beta = configuration.beta
        self.pher_evap_rate = configuration.pher_evap_rate
    
    def next_variable(self):
        return None

    def eval_component(self, variable, value_of_var):
        return 0.0

    def possible_values_of_var(self, variable):
        return None

    def components_transition_probability(self, variable, possible_values):
        p_values = self.p_matrix[variable, possible_values]
        h_values = self.h_matrix[variable, possible_values]
        prob = np.power(p_values, self.alpha) * np.power(h_values, self.beta)
        prob /= np.sum(prob)
        prob_dict = dict(zip(possible_values, prob))
        return prob_dict

    def get_transition_probability(self, variable):
        possible_values = self.possible_values_of_var(variable)
        prob = self.components_transition_probability(variable, possible_values)
        return prob 

    def is_solution_complete(self):
        return True   
    
    def evaporate(self, row, col):
        self.p_matrix[row, col] *= (1 - self.pher_evap_rate)

    def evaporate_all(self):
        self.p_matrix *= (1 - self.pher_evap_rate)

    def pheromone_release_amount(self, row, col, solution_score):
        return 1/solution_score

    def eval_solution(self, solution):
        return 0.0

    def release(self, row, col, amount):        
        self.p_matrix[row][col] += amount

    def release_all(self, solution_components, solution_score):        
        for component in solution_components:
            amount = self.pheromone_release_amount(component[0], component[1], solution_score)
            self.release(component[0], component[1], amount)

    def add_component(self, variable, value_of_var):
        pass

    def clear(self):
        pass

    def lambda_branching_factor(self, row, lmd):
        min_pheromone = 0.0
        max_pheromone = 0.0
        for i in range(self.p_matrix.shape(1)):
            p = self.p_matrix[row, i]
            if(p < min_pheromone):
                min_pheromone = p
            if(p > max_pheromone):
                max_pheromone = p
        limit = min_pheromone + lmd * (max_pheromone - min_pheromone)
        branching_factor = 0
        for i in range(self.p_matrix.shape(1)):
            if(self.p_matrix[row, i] > limit):
                branching_factor += 1 
        return branching_factor

    def average_lambda_branching_factor(self, lmd):
        sum = 0.0
        for i in range(self.p_matrix.shape(0)):
            sum = self.lambda_branching_factor(i, lmd)
        return sum / self.p_matrix.shape(0)
