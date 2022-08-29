# -*- coding: utf-8 -*-
"""
Created on Feb 24, 2022

@author: arnoosh

checker for all codes
Will be run in run_file
python C:\Python\SRP\checker-new.py rand_instances_new output_m2 > C:\Python\SRP\output_m2_checker.txt
"""
#run 16_383 here

import os
import re
from sys import argv
import random
from random import randint
import numpy as np
import math

#make sure obj val is in try error

def create_dict(size, list1):
    dict1 = {}
    for i in range(size):
        dict1[i]={}
        for l in list1:
            dict1[i][l] =[]
    return dict1   



def merge_two_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def get_dist(p1, p2):
    dist2 = (p1[0]-p2[0])**2 +(p1[1]-p2[1])**2 
    dist = math.ceil(np.sqrt(dist2))
    return dist

#inst_dir = "C:/Python/SRP/rand_instances_5"
#filename = "5_426.txt"
    
#sol_dir = "C:/Python/SRP/output_m2"
#print("hellloooo")

#MBA model
#generat passenger demands randomly from 0 to 9
#r = random.randint(1,100)
# =============================================================================
# r = 100
# random.seed(r)
# ro_list = [randint(0,4) for i in range(5)]
# =============================================================================

def parseInstanceFile(inst_dir, filename):
    instanceName = os.path.join(inst_dir , filename)
    #print("inst_name",instanceName)
    #print("inst_dir",inst_dir)
    with open(instanceName,"r") as instance:
        line = instance.readline()
        nb_seed, n, Q, L, C = (int(x) for x in line.split())
        line = instance.readline()
        config_0_seat, config_0_cargo = (int(x) for x in line.split())
        line = instance.readline()
        seats_0 = line.split()
        seats_0 = [int(k) for k in seats_0]        
        dist_V = {}
        dist_v_0 = {}
        dist_v_N1 ={}
        q = {}
        ro = {}
        line = instance.readline()
        i = int(line.split()[0])
        x = int(line.split()[1])
        y = int(line.split()[2])
        q0 = int(line.split()[3]) 
        ro0 = int(line.split()[4])
        point0 = (x,y)
        dist_v_0[i] = point0 #depot node
        dist_v_N1[2*n+1] = point0
        q[i] = q0
        ro[i] = ro0
        for j in range(1,2*n+1):
            line = instance.readline()
            i = int(line.split()[0])
            x = int(line.split()[1])
            y = int(line.split()[2])
            q0 = int(line.split()[3]) 
            ro0 = int(line.split()[4])
            point0 = (x,y)
            dist_V[i] = point0
            q[i] = q0
            ro[i] = ro0
            
        dist_V_0 = merge_two_dicts(dist_V,dist_v_0) #set(V).union(v_0)
        dist_V_N1 = merge_two_dicts(dist_V,dist_v_N1)#set(V).union(v_N1) #V_{N+1}
        dist_V_0N1 = merge_two_dicts(dist_V_0,dist_v_N1)

        V = list(range(1,2*n+1))
        V_0 = list(range(0,2*n+1))
        V_N1 = list(range(1,2*n+2))
        V_0N1 = list(range(0,2*n+2))
        
        return dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0
   
#inst_dir = "C:/Python/SRP/test_rand_inst"   
#filename = "2_80.txt" 
#dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0 = parseInstanceFile(inst_dir, filename) 

#dist_V, dist_V_0N1, q, ro, n, Q, L, C = parseInstanceFile(inst_dir, filename)






#dist_V = {1:(2,1),2: (2,-1), 3:(4,1),4:(4,-1)}
#dist_V = {1:(2,1),2: (2,-1)}

#dist_v_0 = {0:(0,0)} #start and end depot node
#dist_v_N1 = {2*n+1:(0,0)}
# =============================================================================
# dist_V_0 = merge_two_dicts(dist_V,dist_v_0) #set(V).union(v_0)
# dist_V_N1 = merge_two_dicts(dist_V,dist_v_N1)#set(V).union(v_N1) #V_{N+1}
# dist_V_0N1 = merge_two_dicts(dist_V_0,dist_v_N1)
# 
# 
# 
# V = list(range(1,2*n+1))
# V_0 = list(range(0,2*n+1))
# V_N1 = list(range(1,2*n+2))
# V_0N1 = list(range(0,2*n+2))
# =============================================================================

