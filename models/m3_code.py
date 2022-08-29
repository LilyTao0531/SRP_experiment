# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 11:43:29 2021

@authors: Arnoosh 
to run in anaconda 
(for new_inst_dir = "C:/Python/SRP/new_instances"): 
    cd C:\Python\SRP 
    python m3-run.py 5_426.txt > C:\Python\SRP\output_m3\5_426.txt
    
"""
#update it after updating m3

import pandas as pd
import numpy as np
from gurobipy import *
from itertools import combinations
import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB
import time
import os, sys
from sys import argv
from models.model_cp import n_dist_matrix, pick_most_seats
from get_upperbound import gurobi_upperbound
from util import parse_instance_cp


def solve_m3(inst_dir, sol_dir_model, inst_name, time_lim):

    #new_inst_dir = "C:/Python/SRP/test_rand_inst"
    # new_inst_dir = "/home/lily/Cplex_copy/new_instance"
    new_inst_dir = inst_dir
    name_of_file =  inst_name#argv[1]#"5_426.txt" #"5_34_c109.txt" #"5-101-"+str(r) argv[1]#
    
    file_inst = os.path.join(new_inst_dir, name_of_file)   
    
    
    
    path = sol_dir_model
    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")
    result_file = os.path.join(sol_dir_model, name_of_file) 
    
    # instanceName = file_inst

# =============================================================================
# new_inst_dir = "C:/Python/SRP/test_rand_inst"
# name_of_file =  argv[1]#"2_451.txt" #"5_34_c109.txt" #"5-101-"+str(r) argv[1]#argv[1] #wrong "5_682.txt"
# 
# file_inst = os.path.join(new_inst_dir, name_of_file)   
# 
# instanceName = file_inst
# =============================================================================

    def get_dist(p1, p2):
        dist2 = (p1[0]-p2[0])**2 +(p1[1]-p2[1])**2 
        dist = math.ceil(np.sqrt(dist2))
        return dist
    
    dist_V, dist_V_N1, dist_V_0N1, q_hat, pi_hat, n, S_hat, L, C_hat, config_0_seat, config_0_cargo, seats_0 = parse_instance_cp(inst_dir, inst_name)
    
    q_hat.append(0)
    pi_hat.append(0)
    
    
    V = list(range(1,2*n+1))
    V_0 = list(range(0,2*n+1))
    V_N1 = list(range(1,2*n+2))
    V_0N1 = list(range(0,2*n+2))
    
    arc_dist = {}
    
    
    for i in range(2*n+2):
        for j in range(2*n+2):
            if i != j:
                p1 = dist_V_0N1[i]
                p2 = dist_V_0N1[j]
                arc_dist[(i,j)] = math.ceil(get_dist(p1 , p2))
    
    
    

    
    
    arcs = list(arc_dist.keys())  
    
    P = list(range(1,n+1))#dict(list(V.items())[:n]) #pickup vertices
    D = list(range(n+1,2*n+1)) #dict(list(V.items())[n:]) #delivery vertices
    
    
    #K = [i for i in range(1,n+1)]#list(q.keys())
    
    K = C_hat + S_hat*L
      
    Big_M = len(V)
    Big_M_cargo = C_hat+2*S_hat*L
    Big_M_passenger = 2*S_hat
    
                
    #time_lim = 1000
    S_0 = seats_0
    #S_0 = 0 #for now there are no seats at bases, and these are added as upperbound, when variable I think they be added as constraints
    
    start_time = time.time()

    
    m = Model("SRP-TSP")
    vars = m.addVars(arcs, V_0N1,vtype=GRB.BINARY, name='vars') #location j follows location i at position t in the tour
    y = m.addVars(V_0N1, V_0N1,vtype=GRB.BINARY, name='y') #location i is visited at position t of the tour
    
    u = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='u') #remaining cargo space
    w = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='w') #remaining passenger seats
    s = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = -S_hat, name='s') #number of seats picked up or stored at base i (positive or negative)
    #use lb = -S_hat-1 instead of -S_hat, as the later makes the ppi_hatblem infeasible
    pi = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='pi') #number of passengers in the aircraft when leaving location j
    q = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L, name='q') #kg of cargo in the aircraft when leaving location i
    
    #initial values of t, u and y (since definition of u in VRP and SRP are different the initial values will be different)
    
    m.addConstr(y[0,0] == 1)
    m.addConstr(y[2*n+1,2*n+1] == 1)
    m.addConstr(u[0] == config_0_cargo)
    m.addConstr(w[0] == config_0_seat)
    
    
    
    for t in V:
        m.addConstr(y[0,t] ==0,"initial_var_y"+str(t))
        
    #how to make the model to visit location 5
    for t in V_0:
        m.addConstr(sum(y[i,t] for i in V_0) ==1,"time_slot_unique_location"+str(t))
        
    
    for i in V:
        m.addConstr(sum(y[i,t] for t in V) ==1,"visited_"+str(i))
    
    for t in V_N1:
        m.addConstr(w[t] == w[t-1]+ s[t-1] - sum(y[i,t-1]*pi_hat[i] for i in V), "passenger_demand_fulfillment_"+ str(t))
    
    for t in V_N1:
        m.addConstr(u[t] == u[t-1]-L*s[t-1] - sum(y[i,t-1]*q_hat[i] for i in V), "cargo_demand_fulfillment_"+ str(t))

    
      
        
    
    
        
    #define set of requests separately, so that each of them has pickup and delivery    
    #m.addConstr(sum(t*y[i,t] for t in V) - sum(t*y[i,t] for t in V)   <= -1,"precedence_const"+str(t))
     
    for l in P: #K
        m.addConstr(sum(t*y[l,t] for t in V ) - sum(t*y[l+n,t] for t in V ) <= -1, "precedence_commodity"+str(l))
    
    # =============================================================================
    # for t in V:
    #     m.addConstr(u[t]+ L*w[t] >= sum(y[i,t]*q_hat[i] for i in V) + L*sum(y[i,t]*pi_hat[i] for i in V), "u_w_relationship_lb"+ str(t))
    #     
    # for t in V:
    #     m.addConstr(u[t]+ L*w[t] <= C_hat+S_hat*L, "u_w_relationship_ub"+ str(t))
    # 
    # =============================================================================
    
    for t in V:
        m.addConstr(pi[t] + w[t] <= S_hat , "pi_w_relationship_lb"+ str(t))
    
# =============================================================================
#     for t in V:
#          m.addConstr(u[t]+ L*w[t] <= K, "u_w_relationship_ub"+ str(t))
# =============================================================================
     
        
    for t in V:
        m.addConstr(q[t]+ u[t]+ L*w[t]+ L*pi[t] <= K , "pi_w_relationship_ub"+ str(t))
     
    
    for t in V_0N1:
        m.addConstr(-w[t] <= s[t], "seats_lb_"+ str(t))
    
    
    
    for t in V_0N1:
        m.addConstr( s[t] <= sum(S_0[i]*y[i,t] for i in V_0 ) , "seats_ub_"+ str(t))
    
    
    
    # pi constraints
    
      
    pi[0] == 0
    for t in V_N1:
        m.addConstr(pi[t] == pi[t-1] +  sum(pi_hat[i]*y[i,t-1] for i in V ), "current_pass"+str(t)) 
    
# =============================================================================
#     for t in V_0:
#         m.addConstr(pi[t]+pi_hat[t]+ s[t] <= S_hat, "max_seats"+str(i)) 
#     
# =============================================================================
    
# =============================================================================
#     
#     for t in V_0:
#         m.addConstr(w[t]+pi[t]-pi_hat[t]+s[t] <= S_hat, "max_seats"+str(t)) 
#     
# =============================================================================
    
# =============================================================================
#     for t in V_0:
#         m.addConstr(pi[t]+pi_hat[t] <= S_hat, "max_seats"+str(i)) 
#     
# =============================================================================
    
    
    q[0] == 0
    for t in V_N1:
        m.addConstr(q[t] == q[t-1] +  sum(q_hat[i]*y[i,t-1] for i in V ), "current_cargo"+str(t)) 
    
            
    for i in V_0:
        for t in V_0:
            m.addConstr(y[i,t] - sum(vars[i,j,t] for j in V_0N1 if j != i)==0, "y-i-relationship--exiting-from-i"+str(i)+","+str(t))
    
    for j in V_0N1:
        for t in V_N1:
            m.addConstr(y[j,t] - sum(vars[i,j,t-1] for i in V_0  if j != i)==0, "y-j-relationship--entering-to-j"+str(j)+","+str(t))
            
    
    #-----------------------------------
    
    
    
    for t in V_0N1:
        m.addConstr( s[t] <= S_hat, "s_ub"+ str(t))
        
    for t in V_N1:
        m.addConstr( w[t] <= S_hat, "w_ub"+ str(t))
    
    
    for t in V_N1:
        m.addConstr( u[t] <= K, "u_ub"+ str(t))
    
    
    
    #---------------------------------
    # Add initial solution
    # Add arcs of the solution to the model
    dist = n_dist_matrix(dist_V_0N1)
    objective_value, sol_upperbound = gurobi_upperbound(dist_V_0N1, dist, seats_0, config_0_seat, S_hat, C_hat, q_hat, pi_hat, L)
    
    z = sum(sum(vars[i,j,t] for t in V_0)*arc_dist[(i,j)] for i in V_0 for j in V_N1 if i !=j)
    m.addConstr(z <= objective_value)   
        
    #---------------------------------   
    m.setObjective(z,GRB.MINIMIZE)
    

    # Fill all the y(i,t) and z(i, j,t) with 0s first.
    for i in range(2*n + 2):
        for t in range(2*n +2):
            y[i,t].start = 0
            for j in range(2*n + 2):
                if i!= j:
                    vars[i,j,t].start = 0
    
    start_node = 0
    for i in range(len(sol_upperbound)):
        if i != 0:
            y[sol_upperbound[i],i*2-1].start = 1
            vars[start_node, sol_upperbound[i], i*2-2].start = 1
            y[sol_upperbound[i]+n,i*2].start = 1
            vars[sol_upperbound[i], sol_upperbound[i]+n, i*2-1].start = 1
            start_node = sol_upperbound[i]+n
    
    y[0,0].start = 1
    y[2*n+1, 2*n+1].start = 1
    vars[start_node, 2*n+1, 2*n].start = 1

    # Add seats changes of the solution to the model
    actual_changes_seats = pick_most_seats(sol_upperbound, config_0_seat, seats_0, pi_hat, q_hat, S_hat, C_hat, L)

    for i in range(len(sol_upperbound)):
        if i == 0:
            s[0].start = actual_changes_seats[i]
        else:
            s[2*i-1].start = actual_changes_seats[2*i-1]
            s[2*i].start = actual_changes_seats[2*i]
    
    m.update()
       

    time_solution = [(0,objective_value)]

    def get_time_feas(model, where):
        if where == GRB.Callback.MIPSOL:
            print("time to find feasible solution is", model.cbGet(GRB.Callback.RUNTIME))
            time_solution.append((model.cbGet(GRB.Callback.RUNTIME), model.cbGet(GRB.Callback.MIPSOL_OBJBST)))

    # V = [1,2,3,4,5,6]
    # V_0 = [0,1,2,3,4,5,6]
    # V_N1 = [1,2,3,4,5,6,7]
    # V_0N1 = [0,1,2,3,4,5,6,7]


    #sys.stdout = open(result_file, "w")
    
    #m.setParam('TimeLimit', time_lim)
    
    #m.Params.LogToConsole = 0
    #m.Params.OutputFlag = 0 #equivalent to previous one
    m.Params.Threads = 4
    m.Params.TimeLimit = time_lim
    m.Params.OptimalityTol = 1e-6
    m.params.FeasibilityTol = 1e-6
    
    m.Params.LogFile = result_file

    # def mycallback(model, where):
    #     if where == GRB.Callback.SIMPLEX:
    #         print(model.cbGet(GRB.Callback.SPX_OBJVAL))
    # m.optimize(mycallback)
    m.optimize(get_time_feas)    
    
# =============================================================================
#     name = "SRP-m3-run"
#     name_lp_ell = name+".lp"
#     m.write(name_lp_ell)
# =============================================================================
    
    
    def subtour(edges):
        unvisited = list(range(2*n+2)) # or V_0N1 #here we have 1 less variables than VRP formulation
        cycle = range(2*n+3)  # initial length has 1 more city
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*')
                             if j in unvisited]
            if len(cycle) > len(thiscycle):
                cycle = thiscycle
            #print(cycle)
        return cycle
    
    
    def get_edges_vars(vals):
        edge_val = []
        for t in V_0:
            for i in V_0N1:
                for j in V_0N1:
                    if i != j and vals[i,j,t] > 0.5:
                        edge_val.append((i,j))
        return edge_val
    
    
    
    
    
    def convert_t_to_i(dict0, tour0):
        dict1 = {}
        for i in range(len(tour0)): 
            dict1[tour[i]] = dict0[i]
        return dict1
        
    def rounded_dict(dict0,k):
        dict1 = {}
        for i in dict0.keys():
            dict1[i] = round(dict0[i],k)
        return dict1
    
    
    
# =============================================================================
# =============================================================================
# #     
# #     
# #     if m.status == GRB.INFEASIBLE:
# #         print('Model is infeasible')
# #         sys.exit(0)
# #         
# #     elif m.status == GRB.UNBOUNDED:
# #         print('Model is unbounded')
# #         sys.exit(0)
# #         
# #     elif m.status == GRB.OPTIMAL:
# #         print('Model is optimal')   
# #         
# #     elif m.status == GRB.TIME_LIMIT:
# #         print('Optimizaion reaches the time limit')  
# #         sys.exit(0)
# #     else:
# #         print('Optimization ended with status %d'% m.status)
# #         sys.exit(0)
# #         
# =============================================================================
# =============================================================================
    
    
# =============================================================================
#     try:
#         with open(result_file, 'w') as file:
# =============================================================================
    with open(result_file, 'a') as file:  # Use file to refer to the file object

        #try:
        if m.status == GRB.INFEASIBLE:
        # if m.status == GRB.INFEASIBLE or m.status == GRB.UNBOUNDED:
            file.write("No solution is found")  
        
        # elif m.status == GRB.TIME_LIMIT:
        #     file.write("Time limit is reached")

        try:
                    
            dict_w = m.getAttr('x', w)
            
            dict_u = m.getAttr('x', u)
             
            dict_s = m.getAttr('x', s)
              
            
            dict_z = m.getAttr('x', vars)
            
            dict_y = m.getAttr('x', y)
            vals = m.getAttr('x', vars)
            
            edge_val = get_edges_vars(vals)
            selected = gp.tuplelist((i, j) for i, j in edge_val)
            #selected = set(selected)
            tour = subtour(selected)
            file.write('\nOptimal tour: '+str(tour))
            
            #print('')
            #print('Optimal tour:', str(tour))
            dict_seats = rounded_dict(convert_t_to_i(dict_s, tour),6)
            dict_cargo = rounded_dict(convert_t_to_i(dict_u, tour),6)
            dict_pass = rounded_dict(convert_t_to_i(dict_w, tour),6)
            
            file.write('\nSeats changes: ' + str(dict_seats))
            #print('Seats changes:', str(dict_seats))  
            file.write('\nOptimal cost: ' + str(m.objVal))
            #print('Optimal cost:', m.objVal)
            file.write("\ntotal time: "+ str(round(time.time()- start_time,2)))
            #print("\ntotal time: ", round(time.time()- start_time,2))
            file.write("\nFinal MIP gap value:" + str(m.MIPGap))
            #print("\nFinal MIP gap value: %f" % m.MIPGap)
            #print("\n")
        
            file.write("\ntime to find feasible solution is "+ str(m.cbGet(GRB.Callback.RUNTIME)))
            file.write("\nChecking:\n")
            
            file.write("Remaining cargo space:"+ str(dict_cargo))
            file.write("\n")
            file.write("Remaining passenger space:"+ str(dict_pass))
            file.write("\n")
        except:
            file.write("No solution is found")

        
        # else:        
        #     dict_w = m.getAttr('x', w)
            
        #     dict_u = m.getAttr('x', u)
             
        #     dict_s = m.getAttr('x', s)
              
            
        #     dict_z = m.getAttr('x', vars)
            
        #     dict_y = m.getAttr('x', y)
        #     vals = m.getAttr('x', vars)
            
        #     edge_val = get_edges_vars(vals)
        #     selected = gp.tuplelist((i, j) for i, j in edge_val)
        #     #selected = set(selected)
        #     tour = subtour(selected)
        #     file.write('\nOptimal tour: '+str(tour))
            
        #     #print('')
        #     #print('Optimal tour:', str(tour))
        #     dict_seats = rounded_dict(convert_t_to_i(dict_s, tour),6)
        #     dict_cargo = rounded_dict(convert_t_to_i(dict_u, tour),6)
        #     dict_pass = rounded_dict(convert_t_to_i(dict_w, tour),6)
            
        #     file.write('\nSeats changes: ' + str(dict_seats))
        #     #print('Seats changes:', str(dict_seats))  
        #     file.write('\nOptimal cost: ' + str(m.objVal))
        #     #print('Optimal cost:', m.objVal)
        #     file.write("\ntotal time: "+ str(round(time.time()- start_time,2)))
        #     #print("\ntotal time: ", round(time.time()- start_time,2))
        #     file.write("\nFinal MIP gap value:" + str(m.MIPGap))
        #     #print("\nFinal MIP gap value: %f" % m.MIPGap)
        #     #print("\n")
        
        #     file.write("\ntime to find feasible solution is "+ str(m.cbGet(GRB.Callback.RUNTIME)))
        #     file.write("\nChecking:\n")
            
        #     file.write("Remaining cargo space:"+ str(dict_cargo))
        #     file.write("\n")
        #     file.write("Remaining passenger space:"+ str(dict_pass))
        #     file.write("\n")
            
        
# =============================================================================
#         
#     except:
#         with open(result_file, 'w') as file:
#             #print("No solution is found")
#             file.write("No solution is found")
# =============================================================================
        #print("+++++++++++++++++++++++++++++")
    #sys.stdout
    return time_solution



