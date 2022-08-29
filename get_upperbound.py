from asyncio import Task
import os
# from cplex import *
# from model_cp import parse_instance_cp
import random
from random import randint
import numpy as np
import re
import pandas as pd
import numpy as np
from gurobipy import *
import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB
import time
import os, sys
from sys import argv
# from model_cp import parse_instance_cp

def subtour(edges, n):
    #print("edges are", type(edges))
    unvisited = list(range(n)) # or V_0N1
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


# result_matrix = n_dist_matrix(points)
# num_rows, num_cols = result_matrix.shape
# print(result_matrix)


# n*n matrix that represents the distance


# Callback function
def get_time_feas(model, where):
    if where == GRB.Callback.MIPSOL:
        print("time to find feasible solution is", model.cbGet(GRB.Callback.RUNTIME))


def gurobi_upperbound(points, dist, seats_0, config_0_seat, S_hat, C_hat, cargo_requests, passenger_requests, L):
    m = gp.Model("TSP-upperbound")
    # n_request = len(points)//2 - 1
    # range(len(points)): [0, 1, 2, 3, 4, 5, 6, 7]
    
    V_N1 = list(range(len(points)//2))[1:] # [1,2,3]
    V_0 = list(range(len(points)//2))[:-1] # [0,1,2]
    V = list(range(len(points)//2)) # [0,1,2,3]
    Big_M = len(points)//2 - 1 # number of requests
    # print(list(dist.keys()))
    vars = m.addVars(list(dist.keys()), obj=dist, vtype=GRB.BINARY, name='x')
    t = m.addVars(Big_M+1,vtype=GRB.CONTINUOUS, name='t') #arrival time at vertex i #lb = 0
    # m.addConstr(t[0] == 0)
    s = m.addVars(Big_M+1, vtype = GRB.CONTINUOUS, name = "num_seats") #Trial: number of seats at each location
    
    for i in V:
        m.addConstr( s[i] <= S_hat, "Max_seat_capacity"+ str(i))
        m.addConstr( s[i] <= C_hat/L  + S_hat - cargo_requests[i]/L, "Maximum_seat_capacity_due_to_cargos"+ str(i))
        m.addConstr( s[i] >= passenger_requests[i], "Enough_seats_for_passenger"+ str(i))
    m.addConstr(s[0] >= config_0_seat)
    m.addConstr(s[0] <= config_0_seat + seats_0[0])

    for i in V_N1:
        for j in V_N1:
            m.addConstr( s[j] <= s[i] + vars[(i,j)]*(seats_0[i+Big_M]+seats_0[j])+S_hat*(1-vars[(i,j)]), "Adding_max_seats"+ str(i))
    
    for j in V_N1:
         m.addConstr( s[j] <= s[0] + vars[(0,j)]*seats_0[j] + S_hat*(1-vars[(0,j)]), "Adding_max_seats_origin"+ str(j))
    
    for i in V:
        m.addConstr(sum(vars[(i,j)] for j in V if j!=i) ==1,"leaving"+str(i))

    for j in V:
        m.addConstr(sum(vars[(j,i)] for i in V if j!=i) == sum(vars[(i,j)] for i in V if j!=i), "balanced"+str(j))

    for i in V_N1:
        for j in V_N1:
            if i!=j:
                m.addConstr(t[i]+ vars[(i,j)] - Big_M*(1-vars[(i,j)]) <= t[j], "subtour_elimination"+ str(i)+","+str(j))
    

    for i in V_N1:
        m.addConstr( t[i] >= 1, "subtour_elimination_domain"+ str(i))
    
    
    for i in V_N1:
        m.addConstr( t[i] <= Big_M, "subtour_elimination_domain"+ str(i))


    m.setObjective(sum(vars[(i,j)]*dist[(i,j)] for i in V for j in V if i !=j),GRB.MINIMIZE)
    
    #sys.stdout = open(result_file, "w")print(
    
    m.Params.LogToConsole = 0
    # m.setParam('TimeLimit', time_lim)
    m.Params.Threads = 4
    m.Params.OptimalityTol = 1e-6
    m.params.FeasibilityTol = 1e-6
    # m.Params.LogFile = result_file
    # print("result file is: \n", result_file)

    #m.setParam('TimeLimit', time_lim)
    #m.Params.LogFile = result_file
    #m.params.FeasibilityTol = 1e-6
    m.optimize(get_time_feas)
    vals = m.getAttr('x', vars)
    selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
    tour = subtour(selected, Big_M+1)
    print('\nOptimal tour: '+ str(tour))
    
    obj_val = m.objVal
    for i in range(len(tour)):
        obj_val = obj_val + dist[(tour[i], tour[i])]
    return obj_val, tour
    


# gurobi_upperbound(points, dist)