def get_arc_dist(n, dist_V_0N1):
    arc_dist = {}
        
    for i in range(2*n+2):
        for j in range(2*n+2):
            if i != j:
                p1 = dist_V_0N1[i]
                p2 = dist_V_0N1[j]
                arc_dist[(i,j)] = get_dist(p1 , p2) #error here, if changed to [] again error
                #maybe change all the edges to () or use another data type for arc_dist
    return arc_dist

#the following two functions are similar, but the next one returns integer dict from
# string dict the second one returns float dict.
def convert_str_to_dict(dict_str):
    #print("dict_str", dict_str)
    dict_str = dict_str.replace(" ","").replace("{","").replace("}","")
    dict_str_list = dict_str.split(",")
    dict_final = {}
    for i in dict_str_list:
        key_val = i.split(":")
        #print("key_val", key_val)
        key = int(float(key_val[0]))
        val = int(float(key_val[1]))
        dict_final[key] = val
    return dict_final

        

def convert_str_to_dict_float(dict_str):
    #print("dict_str", dict_str)
    dict_str = dict_str.replace(" ","").replace("{","").replace("}","")
    dict_str_list = dict_str.split(",")
    dict_final = {}
    for i in dict_str_list:
        key_val = i.split(":")
        #print("key_val", key_val)
        key = float(key_val[0])
        val = float(key_val[1])
        dict_final[key] = val
    return dict_final


# =============================================================================
#         
# 
# def convert_str_tuple_to_list(list_str):
#     list_final = []
#     subs = list_str.strip().replace("[","").replace("]","").replace(" ", "").split("(")
#     for s in subs:
#         if len(s) >=1:
#             tmp_sub = s.split(")")
#             p1_p2_list = tmp_sub[0].split(',')
#             e = (int(p1_p2_list[0]), int(p1_p2_list[1]))
#             list_final.append(e)
#     return list_final
# 
# =============================================================================
    

def convert_str_to_list(list_str):
    list_str = list_str.replace("[","").replace("]","")
    list_str_list = list_str.split(",")
    list_final = []
    for i in list_str_list:
        el = int(i) #float(i)
        list_final.append(el)
    return list_final


    

def parseSolutionFile(sol_dir, filename):
    #for filename in os.listdir(sol_dir):
        #if filename != "delta_MIP_150_2000_80":
    dict_seats = {}
    dict_seats_float = {}
    obj_val = math.inf
    tour = []
    edges = []

    f = open(os.path.join(sol_dir,filename))
    #dict_seats, dict_seats_float, tour, obj_val = 0,0,0,0
    for line in f: 
        #print("line", line)
        if "Model is infeasible" in line:
            return "infeasibility"
        elif "No solution is found" in line: #Infeasibility is not proved but no solution is returned either.
            return "No solution"
        else:
            if "Optimal tour:" in line:
                tour_str = re.search('Optimal tour: (\[.+\])', line).group(1)
                tour = convert_str_to_list(tour_str) 
                
                #print("Optimal tour done")
            elif "Optimal cost:" in line:
                #line = line.replace(" ","").replace("\n","")
                obj_val = float(line.split("Optimal cost:")[1])
                #obj_val = loat(re.search('Optimal cost: ({.+})', line).group(1))
                obj_val = round(obj_val,6)
                
                #print("Optimal cost:", obj_val)
            elif "Seats changes" in line:
                # print("Seats changes", line)
                dict_seats_str = re.search('Seats changes: ({.+})', line).group(1)
                dict_seats = convert_str_to_dict(dict_seats_str) 
                dict_seats_float = convert_str_to_dict_float(dict_seats_str) 
                #print("Seats changes done", dict_seats_float, dict_seats)
    return dict_seats, dict_seats_float, tour, obj_val
                  
# =============================================================================
#         else:
#             print("line", line)
#         return dict_seats, dict_seats_float, tour, obj_val
#         #for checking
# =============================================================================
        #error here, fix
# =============================================================================
#         if "Remaining cargo space" in line: 
#             dict_cargo_space_str = re.search('Remaining cargo space: ({.+})', line).group(1)
#             dict_cargo_space = convert_str_to_dict_float(dict_cargo_space_str)
#             
#         if "Remaining passenger space" in line: 
#             dict_pass_space_str = re.search('Remaining passenger space: ({.+})', line).group(1)
#             dict_pass_space = convert_str_to_dict_float(dict_pass_space_str)
# =============================================================================
    
    #return dict_cargo_space, dict_pass_space, dict_seats, dict_seats_float, tour, obj_val
            

