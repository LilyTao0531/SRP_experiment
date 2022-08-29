#!/usr/bin/env python
# coding: utf-8

import numpy as np
import json
import os
from Compare import plotRE
import math

"""
    Module with many methods to manipulate XP results, saving and reading XP files and add new results into existing XP files
"""

def saveXP(res, path):
    """
        Create JSON file from XP stored in res and save it at given path
    """
    out_file = open(path, "w")
    json.dump(res, out_file, indent = 4)
    out_file.close()


def readXP(file):
    """
        Create dictionary from XP file
    """
    with open(file) as json_file:
        return json.load(json_file)


def addXP_newInstances(oldXP, newXP):
    """
        Add new XPs run on new instances for the same methods and same time steps/ iterations.
    """
    
    assert len([id for id in oldXP["instances_id"] if id in newXP["instances_id"]]) == 0, "new XP should only include new instances"
    assert oldXP["methods"].keys() == newXP["methods"].keys(), "Methods in new XP should be the same as in old XP"
    assert oldXP["x_axis"] == newXP["x_axis"], "New XP should be run on the same time steps or iterations"
    
    # agg aggregates oldXP ad newXP
    agg = oldXP.copy()
    agg["instances_id"].extend(newXP["instances_id"])
    agg["BKS"].extend(newXP["BKS"])
    for key in agg["methods"].keys():
        agg["methods"][key].extend(newXP["methods"][key])
    
    return agg


def addXP_newSteps(oldXP, newXP):
    """
        Add new XPs run on new time steps / iterations for the same methods and same instances.
        The method supposes steps list in both XP are sorted in ascending order.
        
    """
    
    assert oldXP["instances_id"] == newXP["instances_id"], "New XP should be run on the same instances as oldXP"
    assert oldXP["methods"].keys() == newXP["methods"].keys(), "Methods in new XP should be the same as in old XP"
    assert oldXP["x_axis"]["type"] == newXP["x_axis"]["type"]
    assert len([s for s in oldXP["x_axis"]["steps"] if s in newXP["x_axis"]["steps"]]) == 0, "New XP should only include new time steps / iterations"
    
    # We create new aggregate steps list and save the indices where old steps list is modified
    # Example [1,2,10,20] and [5,60] --> [1,2,5,10,20,60]
    # and modifIndices --> [2, 5]
    aggSteps = oldXP["x_axis"]["steps"].copy()
    modifIndices = []
    curNew = 0
    curAgg = 0
    while curNew < len(newXP["x_axis"]["steps"]):
        if curAgg >= len(aggSteps) or newXP["x_axis"]["steps"][curNew] <= aggSteps[curAgg]:
            aggSteps.insert(curAgg, newXP["x_axis"]["steps"][curNew])
            modifIndices.append(curAgg)
            curNew += 1
            curAgg += 1
        else:
            curAgg+=1
    
    
    # agg aggregates oldXP ad newXP
    agg = oldXP.copy()
    agg["x_axis"]["steps"] = aggSteps
    for key in agg["methods"].keys():
        for i in range(len(agg["instances_id"])):
            for k, idx in enumerate(modifIndices):
                agg["methods"][key][i].insert(idx, newXP["methods"][key][i][k])
                
    # Update BKS if new best solution is found in new XP
    agg["BKS"] = [min(agg["BKS"][i], newXP["BKS"][i]) for i in range(len(agg["instances_id"]))]
    
    return agg


def addXP_newMethods(oldXP, newXP):
    """
        Add new XPs run on new methods (or updating XP for existing methods) for the same instances and time steps/ iterations.
        
    """
    assert oldXP["instances_id"] == newXP["instances_id"], "New XP should be run on the same instances as oldXP"
    assert oldXP["x_axis"] == newXP["x_axis"],  "New XP should be run on the same time steps or iterations"
    
    # agg aggregates oldXP ad newXP
    agg = oldXP.copy()
    for key in newXP["methods"].keys():
        agg["methods"][key] = newXP["methods"][key]
    
    # Update BKS if new best solution is found in new XP
    agg["BKS"] = [min(agg["BKS"][i], newXP["BKS"][i]) for i in range(len(agg["instances_id"]))]
    
    return agg

