import os
import re
from sys import argv
import random
from random import randint
import numpy as np
import math
from models.model_cp import get_solution_detail
from util import parse_instance_cp


def convert_tour_to_edge(tour0):
    edge_li = []
    l = len(tour0)
    for i in range(l-1):
        tu = (tour0[i], tour0[i+1])
        edge_li.append(tu)
    return edge_li

def check_obj_val(obj_val, edges, arc_dist):

    check = True
    total = 0
    print(edges)
    for e in edges:
        total = arc_dist[e[0]][e[1]] + total
    total = round(total,2)
    if round(obj_val,2) != total:
        check = False

    return check

def subtour(edges,n):
    unvisited = list(range(2*n+2)) # or V_0N1
    cycle = range(2*n+3)  # initial length has 1 more city
    while unvisited:  
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for [i, j] in edges if i ==current and j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

def check_no_subtour(edges,n):
    check = True
    if len(subtour(edges,n)) < len(edges):
        check = False
    return check

def enforce_feasible_tour(tour, dist_V_0N1):
    # V_0N1 = list(dist_V_0N1.keys())
    V_0N1 = [i for i in range(len(dist_V_0N1))]
    check = True
    for i in V_0N1:
        if i not in tour:
            check = False
    if len(set(tour)) != len(tour):
        check = False
    return check

def check_seats_picked(dict_seats, tour, Q, V_0, pas_cum): 
    check = True
    for t in V_0:
        if dict_seats[tour[t]] + pas_cum[tour[t]] > Q:
            return "check_seats_picked", t
    return "check_seats_picked checked"

def enforce_vehicle_capacity(cargo_cap, pass_cap, C, S_hat,L,V_0N1):
    
    check = True

    for t in V_0N1:
        if cargo_cap[t] < 0 or cargo_cap[t] > C+S_hat*L or pass_cap[t] < 0 or pass_cap[t] > S_hat or cargo_cap[t] + pass_cap[t] > C+S_hat*L:
            check = False
            #print("t", t)
    if not check:
        print("cargo_capacity less than 0? ", cargo_cap[t] < 0)
        print("cargo_capacity larger than maximum? ", cargo_cap[t] > C+S_hat*L)
        print("passenger_capacity less than 0? ", pass_cap[t] < 0)
        print("passenger_capacity larger than maximum? ", pass_cap[t] > S_hat)
        print("Total aircraft capacity? ", cargo_cap[t] + pass_cap[t] > C+S_hat*L)
    return check

def enforce_pass_picked(tour, dict_seats, pass_cap, ro): 
    check = True
    previous_tour = tour[0]
    for t in tour[1:-1]: #End depot is not counted in ro
        # if ro[t] > pass_cap[t] + dict_seats[t]:
        if ro[t] > (pass_cap[previous_tour] + dict_seats[t]):
            check = False
        previous_tour = t
    return check

def enforce_pass_picked_checked(tour, pass_cap, ro): 
    for t in tour[:-1]: #End depot is not counted in ro
        # if ro[t] > pass_cap[t] + dict_seats[t]:
        if ro[t] > pass_cap[t]:
            return "pass_cap exceeded ", t
    return "enforce_pass_picked_checked checked"

def enforce_cargo_picked(tour, dict_seats, cargo_cap, q, L): 
    check = True
    previous_tour = tour[0]
    for t in tour[1:-1]: #End depot is not counted in ro

        # if q[t] > cargo_cap[t] - L*dict_seats[t]:
        if q[t] > (cargo_cap[previous_tour] - L*dict_seats[t]):
            check = False
        previous_tour = t
    return check

def enforce_cargo_picked_checked(tour, cargo_cap, q, L): 
    for t in tour[:-1]: #End depot is not counted in ro
        # if q[t] > cargo_cap[t] - L*dict_seats[t]:
        if q[t] > cargo_cap[t]:
            return "cargo_cap exceeded " , t
    return "enforce_cargo_picked_checked checked"

def enforce_vehicle_capacity_check(cargo_cap, pass_cap, C, Q,L,V_0N1):

    for t in V_0N1:
        if cargo_cap[t] < 0 or cargo_cap[t] > C+Q*L:
            return "cargo_cap", t
        elif pass_cap[t] < 0 or pass_cap[t] > Q:
            return "pass_cap", t
        elif cargo_cap[t] + pass_cap[t] > C+Q*L:        
            return "pass_cap and cargo_cap", t
    return "enforce_vehicle_capacity_check done"