#sol_dir = "C:/Python/SRP/test_results_m2_total_cap"   
#filename = "2_82.txt" 


#dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(inst_dir, sol_dir, filename) 



   
#dict_cargo_space, dict_pass_space, dict_seats, tour, obj_val = parseInstanceFile(sol_dir, filename)


def convert_tour_to_edge(tour0):
    edge_li = []
    l = len(tour0)
    for i in range(l-1):
        tu = (tour0[i], tour0[i+1])
        edge_li.append(tu)
    return edge_li



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



def check_obj_val(obj_val, edges, arc_dist):

    check = True
    total = 0
    for e in edges:
        total = arc_dist[e] + total
    total = round(total,2)
    if round(obj_val,2) != total:
        check = False

    return check


def check_obj_val_check(obj_val, edges, arc_dist):
    print("edges here", edges)
    total = 0
    for e in edges:
        total = arc_dist[e] + total
        print("e", e)
        print("total", total)
    total = round(total,2)

    return total

def check_no_subtour(edges,n):
    check = True
    if len(subtour(edges,n)) < len(edges):
        check = False
    return check
    

def enforce_feasible_tour(tour, dist_V_0N1):
    V_0N1 = list(dist_V_0N1.keys())
    check = True
    for i in V_0N1:
        if i not in tour:
            check = False
    if len(set(tour)) != len(tour):
        check = False
    return check

def get_cargo_cap(tour, dict_seats,q, config_0_cargo,L, V_N1): #cargo at the arrival of each location, it is cargo empty cap
    cargo_cap= {}
    cargo_cap[0] = config_0_cargo #C
    for t in V_N1:
        cargo_cap[tour[t]] = cargo_cap[tour[t-1]] -L*dict_seats[tour[t-1]] -q[tour[t-1]] 
        
    return cargo_cap
    


def get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1): #remaining passenger capacity at the arrival at location i
    pass_cap= {}
    pass_cap[0] = config_0_seat #Q
    for t in V_N1: #if we enumerate over tour, we could replace tour[t] with t
        pass_cap[tour[t]] = pass_cap[tour[t-1]] +dict_seats[tour[t-1]] - ro[tour[t-1]]
    
    return pass_cap
# =============================================================================
#         if ro[tour[t-1]] < 0 :
#             pass_cap[tour[t]] = pass_cap[tour[t-1]] +dict_seats[tour[t-1]] - ro[tour[t-1]]
#         else:
#             pass_cap[tour[t]] = pass_cap[tour[t-1]] +dict_seats[tour[t-1]] - ro[tour[t-1]]
# =============================================================================
            
    

#to make sure we did not exceed passengers capacity when picking up passengers 
def enforce_pass_picked(tour, dict_seats, pass_cap, ro): 
    check = True
    for t in tour[:-1]: #End depot is not counted in ro
        if ro[t] > pass_cap[t] + dict_seats[t]:
            check = False
    return check
        

def enforce_pass_picked_checked(tour, dict_seats, pass_cap, ro): 
    for t in tour[:-1]: #End depot is not counted in ro
        if ro[t] > pass_cap[t] + dict_seats[t]:
            return "pass_cap exceeded ", t
    return "enforce_pass_picked_checked checked"


def enforce_cargo_picked(tour, dict_seats, cargo_cap, q, L): 
    check = True
    for t in tour[:-1]: #End depot is not counted in ro
        if q[t] > cargo_cap[t] - L*dict_seats[t]:
            check = False
    return check

def enforce_cargo_picked_checked(tour, dict_seats, cargo_cap, q, L): 
    for t in tour[:-1]: #End depot is not counted in ro
        if q[t] > cargo_cap[t] - L*dict_seats[t]:
            return "cargo_cap exceeded " , t
    return "enforce_cargo_picked_checked checked"
  
    

def enforce_vehicle_capacity(cargo_cap, pass_cap, C, Q,L,V_0N1):
    
    check = True

    for t in V_0N1:
        if cargo_cap[t] < 0 or cargo_cap[t] > C+Q*L or pass_cap[t] < 0 or pass_cap[t] > Q or cargo_cap[t] + pass_cap[t] > C+Q*L:
            check = False
            #print("t", t)
    return check

