# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 11:43:29 2021

@authors: Arnoosh 
to run in anaconda: (file_name at the end of path)
python C:\Python\SRP\m2-run.py 5_426.txt > C:\Python\SRP\output_m2\5_426.txt

python C:\Python\SRP\m2-run-new.py 4_996.txt > C:\Python\SRP\output_m2\4_996.txt

python C:\Python\SRP\m2-run.py 5_426.txt

run with run_file.py

"""
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
import math
from util import parse_instance_cp



import logging    # first of all import the module




def solve_m2_total_cap(inst_dir, sol_dir_model, inst_name, time_lim):

    #new_inst_dir = "C:/Python/SRP/test_rand_inst"
    # new_inst_dir = "/Users/user/SRPproject/Cplex_copy/new_instance"
    new_inst_dir = inst_dir
    name_of_file =  inst_name#argv[1]#"5_426.txt" #"5_34_c109.txt" #"5-101-"+str(r) argv[1]#
    
    file_inst = os.path.join(new_inst_dir, name_of_file)   
    
    instanceName = file_inst
    path = sol_dir_model
    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")
    
    
    result_file = os.path.join(sol_dir_model, name_of_file) 

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

    
#     with open(instanceName,"r") as instance:
#         line = instance.readline()
#         nb_seed, n, S_hat, L, C_hat = (int(x) for x in line.split())
#         line = instance.readline()
#         config_0_seat, config_0_cargo = (int(x) for x in line.split())
#         line = instance.readline()
#         seats_0 = line.split()
#         seats_0 = [int(k) for k in seats_0]
#         dist_V = {}
#         dist_v_0 = {}
#         dist_v_N1 ={}
#         q_hat = {}
#         pi_hat = {}
#         line = instance.readline()
#         i = int(line.split()[0])
#         x = int(line.split()[1])
#         y = int(line.split()[2])
#         q_hat0 = int(line.split()[3]) 
#         pi_hat0 = int(line.split()[4])
#         point0 = (x,y)
#         dist_v_0[i] = point0 #depot node
#         dist_v_N1[2*n+1] = point0
#         q_hat[i] = q_hat0
#         pi_hat[i] = pi_hat0
#         for j in range(1,2*n+1):
#             line = instance.readline()
#             i = int(line.split()[0])
#             x = int(line.split()[1])
#             y = int(line.split()[2])
#             q_hat0 = int(line.split()[3]) 
#             pi_hat0 = int(line.split()[4])
#             point0 = (x,y)
#             dist_V[i] = point0
#             q_hat[i] = q_hat0
#             pi_hat[i] = pi_hat0

# #adding the last item of the list, it's not in the text file. Since the first
# #and last vertex are copies of depot, their demands must be the same
#     q_hat[2*n+1] = q_hat[0]
#     pi_hat[2*n+1] = pi_hat[0]
    
#     #seats_0 = 0
#     S_0 = seats_0# [0,4,0,0,0,0,4,0,0,0,0]
    
    def merge_two_dicts(x, y):
        """Given two dictionaries, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z
    
    def get_dist(p1, p2):
        dist2 = (p1[0]-p2[0])**2 +(p1[1]-p2[1])**2 
        dist = math.ceil(np.sqrt(dist2))
        return dist
    
    
    def get_time_feas(model, where):
        if where == GRB.Callback.MIPSOL:
            print("time to find feasible solution is", model.cbGet(GRB.Callback.RUNTIME))


    
    def rounded_dict(dict0,k):
        dict1 = {}
        for i in dict0.keys():
            dict1[i] = round(dict0[i],k)
        return dict1

    
    
    #------------------------------
        
    
    
    # Callback - use lazy constraints (and user cuts) to eliminate sub-tours
    def subtourelim(model, where):
    
               
        if (where == GRB.Callback.MIPNODE) & USERCUTS:  
            vals = model.cbGetNodeRel(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                    if vals[i, j] > 0.0001)
            # find the shortest cycle in the selected edge list
            tour = subtour(selected)
            tour.append(tour[0])
            if len(tour) < n:
                # add subtour elimination constr. for every pair of cities in tour
                model.cbCut(gp.quicksum(model._vars[tour[i], tour[i+1]]
                                        for i in range(len(tour)-1)) <= len(tour)-2)
    def subtour(edges):
        unvisited = list(range(n))
        cycle = range(n+1)  # initial length has 1 more city
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
    
    
    
    
    
    #------------------------------
    #print("seats_0", seats_0)
    
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
    
    arcs = list(arc_dist.keys())
       
            
      
    Big_M = len(V)
    Big_M_cargo = C_hat+2*S_hat*L
    Big_M_passenger = 2*S_hat
    
                   
    #time_lim = 1000
    #S_0 = 0 #for now there are no seats at bases, and these are added as upperbound, when variable I think they be added as constraints    
    #print("start_time", start_time)
    
    
    
    start_time = time.time()
    
    
    
    m = Model("Location-based model-total capacity")
    vars = m.addVars(arcs,vtype=GRB.BINARY, name='vars')
    t = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, name='t') #arrival time at vertex i #lb = 0
    
    sigma = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0,ub= S_hat, name='sigma') #number of seats when leaving i
    c = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L, name='c') #cargo space when leaving i
    
    
    #s = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = -9, ub = S_0, name='s') #number of seats picked up or stored at base i (positive or negative)
    pi = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub= S_hat, name='pi') #number of passengers in the aircraft when leaving location i
    q = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L, name='q') #kg of cargo in the aircraft when leaving location i
    
    
    #initial values of t, u and y (since definition of u in VRP and SRP are different the initial values will be different)
    m.addConstr(t[0] == 0)
    m.addConstr(c[0] == config_0_cargo)
    m.addConstr(sigma[0] == config_0_seat)
    
    
    for i in V_0:
        m.addConstr(sum(vars[(i,j)] for j in V_N1 if j!=i) ==1,"leaving"+str(i))
       
        
    for j in V:
        m.addConstr(sum(vars[(j,i)] for i in V_N1 if j!=i) == sum(vars[(i,j)] for i in V_0 if j!=i), "balanced"+str(j))
        
    for i in V_0:
        for j in V_N1:
            if i!=j:
                m.addConstr(t[i]+ vars[(i,j)] - Big_M*(1-vars[(i,j)]) <= t[j], "subtour_elimination"+ str(i)+","+str(j))
         
            
    for i in P:
        m.addConstr(t[i]+ 1 <= t[i+n], "precedence"+ str(i))
        
    
    for i in V:
        m.addConstr( t[i] >= 1, "subtour_elimination_domain"+ str(i))
    
    
    for i in V:
        m.addConstr( t[i] <= 2*n, "subtour_elimination_domain"+ str(i))
          
        
        
    for i in V_N1:
        m.addConstr( c[i]+L*sigma[i] == C_hat+S_hat*L, "total_cap"+ str(i))   #changed <= to == 
        
        
        
        
    for i in V_0:
        for j in V: #instead of V_N1, S_0 is not defined on V_N1
            if i != j:
                m.addConstr(sigma[j] <= sigma[i]+S_0[j]*vars[(i,j)] + Big_M_passenger*(1-vars[(i,j)]), "passenger_delivery"+str(i)+","+str(j))
    
    
    for i in V_N1:
        m.addConstr( pi[i] <= sigma[i], "picked_up_passengers_limit"+ str(i))    
        
    for i in V_N1:
        m.addConstr( q[i] <= c[i], "picked_up_cargo_limit"+ str(i))        
    
    
    
    #pi constraints
    # =============================================================================
    # big_pi_hat = 0
    # for i in range(n+1):
    #     big_pi_hat = pi_hat[i] + big_pi_hat
    # =============================================================================
      
    pi[0] == 0
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(pi[j] >= pi[i] + pi_hat[j]*vars[(i,j)]-(1-vars[(i,j)])*S_hat, "current_pass"+str(i)+","+str(j)) 
    
    
    
    
    #c constraints
    # =============================================================================
    # big_c = 0
    # for i in range(n+1):
    #     big_c = q_hat[i] + big_c
    # =============================================================================
    big_k = C_hat+S_hat*L  
    q[0] == 0
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(q[j] >= q[i] + q_hat[j]*vars[(i,j)]-(1-vars[(i,j)])*big_k, "current_cargo"+str(i)+","+str(j)) 
    
    
    m.setObjective(sum(vars[(i,j)]*arc_dist[(i,j)] for i in V_0 for j in V_N1 if i !=j),GRB.MINIMIZE)
    
    #sys.stdout = open(result_file, "w")
    
    m.setParam('TimeLimit', time_lim)
    m.Params.LogToConsole = 0
    m.Params.OptimalityTol = 1e-6
    m.params.FeasibilityTol = 1e-6
    m.Params.LogFile = result_file
    m.optimize(get_time_feas)
    
    name = "PD-1SRP"
    name_lp_ell = name+".lp"
    m.write(name_lp_ell)
    
    def subtour(edges):
        print("edges are", type(edges))
        unvisited = list(range(2*n+2)) # or V_0N1
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
    
    #----------------------------
    
    def rounded_dict(dict0,k):
        dict1 = {}
        for i in dict0.keys():
            dict1[i] = round(dict0[i],k)
        return dict1
    
    with open(result_file, 'a') as file:  # Use file to refer to the file object
        #try:
        if m.status == GRB.INFEASIBLE:
            file.write("No solution is found")  

        
        else:
    
            dict_sigma = m.getAttr('x', sigma)
            dict_c = m.getAttr('x', c)
         
            dict_pi = m.getAttr('x', pi)
            dict_q = m.getAttr('x', q)
          
            dict_seats = rounded_dict(dict_sigma,6)
            dict_room_cargo = rounded_dict(dict_c,6)
            dict_cargo = rounded_dict(dict_q,6)
            dict_pass = rounded_dict(dict_pi,6)
        
        
            #dict_z = m.getAttr('x', vars) 
            
            vals = m.getAttr('x', vars)
            
            selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
            
            tour = subtour(selected)
            file.write('\nseats:\n')
            
            dict_seat_changes = {}
            dict_seat_changes[0] = dict_seats[tour[0]] - config_0_seat
            for i in V: #We don't care about number of seats when leaving end-depot
                seat_changes= dict_seats[tour[i]] - dict_seats[tour[i-1]]
                dict_seat_changes[tour[i]] = seat_changes
                #file.write(("seat changes at location" + str(i) + " is " + str(seat_changes)))
            file.write(("\nSeats changes: " + str(dict_seat_changes)))
            file.write(("\nSigma: "+ str(dict_seats)))
            
            file.write('\nOptimal tour: '+ str(tour))
            file.write('\nOptimal cost: '+ str(m.objVal))

            #print('Seats changes: %s' %str(dict_s))
            file.write('\nedges:\n')
            for a in arcs:
                if vars[a].x>=0.99:
                        file.write(str(a) + ": " +str(vars[a].x) + ", ")
            
