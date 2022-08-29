from asyncio import Task
# import os
# from cplex import *
from docplex.cp.model import *
from docplex.cp.solver.cpo_callback import CpoCallback
# from capacity_checker import pick_most_seats
from get_upperbound import gurobi_upperbound
# from get_upperbound import n_dist_matrix, gurobi_upperbound
import random
from random import randint
import numpy as np
import re


import math


n = 2 #This is the number of requests
L = 100 #This is the weight of cargo/seat per unit
cargo_max = 200 # The amount of cargo that can be carried when the maximum passenger capacity has been met.
seat_max = 6 # This is the maximum number of seats in the aircraft
# points = [(0, 0), (-1, 0), (2, 0), (2, 1), (1, 0), (0, 0)]
points_Arnoosh = [(0, 0), (1, 1/2), (1, -1/2), (2, 1/2), (2, -1/2), (0, 0)]
# This is the coordinates of the locations that we need to visit
# The first and last points represent the depot, 
# and the first half of the points are the pickup locations
# while the second half are the delivery locations.

s = [0, 2, 0, 0, 0] #Seats available at each spot
q = [0, 400, 100, -400, -100] # Cargo
p = [0, 2, 6, -2, -6] # Passenger




def build_and_solve(time_limit, points, q, p, n, seat_max, L, config_0_seat, config_0_cargo, seats_0, S_hat, C_hat):


    """

    """

    # Get the input matrix for the upperbound MIP solver
    dist = n_dist_matrix(points) 
    # Get the solution for the upperbound using MIP solver
    obj_val, tour = gurobi_upperbound(points, dist, seats_0, config_0_seat, S_hat, C_hat, q, p, L)
    # Get the distance between each two points
    transition_dist = [[math.ceil(math.hypot(points[a][0] - points[b][0], points[a][1] - points[b][1])) for a in range(2*n + 1)]for b in range(2*n + 1)]
    transition_dist_for_cp = transition_matrix(transition_dist)

    # Create the cp model  
    mdl = CpoModel()

    # Create the empty dictionary that will hold all the interval variables
    itvs = {}

    for i in range(2*n+2): #Include 2 Depots, Pickup nodes, and Delivery nodes
        itvs[i] = mdl.interval_var(size=0, name = 'v' + str(i))
    
    # Create the empty list that will hold all the integer variables of seat changes
    change_of_seats = []
    # seats_0.append(0)
    for i in range(0, 2*n+1):
        change_of_seats.append(mdl.integer_var(-seat_max, seats_0[i])) # Change in number of seats in each pickup/delivery location
    change_of_seats.append(mdl.integer_var(0, 0))

    C = step_at(0, config_0_cargo) # available cargo space
    P = step_at(0, config_0_seat) # number of empty seats
    S = step_at(0, config_0_seat) # number of seats (empty+occupied)
    total_capacity_K = config_0_cargo + config_0_seat * L



    p.append(0)
    q.append(0)
    for i in range(0, len(itvs)): #This is to iterate through all the pickup&delivery locations

        C -= mdl.step_at_start(itvs[i], (0, total_capacity_K))
        C += mdl.step_at_start(itvs[i], (0, total_capacity_K))
        P -= mdl.step_at_start(itvs[i], (0, seat_max))
        P += mdl.step_at_start(itvs[i], (0, seat_max))
        mdl.add(mdl.height_at_start(itvs[i], C) == -q[i]-change_of_seats[i]*L) # This is the change to the available cargo space
        mdl.add(mdl.height_at_start(itvs[i], P) == -(p[i]-change_of_seats[i])) # This is the change to the empty seats

        S += mdl.step_at_start(itvs[i], (0, seat_max))
        S -= mdl.step_at_start(itvs[i], (0, seat_max))
        mdl.add(mdl.height_at_start(itvs[i], S) == change_of_seats[i]) # This is the change to the total number of seats in the aircraft


    mdl.add( C>=0 )
    mdl.add( P>=0 )
    mdl.add( S<=seat_max)

    # The types represent each different location
    type_l = [i for i in range(2*n+1)]
    type_l.extend([0])

    # This is the order of visits to all nodes 
    pi = mdl.sequence_var(vars = [itvs[i] for i in range(len(itvs))], types = type_l)
    
    # This is to enforce the distance the aircraft has to travel from request to request
    mdl.add( mdl.no_overlap(pi, transition_dist_for_cp) )
    # Start from the depot and end in the depot.
    mdl.add( mdl.first(pi, itvs[0]))
    mdl.add( mdl.last(pi, itvs[2*n +1]))
    
    # Enforce the upper bound on the objective function
    mdl.add( mdl.end_of(itvs[2*n +1]) <= obj_val)

    for i in range(1, n+1): #Pickup BEFORE Delivery
        mdl.add(mdl.end_before_start(itvs[i], itvs[i+n]))

    mdl.add(
        mdl.minimize(
            mdl.end_of(itvs[2*n +1])
        )
    )

     #----------- Initialize empty solution object for the initial solution -------------
    stp = mdl.create_empty_solution()
    
    prev_node = None # Initialize the previous node
    current_time = None
    for i in range(len(tour)):
        if i == 0:
            current_time = 0
            stp.add_interval_var_solution(itvs[i], start = current_time)
            prev_node = 0
        else:
            pickup = tour[i]
            delivery = pickup + n
            travel_diff_req = transition_dist[prev_node][pickup] # Travel to the pickup node
            current_time = current_time + travel_diff_req
            stp.add_interval_var_solution(itvs[pickup], start = current_time)

            travel_same_req = transition_dist[pickup][delivery] # Travel to the delivery node
            current_time = current_time + travel_same_req
            stp.add_interval_var_solution(itvs[delivery], start = current_time)
            prev_node = delivery

    travel_back_depot = transition_dist[prev_node][0] # Travel back to the depot after fulfilling all the inquries.
    current_time = current_time + travel_back_depot
    stp.add_interval_var_solution(itvs[2*n+1], start = current_time)

    
    actual_changes_seats = pick_most_seats(tour, config_0_seat, seats_0, p, q, S_hat, C_hat, L)
    for i in range(len(tour)):
        if i == 0:
            stp.add_integer_var_solution(change_of_seats[i], value = actual_changes_seats[0])
        else:
            stp.add_integer_var_solution(change_of_seats[tour[i]], value = actual_changes_seats[2*i-1])
            stp.add_integer_var_solution(change_of_seats[tour[i]+n], value = actual_changes_seats[2*i])
    mdl.set_starting_point(stp)
    

    
    print("\nSolving model....")

    # msol = mdl.solve(TimeLimit = time_limit, log_output = None)
    # msol = mdl.solve(mdl, TimeLimit = time_limit)
    
    # Initiate the solving process with a Callback function that is triggered every time a new solution is found
    solver = CpoSolver(mdl, TimeLimit = time_limit,
                      execfile='/opt/ibm/ILOG/CPLEX_Studio201/cpoptimizer/bin/x86-64_linux/cpoptimizer')

    msol = []
    has_next_sol = True
    while has_next_sol:
        has_next_sol = solver.search_next()
        msol.append(has_next_sol)
        


    print("done")
    return msol, itvs, pi, change_of_seats, obj_val



