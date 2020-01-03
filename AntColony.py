#-*- coding:utf-8 -*-
import multiprocessing
from multiprocessing import Pool
import copy

from Ant import Ant
from AntColonyConfiguration import AntColonyConfiguration
#import functools
import ConstructionGraph
from ConstructionGraph import ConstructionGraph
from Error import Error

class AntColony:
    def __init__(self, configuration, construction_graph):
        try:
            print('模型初始化开始！')
            self.configuration = configuration
            self.construction_graph = construction_graph
            self.ants = [Ant() for i in range(self.configuration.num_of_ants)]
            self.best_ant = Ant()
            self.best_ant_no_ls = Ant()
            print('模型初始化完成！')
        except Exception:
            print('模型初始化失败！')
            print(Exception)

    def update_best_solution_no_ls(self):
        try:        
            self.ants.sort(key = lambda ant: ant.solution_score)
            if self.best_ant_no_ls.get_solution_score() >= self.ants[0].get_solution_score():
                self.best_ant_no_ls = copy.deepcopy(self.ants[0])
        except:
            print('更新（局部搜索前）最佳蚂蚁失败')

    def update_best_solution(self):
        try:
            self.ants.sort(key = lambda ant: ant.solution_score)
            if self.best_ant.get_solution_score() >= self.ants[0].get_solution_score():
                self.best_ant = copy.deepcopy(self.ants[0])
        except:
            print('更新最佳蚂蚁失败')

    def update_pheromones(self):
        self.construction_graph.evaporate_all()
        for ant in self.ants:
            self.construction_graph.release_all(ant.solution_components, ant.solution_score)

    def apply_local_search(self):
        if self.configuration.local_search_type == 'LST_NONE':
            pass
        if self.configuration.local_search_type == 'LST_BEAT':
            self.ants.sort(key = lambda ant: ant.get_solution_score())
            self.ants[0].local_search(self.construction_graph)
        if self.configuration.local_search_type == 'LST_ALL':
            for ant in self.ants:
                ant.local_search(self.construction_graph)

    def draw_solution(self):
        pass

    def iterate(self, iter_num):
        try:
            for ant in self.ants:
                ant.reset()
                ant.construct_solution(self.construction_graph, self.configuration.alpha, self.configuration.beta)
            self.update_best_solution_no_ls()
            self.apply_local_search()
            self.update_best_solution()
            self.update_pheromones()
            self.draw_solution()
            print('第{0}次迭代：迭代最佳蚂蚁分值{1};种群最佳分值{2}'.format(iter_num,self.ants[0].solution_score,self.best_ant.solution_score))
        except Error as e:
            raise e
    
    def parallel_iterate(self, ant):
        ant.reset()
        solution_info = ant.construct_solution(self.construction_graph, self.configuration.alpha, self.configuration.beta)
        return solution_info

    def update_ants(self, solution_info):        
        if(len(solution_info)==len(self.ants)):
            i = 0
            for ant in self.ants:
                ant.update_solution(solution_info[i])
                i = i+1

    def parallel_run(self):   
        try:
            process_num = multiprocessing.cpu_count()
            for i in range(self.configuration.num_of_iter):  
                pool = Pool(process_num)          
                resurlts = pool.map(self.parallel_iterate, self.ants)
                pool.close()
                pool.join()            
                self.update_ants(resurlts)
                self.update_best_solution_no_ls()
                self.apply_local_search()
                self.update_best_solution()
                self.update_pheromones()
                print('第{0}次迭代:最优{1}'.format(i,self.best_ant.solution_score))
            print('最优蚂蚁分值{}'.format(self.best_ant.solution_score))
        except Error as e:
            print('模型运行失败！错误信息：')
            print(e)
    
    def run(self):
        try:
            for i in range(self.configuration.num_of_iter):
                self.iterate(i)
            print('模型运行完成！')
            print('最佳方案为：{}'.format(self.best_ant.solution_components))
            print('最佳方案目标函数分值：{}'.format(self.best_ant.solution_score))
        except Error as e:
            print('模型运行失败！错误信息：')
            print(e)


class ACSAntColony(AntColony):
    def __init__(self, configuration, construction_graph):
        super(ACSAntColony, self).__init__(configuration, construction_graph)      
        self.q0 = configuration.q0
        self.xi = configuration.xi                #ξ  

    def update_pheromones(self):
        components = self.best_ant.solution_components
        for cpt in components:
            self.construction_graph.evaporate(cpt[0],cpt[1])
        self.construction_graph.release_all(self.best_ant.solution_components, \
            self.xi * self.configuration.pher_evap_rate * self.best_ant.solution_score)
        
          