# =============================================================================
#             file.write('\nseats:\n')            
#         
#             
#             dict_seat_changes = {}
#             for i in V_0:
#                 seat_changes= dict_sigma[tour[i+1]] - dict_sigma[tour[i]]
#                 dict_seat_changes[i] = seat_changes
#                 #file.write(("seat changes at location" + str(i) + " is " + str(seat_changes)))
#             file.write(("Seats changes: " + str(dict_seat_changes)))
#         
# =============================================================================
            file.write('\narrival time:\n')            
            for i in V_0:
                if t[i].x>= 0.99:
                    file.write("\narrival time of vertex: "+str(i)+ str(round(t[i].x,6)))
                                
            file.write("\ntotal time: "+ str(round(time.time()- start_time,2)))
            file.write("\nFinal MIP gap value: "+ str(m.MIPGap))
            file.write("\ntime to find feasible solution is "+ str(m.cbGet(GRB.Callback.RUNTIME)))
            file.write("\nChecking:\n")
            
            file.write("current passenger:"+ str(dict_pass))
            file.write("\n")
            file.write("current cargo:"+ str(dict_cargo))
            file.write("\n")    
            file.write("room for cargo:"+ str(dict_room_cargo))
            file.write("\n")  
            file.write("room for passengers:"+str(dict_seats))
            file.write("\n")
            
    
    