def get_solution_detail(instance_name, msol, csv_file, itvs, pi, change_of_seats, p, q, n, config_0_seat, config_0_cargo):   
    '''

    This function converts the CpoSolveResult Object into detailed solution
    in forms of lists and dictionaries

    '''
    
    p.append(0) #list of passenger requests for all the locations to visit in the ascending order of location index
    q.append(0) #list of cargoes equests for all the locations to visit in the ascending order of location index

    seats_changes = {} # change of seats as the travel continues
    tour = []
    pasenger_cap = {0: config_0_seat}
    cargo_cap = {0: config_0_cargo}

    # msol = msol[-1] # this is not working for some reason
    print("total number of solutions: ", len(msol))


    if msol: # If msol has any element solution that is not None [changed on Sunday]
        
        obj_val = msol[-1].get_objective_values()[0]
        time_elapsed = msol[-1].get_solve_time()
        optimality = msol[-1].get_solve_status()
        print("time elapsed:", time_elapsed)
        print("Solution status: ", optimality)
        print("Total distance will be "+str( obj_val ))
        

        n_cargo = {0:0} # The initial number of cargoes is 0
        n_cargo_current = 0 #The aircraft starts as empty
    
        n_passenger = {0:0} #The initial number of passengers is 0
        n_passenger_current = 0 #The aircraft starts as empty

        c_hat = cargo_cap[0] # The number of cargoes in the flight (updated real-time)
        p_hat = pasenger_cap[0] # The number of passengers in the flight (updated real-time)

        # Get the sequence variable details
        sequence_variable = msol[-1].get_var_solution(pi)
        sequence_values = sequence_variable.get_value()
        n_of_nodes = len(sequence_values)

        for i in range(0, 2*n+1):
            num_seat = msol[-1].get_value(change_of_seats[i])
            seats_changes[i] = num_seat
        print("Seats Changes: ", seats_changes)

        for v in sequence_values:
            
            nm = v.get_name()
            location_id = int(re.search("\d+", nm).group(0)) # Extract the node number
            tour.append(location_id)
            if location_id < (n_of_nodes-1): #and location_id > 0: # Excluding the depots
                # Number of cargos in the aircraft at each location
                n_cargo[location_id] = n_cargo_current + q[location_id]
                n_cargo_current = n_cargo[location_id]

                # Number of passengers in the aircraftin at each location
                n_passenger[location_id] = n_passenger_current + p[location_id]
                n_passenger_current = n_passenger[location_id]

                # Available cargo space in each location
                c_hat = c_hat - q[location_id] - L * seats_changes[location_id]
                cargo_cap[location_id] = c_hat

                # Available passenger space(empty seats) in each location
                p_hat = p_hat - p[location_id] + seats_changes[location_id]
                pasenger_cap[location_id] = p_hat

        # cargo_cap = cumul_c
        # pasenger_cap = cumul_p
        

        with open(csv_file, 'a') as file:

            file.write(instance_name + "\n")
            file.write("Objective Value: " + str(obj_val) + "\n")
            file.write("Optimality: " + str(optimality) + "\n")
            file.write("Time Elapsed: " + str(time_elapsed) + "\n")
            file.write("Seats Changes: " + str(seats_changes) + "\n")
            file.write("Optimal Tour: "+ str(tour) + "\n")
            file.write("Remaining Cargo Space: "+ str(cargo_cap) +"\n")
            file.write("Remaining Empty Seats: "+ str(pasenger_cap) +"\n")
            file.write("Current Cargo: "+ str(n_cargo) + "\n")
            file.write("Current Passenger :" +str(n_passenger) +"\n")
            file.write("\n")

        return obj_val, seats_changes, tour, cargo_cap, pasenger_cap, n_cargo, n_passenger
    

