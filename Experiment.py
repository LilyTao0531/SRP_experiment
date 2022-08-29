from distutils.command.build_clib import build_clib
import numpy as np
from gurobipy import *
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB
import time
import os, sys
from models.m2_code import solve_m2
from models.m2_total_cap_code import solve_m2_total_cap
from models.m3_code import solve_m3
from models.model_cp import build_and_solve, get_solution_search_next 

from checker import check_code
from checker_cp import check_cp_output

from generator import generate_all_inst
from read_output_code import read_output
from util import saveXP, generage_list_x, assign_values, assign_values_timeout, parse_instance_cp
from Compare import plotRE, plotMRE
import math
import logging

class Experiment:

    def __init__(self, solution_directory):
        self.solution_dir = solution_directory #"/home/lily/Cplex_copy/"

    def generate_instances(self, inst_sizes_list, count):
        logging.critical("inst generation")
        generate_all_inst(self.solution_dir, inst_sizes_list, count)

    def check_feasibility(self, inst_sizes_list, model_name_list, time_lim):

        '''
        This function solves the instances of specified size without generating plots or comparative results.

        The solution details for each instance are stored in the folder named "results_m3" for the MILP model
        (not for the CP model)

        The list of solutions for all instances are stored in the folder named "output"
        
        '''
        
        for s in inst_sizes_list:
            size = str(s)
            inst_dir = os.path.join(self.solution_dir, "new_instance_" + size)
            for inst_name in os.listdir(inst_dir):
                if inst_name == ".DS_Store": # This is to skip any DS_Store file
                    pass
                else:
                    #print(inst_name)
                    logging.critical(inst_name)
                    for model_name in model_name_list:
                        sol_dir_model =  os.path.join(self.solution_dir, "results_" + model_name)
                        
                        
                        output_dir = os.path.join(self.solution_dir, "output")
                        path = output_dir
                        # Check whether the specified path exists or not
                        check_existed = os.path.exists(path)
                        if not check_existed:  
                            # Create a new directory because it does not exist 
                            os.makedirs(path)
                        csv_file0 = "SRP_results_"+model_name+".csv"
                        csv_file = os.path.join(path, csv_file0)
                        result_folder = "results_" + model_name
                        
                        if model_name == 'm2':                  
                            solve_m2(inst_dir, sol_dir_model, inst_name, time_lim)
                            logging.critical("m2 code done!")
                            check_code(inst_dir, sol_dir_model, inst_name, model_name)
                            logging.critical("checker for m2 done!")
                            read_output(self.solution_dir, result_folder, csv_file)
                            logging.critical("reading output is done!")
                        elif model_name == 'm2_total_cap':
                            #sol_dir_model =  os.path.join(sol_dir, "results_" + "m2_total_cap") 
                            solve_m2_total_cap(inst_dir, sol_dir_model, inst_name, time_lim)
                            logging.critical("m2_total_cap code done!")
                            check_code(inst_dir, sol_dir_model, inst_name, model_name)
                            logging.critical("checker for m2_total_cap done!")
                            #csv_file = "SRP_results_"+model_name+".csv"
                            #result_folder = "results_" + model_name
                            read_output(self.solution_dir, result_folder, csv_file)
                            logging.critical("reading output is done!")
                            
                        elif model_name == 'm3':
                            #sol_dir_model =  os.path.join(sol_dir, "results_" + "m3") 
                            time_solution = solve_m3(inst_dir, sol_dir_model, inst_name, time_lim)
                            logging.critical("m3 code done!")
                            check_code(inst_dir, sol_dir_model, inst_name, model_name)
                            logging.critical("checker for m3 done!")
                            read_output(self.solution_dir, result_folder, csv_file)
                            logging.critical("reading output is done!")

                        elif model_name == 'cp':
                            dist_V, dist_V_N1, points, q, p, n, seat_max, L, C_hat, config_0_seat, config_0_cargo, s = parse_instance_cp(inst_dir, inst_name)
                            solution, itvs, pi, change_of_seats, obj_val= build_and_solve(time_lim, points, q, p, n, seat_max, L, config_0_seat, config_0_cargo, s, seat_max, C_hat)
                            logging.critical("cp code done!")
                            base = os.path.splitext(csv_file)[0]
                            # os.rename(csv_file, base + '.txt')
                            csv_file = base + '.txt'
                            check_cp_output(inst_dir, csv_file, inst_name, solution, itvs, pi, change_of_seats)
                            logging.critical("checker for cp done!")
                            # read_output(result_folder, csv_file)
                            # logging.critical("reading output is done!")

                        
                    logging.critical('file '+inst_name+' done\n')
    def compare_re(self, list_of_sizes, model_name_list, time_lim, time_increment = 0):
        '''
        This is the function that plots & compares the Mean Relative Error of the models

        The result dictionary per instance size is saved to .json file is saved and the plots are generated.
        
        '''
        
        
        for s in list_of_sizes:
            size = str(s)
            inst_dir = os.path.join(self.solution_dir, "new_instance_" + size)


            #Generate a list of numbers for x-axis.
            list_x = generage_list_x(time_lim, time_increment)
            
            #Initiate the dictionary that will be passed into the code for comparing Mean Relative Errors.
            result_dict = { 
                "instance_id": [],
                "methods": {},
                "x_axis": { 
                    "type": "time",
                    "steps":list_x   
                },
                "BKS":[]
            }

            #Attach empty lists for each method that will be used for comparison.
            for model_name in model_name_list:
                result_dict["methods"][model_name] = []

            for inst_name in os.listdir(inst_dir):
                instance_BKS = math.inf # This is the initial value of the Best Known Solution.
                if inst_name == ".DS_Store":
                    pass
                else:
                    result_dict["instance_id"].append(inst_name) #Append instance names to the result dictionary.
                    
                    logging.critical(inst_name)
                    for model_name in model_name_list:

                        sol_dir_model =  os.path.join(self.solution_dir, "results_" + model_name)
                        
                        
                        output_dir = os.path.join(self.solution_dir, "output")
                        path = output_dir
                        # Check whether the specified path exists or not; if not, create a new directory.
                        check_existed = os.path.exists(path)
                        if not check_existed:  
                            os.makedirs(path)

                        csv_file0 = "SRP_results_"+model_name+".csv"
                        csv_file = os.path.join(path, csv_file0) # This is the file that the solution info will be written into.
                        result_folder = "results_" + model_name
                            
                        if model_name == 'm3':
                            time_solution_tuple_m3 = solve_m3(inst_dir, sol_dir_model, inst_name, time_lim)
                            logging.critical("m3 code done!")

                            if not time_solution_tuple_m3: # Times out, fill the x_list with "TO"
                                assign_values_timeout(model_name, result_dict, list_x)
                            else:
                                assign_values(time_solution_tuple_m3, model_name, result_dict, list_x)
                            
                            check_code(inst_dir, sol_dir_model, inst_name, model_name)
                            logging.critical("checker for m3 done!")
                            read_output(self.solution_dir, result_folder, csv_file)
                            logging.critical("reading output is done!")

                            #Update BKS only when there's a solution before timeout
                            if result_dict["methods"][model_name][-1][-1] != "TO": 
                                # Update BKS when the most recent solution is better than exisitng BKS
                                if result_dict["methods"][model_name][-1][-1] < instance_BKS:
                                    instance_BKS = result_dict["methods"][model_name][-1][-1]

                        elif model_name == 'cp':
                            dist_V, dist_V_N1, points, q, p, n, seat_max, L, C_hat, config_0_seat, config_0_cargo, s = parse_instance_cp(inst_dir, inst_name)
                            
                            solution, itvs, pi, change_of_seats, upperbound = build_and_solve(time_lim, points, q, p, n, seat_max, L, config_0_seat, config_0_cargo, s, seat_max, C_hat)
                        
                            logging.critical("cp code done!")
                            base = os.path.splitext(csv_file)[0]
                            csv_file = base + '.txt' # This is the file that the solution info will be written into.
                            time_solution_tuple_cp = get_solution_search_next(solution, points, upperbound)
                            
                            if len(time_solution_tuple_cp) == 1 and time_solution_tuple_cp[0][1] == math.inf: # Times out, fill the x_list with "TO"
                                logging.critical("cp timed out with no solution!")
                                assign_values_timeout(model_name, result_dict, list_x)
                                pass
                            else:
                                assign_values(time_solution_tuple_cp, model_name, result_dict, list_x)
                                check_cp_output(inst_dir, csv_file, inst_name, solution, itvs, pi, change_of_seats)
                                logging.critical("checker for cp done!")
                            
                            # Update BKS only when there's a solution before timeout
                            if result_dict["methods"][model_name][-1][-1] != "TO":
                                # Update BKS when the most recent solution is better than exisitng BKS
                                if result_dict["methods"][model_name][-1][-1] < instance_BKS:
                                    instance_BKS = result_dict["methods"][model_name][-1][-1]

                        
                    logging.critical('file '+inst_name+' done\n')
                    # For every instance, attach the best available solution to "BKS" in result_dict
                    result_dict["BKS"].append(instance_BKS) 

            saveXP(result_dict, size + " result_json_file.json")
            # plotRE(result_dict, "Relative Error "+"Instance ", sol_dir + "/graphs/")
            plotMRE(result_dict, "for Instance with "+size + " requests", self.solution_dir + "/graphs/")
            


            