import re
import numpy as np
class City:
    def __init__(self, id, x, y):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)

def load_data(filename):
        cities = []
        with open(filename,'r') as f:
            flag = False            
            for line in f:
                if ('EOF' in line):
                    flag = False
                if flag:
                    coor = re.split(r'\s+',line.strip())
                    city = City(coor[0], coor[1], coor[2])
                    cities.append(city)
                if ('NODE_COORD_SECTION' in line):
                    flag = True
        return cities

def get_dist_matrix(cities):
    matrix = np.zeros((len(cities),len(cities)))
    for city in cities:
        for city_to in cities:
            matrix[city.id-1][city_to.id-1] = np.sqrt(np.power((city.x - city_to.x),2)\
                    +np.power((city.y - city_to.y),2))
    return matrix

def load_opt_solution(filename):
    path = []
    with open(filename,'r') as f:
        flag = False            
        for line in f:
            if ('-1' in line):
                flag = False
            if flag:
                coor = line.strip()
                path.append(int(coor))
            if ('TOUR_SECTION' in line):
                flag = True
    return path