def enforce_vehicle_capacity_check(cargo_cap, pass_cap, C, Q,L,V_0N1):

    for t in V_0N1:
        if cargo_cap[t] < 0 or cargo_cap[t] > C+Q*L:
            return "cargo_cap", t
        elif pass_cap[t] < 0 or pass_cap[t] > Q:
            return "pass_cap", t
        elif cargo_cap[t] + pass_cap[t] > C+Q*L:        
            return "pass_cap and cargo_cap", t
    return "enforce_vehicle_capacity_check done"



def check_sol_cap(cargo_cap, dict_cargo_space, pass_cap, dict_pass_space, V_0N1):
    check = True
    for i in V_0N1:
        if dict_cargo_space[i] != cargo_cap[i] or dict_pass_space[i] != pass_cap[i]:
            check = False
    return check

def cumulative_demand(tour, q, ro, V):
    cargo_cum = {}
    cargo_cum[0] = 0
    pas_cum = {}
    pas_cum[0] = 0
    #print("tour", tour)
    for t in V:
        cargo_demand = q[tour[t]]
        pass_demand = ro[tour[t]]
        cargo_cum[tour[t]] = cargo_cum[tour[t-1]]+ cargo_demand
        pas_cum[tour[t]] = pas_cum[tour[t-1]]+ pass_demand
    return cargo_cum, pas_cum


#checks that number of picked up seats plus number of passengers currently on aircraft does not exceed the seat capacity
def check_seats_picked(dict_seats, tour, Q, V_0, pas_cum): 
    check = True
    for t in V_0:
        if dict_seats[tour[t]] + pas_cum[tour[t]] > Q:
            return "check_seats_picked", t
    return "check_seats_picked checked"

def check_seats_picked_check(dict_seats, tour, Q, V_0, pas_cum): 
    for t in V_0:
        if dict_seats[tour[t]] + pas_cum[tour[t]] > Q:
            check = False
    return check    

def compare_dicts(dict1,dict2):
    check = True
    if dict1.keys() == dict2.keys():
        for k in dict1.keys():
            diff = dict1[k]-dict2[k]
            if diff > 0.5:
                check = False
    else:
        check = False
        #print("different keys")
    return check


def sorted_dict(dict0, list0):
    ordered_dict_items = [(k,dict0[k]) for k in list0]
    return ordered_dict_items