# =============================================================================
#     try:
#         
#         dict_sigma = m.getAttr('x', sigma)
#         dict_c = m.getAttr('x', c)
#      
#         dict_pi = m.getAttr('x', pi)
#         dict_q = m.getAttr('x', q)
#       
#         dict_seats = rounded_dict(dict_sigma,6)
#         dict_room_cargo = rounded_dict(dict_c,6)
#         dict_cargo = rounded_dict(dict_q,6)
#         dict_pass = rounded_dict(dict_pi,6)
#     
#     
#         #dict_z = m.getAttr('x', vars) 
#         
#         vals = m.getAttr('x', vars)
#         
#         selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
#         
#         tour = subtour(selected)
#         
#         for i in V_0:
#             seat_changes= dict_sigma[tour[i+1]] - dict_sigma[tour[i]]
#             print("seat changes at location {} is {}".format(i,seat_changes))
#         
#         print('')
#         print('Optimal tour: %s' % str(tour))
#         print('Optimal cost: %g' % m.objVal)
#         print('')
#         #print('Seats changes: %s' %str(dict_s))
#         print('\nedges:\n')
#         for a in arcs:
#             if vars[a].x>=0.99:
#                     print("answer:",a,vars[a].x)
#         
#         print('\nseats:\n')            
#     
#         
#         for i in V_0:
#             seat_changes= dict_seats[tour[i+1]] - dict_seats[tour[i]]
#             print("seat changes at location {} is {}".format(i,seat_changes))
#     
#         print('\narrival time:\n')            
#         for i in V_0:
#             if t[i].x>= 0.99:
#                 print("arrival time of vertex:",i,round(t[i].x,6))
#                             
#         print("\ntotal time: ", round(time.time()- start_time,2))
#         print("\nFinal MIP gap value: %f" % m.MIPGap)
#         
#         print("\nChecking:\n")
#         
#         print("current passenger:", dict_pass)
#         print("\n")
#         print("current cargo:", dict_cargo)
#         print("\n")    
#         print("room for cargo:", dict_room_cargo)
#         print("\n")  
#         print("room for passengers:", dict_seats)
#         print("\n")
#         
#     
#         
#     except:
#         print("No solution is found")
#     print("+++++++++++++++++++++++++++++")
#     #sys.stdout
# =============================================================================