def check_cp_output(inst_dir, csv_file, inst_name, have_solution, itvs, pi, change_of_seats):
    
    checker_dir = "/home/lily/srp_experiment/results_cp/checker"
    path = checker_dir

    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")

    name_of_file = "cp" +"_checker.txt"
    checker_file = os.path.join(checker_dir, name_of_file)  
    
    dist_V, dist_V_N1, dist_V_0N1, q_hat, p_hat, n, S_hat, L, C_hat, config_0_seat, config_0_cargo, seats_0 = parse_instance_cp(inst_dir, inst_name)
    V = list(range(1,2*n+1))
    V_minus = [(i-1) for i in V]
    V_0 = list(range(0,2*n+1))
    V_N1 = list(range(1,2*n+2))
    V_0N1 = list(range(0,2*n+2))
    

    
    with open(checker_file, 'a') as file:
        
        if not have_solution:
            file.write("\ninstance "+ inst_name + "<< infeasible >>")
        else:
            obj_val, dict_seats, tour, cargo_cap, passenger_cap, n_cargo, n_passenger = get_solution_detail(inst_name, have_solution, csv_file, itvs, pi, change_of_seats, p_hat, q_hat, n, config_0_seat, config_0_cargo)

            tour_two_depots = tour.copy()
            tour[-1] = 0 # Assign index of 0 instead of (2*n + 1) to the end depot due to the design of the checker function

            edges_two_depots = convert_tour_to_edge(tour_two_depots)

            edges = convert_tour_to_edge(tour)
            arc_dist = [[math.ceil(math.hypot(dist_V_0N1[a][0] - dist_V_0N1[b][0], dist_V_0N1[a][1] - dist_V_0N1[b][1])) for a in range(2*n + 1)]for b in range(2*n + 1)]
            
            pas_cum = n_passenger
            file.write("\n")
        
            if check_obj_val(obj_val, edges,arc_dist):
                if check_no_subtour(edges_two_depots,n):
                    if enforce_feasible_tour(tour_two_depots, dist_V_0N1):
                        if check_seats_picked(dict_seats, tour, S_hat, V, pas_cum):
                            if enforce_vehicle_capacity(cargo_cap, passenger_cap, C_hat, S_hat,L,V_minus):
                                if enforce_pass_picked(tour, dict_seats,passenger_cap, p_hat):
                                    if enforce_cargo_picked(tour, dict_seats, cargo_cap, q_hat, L):
                                        file.write("\ninstance " + inst_name + " << feasible >>") 
                                    else:
                                        _ , which_t = enforce_cargo_picked_checked(tour, cargo_cap, q_hat, L)
                                        file.write("\ninstance " + inst_name + " << invalid >> (picked up cargo exceeded at location " + str(which_t) + " )")
                                        #file.write("\ninstance " + filename + " << invalid >> (picked up cargo exceeded at location " + here + " )")

                                else:
                                    _ , which_t = enforce_pass_picked_checked(tour,  passenger_cap, p_hat)
                                    file.write("\ninstance " + inst_name + " << invalid >> (picked up passengers exceeded at location " + str(which_t) + " )")
                                    
                            else:
                                reason_t , which_t = enforce_vehicle_capacity_check(cargo_cap, passenger_cap, C_hat, S_hat,L,V_0N1)
                                file.write("\ninstance {} << invalid >> (vehicle capacity is violated at location {} due to {})".format(inst_name, str(which_t), reason_t))
                                #file.write("\nwhich_t"+ str(which_t))
                        else:
                            which_t = check_seats_picked(dict_seats, tour, S_hat, V_0, pas_cum)
                            file.write("\ninstance "+ inst_name + " << invalid >> (number of picked up seats exceeding the valid capacity)") 
                            file.write("\nwhich_t"+ str(which_t))
                        
                    else:
                        file.write("\ninstance " + inst_name + " << invalid >> (each location is not visited exactly once)")
                else:
                    file.write("\ninstance "+ inst_name + " << invalid >> (tour has a subtour)")
            else:
                file.write("\ninstance "+ inst_name + " << invalid >> (wrong objective value)")