# =============================================================================
# =============================================================================
# # 
# # #inst_dir = "C:/Python/SRP/test_rand_inst"  
# # inst_dir = "C:/Python/SRP/new_instances"  
# # 
# # sol_dir = "C:/Python/SRP/test_results_m2_total_cap"   
# # #sol_dir = "C:/Python/SRP/test_results_m3"   
# # 
# # filename = "10_733.txt" 
# # #filename = "4_821.txt" 
# # 
# # 
# # dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0 = parseInstanceFile(inst_dir, filename)
# # V = list(range(1,2*n+1))
# # V_0 = list(range(0,2*n+1))
# # V_N1 = list(range(1,2*n+2))
# # V_0N1 = list(range(0,2*n+2))
# #  
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # 
# # 
# # if parseSolutionFile(inst_dir,sol_dir, filename) == "infeasibility":
# #     print("\ninstance ", filename , "<< infeasible >>")
# # else:
# #     dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(inst_dir,sol_dir, filename)
# # 
# #     edges = convert_tour_to_edge(tour)
# #     #print(edges)
# #     arc_dist = get_arc_dist(n, dist_V_0N1)
# #     cargo_cap = get_cargo_cap(tour, dict_seats,q, config_0_cargo ,L, V_N1)
# #     pass_cap = get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1)
# #     cargo_cum, pas_cum = cumulative_demand(tour, q, ro, V)
# #     #print("cargo_cap", cargo_cap)
# #     if check_obj_val(obj_val, edges,arc_dist):
# #         if check_no_subtour(edges,n):
# #             if enforce_feasible_tour(tour, dist_V_0N1):
# #                 if compare_dicts(dict_seats, dict_seats_float):
# #                     if check_seats_picked(dict_seats, tour, Q, V_0, pas_cum):
# #                         if enforce_vehicle_capacity(cargo_cap, pass_cap, C, Q,L,V_0N1):
# #                             if enforce_pass_picked(tour, dict_seats, pass_cap, ro):
# #                                 if enforce_cargo_picked(tour, dict_seats, cargo_cap, q, L):
# #                                     print("\ninstance " , filename , " << feasible >>") 
# #                                 else:
# #                                     _ , which_t = enforce_cargo_picked_checked(tour, dict_seats, cargo_cap, q, L)
# #                                     print("\ninstance " + filename + " << invalid >> (picked up cargo exceeded at location " + str(which_t) + " )")
# #                                     #file.write("\ninstance " + filename + " << invalid >> (picked up cargo exceeded at location " + here + " )")
# #      
# #                             else:
# #                                 _ , which_t = enforce_pass_picked_checked(tour, dict_seats, pass_cap, ro)
# #                                 print("\ninstance " , filename , " << invalid >> (picked up passengers exceeded at location " , str(which_t) , " )")
# #                                
# #                         else:
# #                             reason_t , which_t = enforce_vehicle_capacity_check(cargo_cap, pass_cap, C, Q,L,V_0N1)
# #                             print("\ninstance {} << invalid >> (vehicle capacity is violated at location {} due to {})".format(filename, str(which_t), reason_t))
# #                             #file.write("\nwhich_t"+ str(which_t))
# #                     else:
# #                         which_t = check_seats_picked(dict_seats, tour, Q, V_0, pas_cum)
# #                         print("\ninstance ", filename , " << invalid >> (number of picked up seats exceeding the valid capacity)") 
# #                         print("\nwhich_t", str(which_t))
# #                 else:
# #                     print("\ninstance ", filename , " << invalid >> (number of seats are far from an integer number)")                  
# #                          
# #             else:
# #                 print("\ninstance " , filename , " << invalid >> (each location is not visited exactly once)")
# #         else:
# #             print("\ninstance ", filename , " << invalid >> (tour has a subtour)")
# #     else:
# #         total = check_obj_val_check(obj_val, edges, arc_dist)
# #         print("\ninstance ", filename , " << invalid >> (wrong objective value)")
# #         print("total is {} but objective value is {}".format(total, obj_val))
# #     
# #     
# =============================================================================
# 
# =============================================================================
# =============================================================================
# 
# try:
#     inst_dir = "C:/Python/SRP/new_instances"  
#     sol_dir = "C:/Python/SRP/test_results_m2_total_cap"   
#     filename = "16_383.txt" 
#     print(filename)
#     dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0 = parseInstanceFile(inst_dir, filename)
#     V = list(range(1,2*n+1))
#     V_0 = list(range(0,2*n+1))
#     V_N1 = list(range(1,2*n+2))
#     V_0N1 = list(range(0,2*n+2))
#     
#     dict_cargo_space, dict_pass_space, dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(inst_dir,sol_dir, filename)
#     edges = convert_tour_to_edge(tour)
#     arc_dist = get_arc_dist(n, dist_V_0N1)
#     #cargo_cap = get_cargo_cap(tour, dict_seats,q, config_0_cargo ,L, V_N1)
#     #pass_cap = get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1)
#     
#     
#     cargo_cum, pas_cum = cumulative_demand(tour, q, ro, V)
#  
#     if check_obj_val(obj_val, edges,arc_dist):
#         if check_no_subtour(edges):
#             if enforce_feasible_tour(tour, dist_V_0N1):
# 
#                 if compare_dicts(dict_seats, dict_seats_float):
#                     if check_seats_picked(dict_seats, V_0, pas_cum):
#                         print("instance", filename + " << feasible >>") 
#                     else: 
#                         print("instance", filename + " << invalid >> (number of picked up seats exceeding the valid capacity) ") 
#                 else:
#                     print("instance", filename + " << invalid >> (number of seats are far from an integer number) ")                  
#                 
#             else:
#                 print("instance", filename + " << invalid >> (each location is not visited exactly once)")
#         else:
#             print("instance", filename + " << invalid >> (tour has a subtour)")
#     else:
#         print("instance", filename + " << invalid >> (wrong objective value)")
# except:
#     print("instance", filename,"<< infeasible >>")
# 
# =============================================================================