def get_solution_search_next(msol_all, points, upperbound):
    '''

    This function iterates through a List of CpoSolveResult Object 
    and record changes in solution and change time into a dictionary

    '''

    solvings = [(0, upperbound)]
    for msol in msol_all:
        
        have_solution = msol.get_objective_values()
        if have_solution:
            obj_val = have_solution[0]
        else:
            obj_val = upperbound
            
        time_elapsed = msol.get_solve_time()
        solvings.append((time_elapsed, obj_val))
        
    return solvings


def n_dist_matrix(points):
    '''

    This function generates the distance matrix that will be passed into 
    the MILP model that generates upper bound solutions

    '''


    visit = len(points)//2
    matrix_of_dist = np.zeros(shape=(visit, visit))
    for i in range(visit):
        for j in range(visit):
            if i == 0:
                start_loc = points[i]
            else:
                start_loc = points[i+visit-1]
            end_loc = points[j]
            matrix_of_dist[i][j] = math.ceil(math.hypot(start_loc[0]-end_loc[0], start_loc[1] - end_loc[1]))
    num_rows, num_cols = matrix_of_dist.shape
    dist = {(i, j): matrix_of_dist[i][j] for i in range(num_rows) for j in range(num_cols)}
    return dist

def pick_most_seats(tour, config_0_seat, seats_0, p_hat, q_hat, S_hat, C_hat, L) -> list:
    '''
    
    This function checks if the seat constraint will be violated even though 
    the aircraft picks up as many seats as possible
    
    '''


    seats_total = config_0_seat
    satisfied = True
    pickup_seats = []

    for t in tour:
    
        # Pick up seats at the pickup location
        seats_new = min(S_hat, seats_total+seats_0[t], C_hat/L  + S_hat - q_hat[t]/L)
        pickup_seats.append(int(seats_new - seats_total))
        seats_total = seats_new

        if seats_total < p_hat[t]:
            print("seats_total: ",seats_total, " Tour: ", t)
            satisfied = False
            return satisfied

        # Pick up seats at the delivery locaton
        if t != 0:
            seats_new = min(seats_total+seats_0[t+len(tour)-1], S_hat)
            pickup_seats.append(int(seats_new - seats_total))
            seats_total = seats_new
        
    
    return pickup_seats



        