# =============================================================================
# =============================================================================
# =============================================================================
# # #                 
# # #     time_lim = 10
# # #     #S_0 = 0 #for now there are no seats at bases, and these are added as upperbound, when variable I think they be added as constraints
# # #     
# # #     start_time = time.time()
# # #     
# # #     print("start_time", start_time)
# # #     
# # #     
# # #     
# # #     start_time = time.time()
# # #     
# # #     
# # #     m = Model("Location-based model-total capacity")
# # #     vars = m.addVars(arcs,vtype=GRB.BINARY, name='vars')
# # #     t = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, name='t') #arrival time at vertex i #lb = 0
# # #     
# # #     sigma = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0,ub= S_hat+1, name='sigma') #number of seats when leaving i
# # #     c = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L+1, name='c') #cargo space when leaving i
# # #     
# # #     
# # #     #s = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = -9, ub = S_0, name='s') #number of seats picked up or stored at base i (positive or negative)
# # #     pi = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub= S_hat+1, name='pi') #number of passengers in the aircraft when leaving location i
# # #     q = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L+1, name='q') #kg of cargo in the aircraft when leaving location i
# # #     
# # #     
# # #     #initial values of t, u and y (since definition of u in VRP and SRP are different the initial values will be different)
# # #     m.addConstr(t[0] == 0)
# # #     m.addConstr(c[0] == config_0_cargo)
# # #     m.addConstr(sigma[0] == config_0_seat)
# # #     
# # #     
# # #     for i in V_0:
# # #         m.addConstr(sum(vars[(i,j)] for j in V_N1 if j!=i) ==1,"leaving"+str(i))
# # #        
# # #         
# # #     for j in V:
# # #         m.addConstr(sum(vars[(j,i)] for i in V_N1 if j!=i) == sum(vars[(i,j)] for i in V_0 if j!=i), "balanced"+str(j))
# # #         
# # #     for i in V_0:
# # #         for j in V_N1:
# # #             if i!=j:
# # #                 m.addConstr(t[i]+ vars[(i,j)] - Big_M*(1-vars[(i,j)]) <= t[j], "subtour_elimination"+ str(i)+","+str(j))
# # #          
# # #             
# # #     for i in P:
# # #         m.addConstr(t[i]+ 1 <= t[i+n], "precedence"+ str(i))
# # #         
# # #     
# # #     for i in V:
# # #         m.addConstr( t[i] >= 1, "subtour_elimination_domain"+ str(i))
# # #     
# # #     
# # #     for i in V:
# # #         m.addConstr( t[i] <= 2*n, "subtour_elimination_domain"+ str(i))
# # #           
# # #         
# # #         
# # #     for i in V_N1:
# # #         m.addConstr( c[i]+L*sigma[i] <= C_hat+S_hat*L, "total_cap"+ str(i))    
# # #         
# # #         
# # #         
# # #         
# # #     for i in V_0:
# # #         for j in V: #instead of V_N1, S_0 is not defined on V_N1
# # #             if i != j:
# # #                 m.addConstr(sigma[j] <= sigma[i]+S_0[j] + Big_M_passenger*(1-vars[(i,j)]), "passenger_delivery"+str(i)+","+str(j))
# # #     
# # #     
# # #     for i in V_N1:
# # #         m.addConstr( pi[i] <= sigma[i], "picked_up_passengers_limit"+ str(i))    
# # #         
# # #     for i in V_N1:
# # #         m.addConstr( q[i] <= c[i], "picked_up_cargo_limit"+ str(i))        
# # #     
# # #     
# # #     
# # #     #pi constraints
# # #     # =============================================================================
# # #     # big_pi_hat = 0
# # #     # for i in range(n+1):
# # #     #     big_pi_hat = pi_hat[i] + big_pi_hat
# # #     # =============================================================================
# # #       
# # #     pi[0] == 0
# # #     for i in V_0:
# # #         for j in V_N1:
# # #             if i != j:
# # #                 m.addConstr(pi[j] >= pi[i] + pi_hat[j]*vars[(i,j)]-(1-vars[(i,j)])*S_hat, "current_pass"+str(i)+","+str(j)) 
# # #     
# # #     
# # #     
# # #     
# # #     #c constraints
# # #     # =============================================================================
# # #     # big_c = 0
# # #     # for i in range(n+1):
# # #     #     big_c = q_hat[i] + big_c
# # #     # =============================================================================
# # #     big_k = C_hat+S_hat*L  
# # #     q[0] == 0
# # #     for i in V_0:
# # #         for j in V_N1:
# # #             if i != j:
# # #                 m.addConstr(q[j] >= q[i] + q_hat[j]*vars[(i,j)]-(1-vars[(i,j)])*big_k, "current_cargo"+str(i)+","+str(j)) 
# # #     
# # #     
# # #     m.setObjective(sum(vars[(i,j)]*arc_dist[(i,j)] for i in V_0 for j in V_N1 if i !=j),GRB.MINIMIZE)
# # #     
# # #     
# # #     sys.stdout = open(result_file, "w")
# # #     m.setParam('TimeLimit', time_lim)
# # #     m.Params.Threads = 4
# # #     m.Params.OptimalityTol = 1e-6
# # #     m.params.FeasibilityTol = 1e-6
# # #     #m.Params.LogToConsole = 0
# # #     m.Params.LogFile = result_file
# # #     m.optimize()
# # #     
# # #     #name = "PD-1SRP"
# # #     #name_lp_ell = name+".lp"
# # #     #m.write(name_lp_ell)
# # #  
# # #     dict_sigma = m.getAttr('x', sigma)
# # #     dict_c = m.getAttr('x', c)
# # #  
# # #     dict_pi = m.getAttr('x', pi)
# # #     dict_q = m.getAttr('x', q)
# # #   
# # #     dict_seats = rounded_dict(dict_sigma,6)
# # #     dict_room_cargo = rounded_dict(dict_c,6)
# # #     dict_cargo = rounded_dict(dict_q,6)
# # #     dict_pass = rounded_dict(dict_pi,6)
# # # 
# # # 
# # #     #dict_z = m.getAttr('x', vars) 
# # #     
# # #     vals = m.getAttr('x', vars)
# # #     
# # #     selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
# # #     
# # #     tour = subtour(selected)
# # #     
# # #     for i in V_0:
# # #         seat_changes= dict_seats[tour[i+1]] - dict_seats[tour[i]]
# # #         print("seat changes at location {} is {}".format(i,seat_changes))
# # #     
# # #     
# # #     print('')
# # #     print('Optimal tour: %s' % str(tour))
# # #     print('Optimal cost: %g' % m.objVal)
# # #     print('')
# # #     #print('Seats changes: %s' %str(dict_s))
# # #     print('\nedges:\n')
# # #     for a in arcs:
# # #         if vars[a].x>=0.99:
# # #                 print("answer:",a,vars[a].x)
# # #     
# # #     print('\nseats:\n')            
# # # 
# # #     
# # #     for i in V_0:
# # #         seat_changes= dict_seats[tour[i+1]] - dict_seats[tour[i]]
# # #         print("seat changes at location {} is {}".format(i,seat_changes))
# # # 
# # #     print('\narrival time:\n')            
# # #     for i in V_0:
# # #         if t[i].x>= 0.99:
# # #             print("arrival time of vertex:",i,round(t[i].x,6))
# # #                         
# # #     print("\ntotal time: ", round(time.time()- start_time,2))
# # #     print("\nFinal MIP gap value: %f" % m.MIPGap)
# # #     
# # #     print("\nChecking:\n")
# # #     
# # #     print("current passenger:", dict_pass)
# # #     print("\n")
# # #     print("current cargo:", dict_cargo)
# # #     print("\n")    
# # #     print("room for cargo:", dict_room_cargo)
# # #     print("\n")  
# # #     print("room for passengers:", dict_seats)
# # #     print("\n")
# # # 
# # # 
# # #     
# # #     
# # #     
# # #     print("+++++++++++++++++++++++++++++")
# # #     try:
# # #     
# # #         dict_sigma = m.getAttr('x', sigma)
# # #         dict_c = m.getAttr('x', c)
# # #      
# # #         dict_pi = m.getAttr('x', pi)
# # #         dict_q = m.getAttr('x', q)
# # #       
# # #         dict_seats = rounded_dict(dict_sigma,6)
# # #         dict_room_cargo = rounded_dict(dict_c,6)
# # #         dict_cargo = rounded_dict(dict_q,6)
# # #         dict_pass = rounded_dict(dict_pi,6)
# # #     
# # #     
# # #         #dict_z = m.getAttr('x', vars) 
# # #         
# # #         vals = m.getAttr('x', vars)
# # #         
# # #         selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
# # #         
# # #         tour = subtour(selected)
# # #         
# # #         for i in V_0:
# # #             seat_changes= dict_sigma[tour[i+1]] - dict_sigma[tour[i]]
# # #             print("seat changes at location {} is {}".format(i,seat_changes))
# # #         
# # #         print('')
# # #         print('Optimal tour: %s' % str(tour))
# # #         print('Optimal cost: %g' % m.objVal)
# # #         print('')
# # #         #print('Seats changes: %s' %str(dict_s))
# # #         print('\nedges:\n')
# # #         for a in arcs:
# # #             if vars[a].x>=0.99:
# # #                     print("answer:",a,vars[a].x)
# # #         
# # #         print('\nseats:\n')            
# # #     
# # #         
# # #         for i in V_0:
# # #             seat_changes= dict_seats[tour[i+1]] - dict_seats[tour[i]]
# # #             print("seat changes at location {} is {}".format(i,seat_changes))
# # #     
# # #         print('\narrival time:\n')            
# # #         for i in V_0:
# # #             if t[i].x>= 0.99:
# # #                 print("arrival time of vertex:",i,round(t[i].x,6))
# # #                             
# # #         print("\ntotal time: ", round(time.time()- start_time,2))
# # #         print("\nFinal MIP gap value: %f" % m.MIPGap)
# # #         
# # #         print("\nChecking:\n")
# # #         
# # #         print("current passenger:", dict_pass)
# # #         print("\n")
# # #         print("current cargo:", dict_cargo)
# # #         print("\n")    
# # #         print("room for cargo:", dict_room_cargo)
# # #         print("\n")  
# # #         print("room for passengers:", dict_seats)
# # #         print("\n")
# # #         
# # # 
# # #     
# # #     except:
# # #         print("No solution is found")
# # #     print("+++++++++++++++++++++++++++++")    
# # #     sys.stdout
# # # 
# # # 
# =============================================================================
# =============================================================================
# 
# =============================================================================