# =============================================================================
#     dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(inst_dir,sol_dir, filename)
#     edges = convert_tour_to_edge(tour)
#     arc_dist = get_arc_dist(n, dist_V_0N1)
#     cargo_cap = get_cargo_cap(tour, dict_seats,q, config_0_cargo ,L, V_N1)
#     pass_cap = get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1)
#     
#     print("here",enforce_cargo_picked(tour, dict_seats, cargo_cap, q, L))
# 
# =============================================================================


def check_code(inst_dir, sol_dir, filename, model_name):
    
    checker_dir = os.path.join(sol_dir, "checker") 
    path = checker_dir
    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")
    name_of_file = model_name +"_checker.txt"
    #name_of_file = model_name +"_checker_" + filename
    checker_file = os.path.join(checker_dir, name_of_file)  
    
    dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0 = parseInstanceFile(inst_dir, filename)
    V = list(range(1,2*n+1))
    V_0 = list(range(0,2*n+1))
    V_N1 = list(range(1,2*n+2))
    V_0N1 = list(range(0,2*n+2))
    

    
    with open(checker_file, 'a') as file:
        file.write("\n\nchecking "+ sol_dir + "_" + filename )
        if parseSolutionFile(sol_dir, filename) == "infeasibility":
            file.write("\ninstance "+ filename + "<< infeasible >>")
        elif parseSolutionFile(sol_dir, filename) == "No solution":
            file.write("\ninstance "+ filename + "<< feasible >>")
        else:
            dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(sol_dir, filename)
            edges = convert_tour_to_edge(tour)
            arc_dist = get_arc_dist(n, dist_V_0N1)
            cargo_cap = get_cargo_cap(tour, dict_seats,q, config_0_cargo ,L, V_N1)
            pass_cap = get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1)
            #file.write("\nDemand cargo "+str(q) + "\nDemand passengers "+ str(ro) +"\nn "+str(n) +"\nConfig_0_seat " 
                      # +str(config_0_seat) + "\nconfig_0_cargo " + str(config_0_cargo))
            #file.write("\nC "+str(C) + "\nQ "+ str(Q) + "\nL " +str(L))
            #file.write("\n\nTour " + str(tour)+ "\nSeats " + str(sorted_dict(dict_seats, tour[:-1]))) #The end-depot is not considered in the m2_total_cap model 
            #file.write("\nDemand cargo "+str(sorted_dict(q, tour[:-1])) + "\nDemand passengers "+ str(sorted_dict(ro, tour[:-1]))) 
            #file.write("\nCargo Cap "+ str(sorted_dict(cargo_cap, tour)) + "\nPassenger Cap "+ str(sorted_dict(pass_cap, tour)))
            
            #file.write("\nObj Val "+ str(obj_val))
            
            cargo_cum, pas_cum = cumulative_demand(tour, q, ro, V)
            file.write("\n")
        
            if check_obj_val(obj_val, edges,arc_dist):
                if check_no_subtour(edges,n):
                    if enforce_feasible_tour(tour, dist_V_0N1):
                        if compare_dicts(dict_seats, dict_seats_float):
                            if check_seats_picked(dict_seats, tour, Q, V_0, pas_cum):
                                if enforce_vehicle_capacity(cargo_cap, pass_cap, C, Q,L,V_0N1):
                                    if enforce_pass_picked(tour, dict_seats, pass_cap, ro):
                                        if enforce_cargo_picked(tour, dict_seats, cargo_cap, q, L):
                                            file.write("\ninstance " + filename + " << feasible >>") 
                                        else:
                                            _ , which_t = enforce_cargo_picked_checked(tour, dict_seats, cargo_cap, q, L)
                                            file.write("\ninstance " + filename + " << invalid >> (picked up cargo exceeded at location " + str(which_t) + " )")
                                            #file.write("\ninstance " + filename + " << invalid >> (picked up cargo exceeded at location " + here + " )")

                                    else:
                                        _ , which_t = enforce_pass_picked_checked(tour, dict_seats, pass_cap, ro)
                                        file.write("\ninstance " + filename + " << invalid >> (picked up passengers exceeded at location " + str(which_t) + " )")
                                       
                                else:
                                    reason_t , which_t = enforce_vehicle_capacity_check(cargo_cap, pass_cap, C, Q,L,V_0N1)
                                    file.write("\ninstance {} << invalid >> (vehicle capacity is violated at location {} due to {})".format(filename, str(which_t), reason_t))
                                    #file.write("\nwhich_t"+ str(which_t))
                            else:
                                which_t = check_seats_picked(dict_seats, tour, Q, V_0, pas_cum)
                                file.write("\ninstance "+ filename + " << invalid >> (number of picked up seats exceeding the valid capacity)") 
                                file.write("\nwhich_t"+ str(which_t))
                        else:
                            file.write("\ninstance "+ filename + " << invalid >> (number of seats are far from an integer number)")                  
                        
                    else:
                        file.write("\ninstance " + filename + " << invalid >> (each location is not visited exactly once)")
                else:
                    file.write("\ninstance "+ filename + " << invalid >> (tour has a subtour)")
            else:
                file.write("\ninstance "+ filename + " << invalid >> (wrong objective value)")