def generage_list_x(time_lim, time_increment): # The x-axis divided by certain time_increment
    list_raw = np.arange(time_increment, time_lim, time_increment)
    list_final = np.round(list_raw, decimals=5)
    return list_final.tolist()

def assign_values(time_solution_tuple, model_name, result_dict, list_x): # Determine the y-value for every x-value, according to the experiment results
    index_of_x = 0
    value_of_y = []
    for i in range(len(time_solution_tuple)): # Go through every time-point when solution changes and the objective value
        # if index_of_x is not out of range and index_of_x is earlier than the change in solution, assign the objective value one before.
        while index_of_x <= len(list_x) - 1 and time_solution_tuple[i][0] > list_x[index_of_x]:
            if i == 0: # If no previous solution, then assign a place holder "TO"
                value_of_y.append("TO")
            else:
                value_of_y.append(time_solution_tuple[i-1][1])
            index_of_x = index_of_x + 1

        if model_name[0] == "m" and i ==  (len(time_solution_tuple) - 1):
            while index_of_x <= (len(list_x) - 1):
                value_of_y.append(time_solution_tuple[-1][1])
                index_of_x = index_of_x + 1
    while index_of_x <= len(list_x) - 1:
        value_of_y.append(time_solution_tuple[-1][1])
        index_of_x = index_of_x + 1

    result_dict["methods"][model_name].append(value_of_y)

def assign_values_timeout(model_name, result_dict, list_x): # Assign "TO" to all y-values of instances without a concrete solution
    index_of_x = 0
    value_of_y = []
    while index_of_x <= len(list_x) - 1:
        value_of_y.append("TO")
        index_of_x = index_of_x + 1
    result_dict["methods"][model_name].append(value_of_y)

# example = readXP("result_json_file.json")
# plotRE(example, "Relative Error", "graphs")

def parse_instance_cp(inst_dir, filename):
    file_inst = os.path.join(inst_dir, filename) 
    with open(file_inst,"r") as instance:
        line = instance.readline()
        nb_seed, n, S_hat, L, C_hat = (int(x) for x in line.split())
        line = instance.readline()
        config_0_seat, config_0_cargo = (int(x) for x in line.split())
        line = instance.readline()
        seats_0 = line.split()
        seats_0 = [int(k) for k in seats_0]
        dist_V = []
        dist_v_0 = []
        dist_v_N1 =[]
        q_hat = []
        p_hat = []
    
        for j in range(0,2*n+1):

            line = instance.readline()
            i = int(line.split()[0])
            x = int(line.split()[1])
            y = int(line.split()[2])
            q_hat0 = int(line.split()[3]) 
            p_hat0 = int(line.split()[4])
            point0 = (x,y)
            if j == 0:
                dist_v_0.append(point0) 
                dist_v_N1.append(point0)
            else:
                dist_V.append(point0)
            q_hat.append(q_hat0) 
            p_hat.append(p_hat0)
    
    # q_hat[2*n+1] = q_hat[0]
    # pi_hat[2*n+1] = pi_hat[0]
    
    #print("q_hat is", q_hat)
    
    #print("pi_hat is", pi_hat)
    # dist_V_0 = merge_two_dicts(dist_V,dist_v_0) #set(V).union(v_0)
    dist_V_0 = dist_v_0 + dist_V
    dist_V_N1 = dist_V + dist_v_N1 #set(V).union(v_N1) #V_{N+1}
    dist_V_0N1 = dist_v_0 + dist_V + dist_v_N1
    
    
    
   
    
    P = list(range(1,n+1))#dict(list(V.items())[:n]) #pickup vertices
    D = list(range(n+1,2*n+1)) #dict(list(V.items())[n:]) #delivery vertices
    return dist_V, dist_V_N1, dist_V_0N1, q_hat, p_hat, n, S_hat, L, C_hat, config_0_seat, config_0_cargo, seats_0

