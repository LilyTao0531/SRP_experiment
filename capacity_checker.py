import os
import re
from sys import argv
import random
from random import randint
import numpy as np
import math
from util import parse_instance_cp
# from checker import convert_tour_to_edge
from models.model_cp import pick_most_seats, n_dist_matrix, gurobi_upperbound

# def pick_most_seats(tour, config_0_seat, seats_0, p_hat, q_hat, S_hat, C_hat, L):
#     seats_total = config_0_seat
#     satisfied = True

#     for t in tour:
#         seats_total = min(S_hat, seats_total+seats_0[t], C_hat/L  + S_hat - q_hat[t]/L)
#         # Pick up seats at the pickup location
#         if seats_total < p_hat[t]:
#             print("seats_total: ",seats_total, " Tour: ", t)
#             satisfied = False
#             return satisfied

#         seats_total = min(seats_total+seats_0[t+len(tour)-1], S_hat)
#         # Pick up seats at the delivery locaton

#     return satisfied

# get_solution_search_next(msol_all)
instance_directory = os.path.join(os.getcwd(), "new_instance_2000/")
# instance_directory = "/home/lily/srp_experiment/new_instance_2000/"
number_of_infeasible_instances = 0
for inst_name in os.listdir(instance_directory):

    if inst_name == ".DS_Store": # This is to skip any DS_Store file
        pass
    else:
        dist_V, dist_V_N1, points, q_hat, p_hat, n, S_hat, L, C_hat, config_0_seat, config_0_cargo, seats_0 = parse_instance_cp(instance_directory, inst_name)
        dist = n_dist_matrix(points)
        objective_value, tour = gurobi_upperbound(points, dist, seats_0, config_0_seat, S_hat, C_hat, q_hat, p_hat, L)
        print("Instance:", inst_name, " Objective Value:", objective_value)
        result_list = pick_most_seats(tour, config_0_seat, seats_0, p_hat, q_hat, S_hat, C_hat, L)
        if result_list:
            print(result_list)
            print(len(result_list))
            print("Passenger capacity satisfied.") 
        else:
            print("Passenger capacity NOT satisfied.")
            number_of_infeasible_instances = number_of_infeasible_instances + 1
print("Number of infeasible instances: ", number_of_infeasible_instances/len(os.listdir(instance_directory)))
print(objective_value)