# =============================================================================
# 
# 
# inst_dir = "C:/Python/SRP/test_rand_inst"  
# sol_dir = "C:/Python/SRP/test_results_m2"   
# filename = "4_335.txt" 
# model_name = "m2"
# 
# check_code(inst_dir, sol_dir, filename, model_name)
# =============================================================================

# =============================================================================
# 
#         
# if __name__ == '__main__':
#     file_path = "C:/Python/SRP"
# 
#     sol_dir = os.path.join(file_path,argv[2])#'output_MIP_m3/' #for my laptop
#     inst_dir = os.path.join(file_path, argv[1])#'inst_MIP/' #for my laptop
#     #for lab system
#     #sol_dir = "~/Research/Python/fleet/MIP/inst_MIP_mba" #for lab system
#     #inst_dir = "~/Research/Python/fleet/MIP/solve_MIP_mba" #for lab system
#     
#     for filename in os.listdir(sol_dir):
#             dist_V, dist_V_0N1, q, ro, n, Q, L, C, config_0_seat, config_0_cargo, seats_0 = parseInstanceFile(inst_dir, filename)
#             V = list(range(1,2*n+1))
#             V_0 = list(range(0,2*n+1))
#             V_N1 = list(range(1,2*n+2))
#             V_0N1 = list(range(0,2*n+2))
#             try:
#                 dict_cargo_space, dict_pass_space, dict_seats, dict_seats_float, tour, obj_val = parseSolutionFile(inst_dir,sol_dir, filename)
#                 edges = convert_tour_to_edge(tour)
#                 arc_dist = get_arc_dist(n, dist_V_0N1)
#                 cargo_cap = get_cargo_cap(tour, dict_seats,q, config_0_cargo ,L, V_N1)
#                 pass_cap = get_pass_cap(tour, dict_seats, ro, config_0_seat, V_N1)
#                 
#                 
#                 cargo_cum, pas_cum = cumulative_demand(tour, q, ro, V)
#  
#                 if check_obj_val(obj_val, edges,arc_dist):
#                     if check_no_subtour(edges):
#                         if enforce_feasible_tour(tour, dist_V_0N1):
#                             if enforce_vehicle_capacity(cargo_cap, pass_cap, C, Q,L,V_0N1):
#                                 if check_sol_cap(cargo_cap, dict_cargo_space, pass_cap, dict_pass_space, V_0N1):                                         
#                                     if compare_dicts(dict_seats, dict_seats_float):
#                                         if check_seats_picked(dict_seats, V_0N1, pas_cum):
#                                             print("instance", filename + " << feasible >>") 
#                                         else: 
#                                             print("instance", filename + " << invalid >> (number of picked up seats exceeding the valid capacity) ") 
#                                     else:
#                                         print("instance", filename + " << invalid >> (number of seats are far from an integer number) ")                  
#                                 else:
#                                     print("instance", filename + " << invalid >> (the actual and the solution vehicle remaining capacity doesn't match)") 
#                                     print(cargo_cap, '\n', dict_cargo_space)
#                             else:
#                                 print("instance", filename + " << invalid >> (vehicle capacity is violated)")
#                         else:
#                             print("instance", filename + " << invalid >> (each location is not visited exactly once)")
#                     else:
#                         print("instance", filename + " << invalid >> (tour has a subtour)")
#                 else:
#                     print("instance", filename + " << invalid >> (wrong objective value)")
#             except:
#                 print("instance", filename,"<< infeasible >>")
#             
#             
#             
#         
# =============================================================================




          