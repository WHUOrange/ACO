#-*- coding:utf-8 -*-
Local_Search_Type = {0:'LST_NONE',1:'LST_BEAT',2:'LST_ALL'}
class AntColonyConfiguration:
    def __init__(self, alpha = 1, beta = 3, pher_evap_rate = 0.5, pher_init_amount = 1,\
        num_of_ants = 200, num_of_iter = 10, local_search_type = Local_Search_Type[0]):
        self.alpha = alpha
        self.beta = beta
        self.pher_evap_rate = pher_evap_rate
        self.pher_init_amount = pher_init_amount
        self.num_of_ants = num_of_ants
        self.num_of_iter = num_of_iter
        self.local_search_type = local_search_type


class ACSAntColonyConfiguration(AntColonyConfiguration):
    def __init__(self, alpha = 1, beta = 4, pher_evap_rate = 0.1, pher_init_amount = 1,\
        num_of_ants = 10, num_of_iter = 20, local_search_type = Local_Search_Type[0],\
        q0 = 0.6, xi = 0.9):
        super().__init__(alpha , beta, pher_evap_rate, pher_init_amount,\
            num_of_ants, num_of_iter, local_search_type)
        self.q0 = q0
        self.xi = xi
