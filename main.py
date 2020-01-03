import numpy as np
import time
from AntColony import *
from AntColonyConfiguration import *
from TestProblem import TSPConstructionGraph
from LoadData import *
from multiprocessing import *

def run():
    cities = load_data('a280.tsp')
    path = load_opt_solution('a280.opt.tour')
    dist_matrix = get_dist_matrix(cities)
    max_dist = np.max(dist_matrix)
    heuristic_matrix = (max_dist / (dist_matrix+1)).astype(np.float)
    print(heuristic_matrix)
    solution = []
    for i in range(len(path)):
        if(i>0):
            solution.append([path[i-1]-1,path[i]-1])
        else:
            solution.append([path[-1]-1,path[0]-1])
    print('最优方案{}'.format(solution))
    configuration = AntColonyConfiguration(local_search_type='LST_BEAT')
    problem = TSPConstructionGraph(heuristic_matrix,configuration,dist_matrix)
    score = problem.eval_solution(solution)
    print('最优方案目标函数分值{}'.format(score))
    ant_colony = AntColony(configuration, problem)
    ant_colony.run()
    print('蚁群最佳方案目标函数分值：{}'.format(ant_colony.best_ant.solution_score))

def acs_run():
    start_time = time.time()
    cities = load_data('a280.tsp')
    dist_matrix = get_dist_matrix(cities)
    max_dist = np.max(dist_matrix)
    heuristic_matrix = (max_dist / (dist_matrix+1)).astype(np.float)
    configuration = ACSAntColonyConfiguration()
    problem = TSPConstructionGraph(heuristic_matrix,configuration,dist_matrix)
    ant_colony = ACSAntColony(configuration, problem)
    start_time = time.time()
    ant_colony.run()
    end_time = time.time()
    print('耗时:{}'.format(end_time -start_time))

def antcolony_run(ant_colony):
    ant_colony.iterate(0)
    return ant_colony.best_ant.solution_components
#run()
def parallel_run():
    start_time = time.time()
    cities = load_data('a280.tsp')
    path = load_opt_solution('a280.opt.tour')
    dist_matrix = get_dist_matrix(cities)
    max_dist = np.max(dist_matrix)
    heuristic_matrix = (max_dist / (dist_matrix+1)).astype(np.float)
    configuration = AntColonyConfiguration()
    problem = TSPConstructionGraph(heuristic_matrix,configuration,dist_matrix)
    ant_colony = AntColony(configuration, problem)
    start_time = time.time()
    ant_colony.parallel_run()
    end_time = time.time()
    print('耗时:{}'.format(end_time -start_time))
    

if __name__ == '__main__':
    parallel_flag = True
    if(parallel_flag):
        parallel_run()
    else:
        run()