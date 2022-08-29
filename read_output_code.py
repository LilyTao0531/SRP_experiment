import glob
import os
import numpy as np
import csv
import pandas as pd
from sys import argv
import re
#to run:
#python read_output.py
#python read_output.py results_m2_total_cap SRP_results_m2.csv

def read_output(sol_dir, result_folder, csv_file):
    
    #csv_file = argv[2]
    with open(csv_file, 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["file_name", "number_commodities", "obj", "number_nodes", "time_optimality", "time_feasibility", "gap", "solution_status"])
        print("line file size obj node time feas_time gap status")
        #result_folder = str(argv[1])
        path0 = os.path.join(sol_dir,result_folder)
        print("path0", path0)
        for file1 in os.listdir(path0): #os.listdir('C:/Python/SRP/results_m2'):

            opt, check, feas, infeas, feas_time_check, time_limit_reached, feas_time, check_infeasibility = 0, 0, 0, 0, 0, 0, 0, 0 
            obj, node, time, feas_time, gap = 0,0,0,0,0 #initialize them for the next instance
            #for file1 in files:
            if file1.endswith(".txt"):
                #fname = '/home/arnoosh/Research/Python/SRP/output-m2'+"/"+file1
                fname = path0 + "/"+ file1 #'C:/Python/SRP/results_m2'+"/"+file1
                solvings = []
                with open(fname) as infile:
                    #print("file_name", file1)
                    file_size = int(file1.split("_")[0])
                    
                    for line in infile:
                        # This is to record each of the search status and the solution changes over time
                        # t_sol_pair = []
                        # if "time to find feasible solution is" in line:
                        #     t_sol_pair.append()

                        # if line[0] == "H" and ord(line[1]) <= 57 :
                        #     indiv_record = re.findall('[a-zA-Z]+|\d*\.?\d+', line)
                        #     time_point = float(indiv_record[-2])
                        #     obj_val = float(indiv_record[3])
                        #     solvings.append((time_point, obj_val))                    
                        
                        line_l = line.split()
                        if "Best objective" in line:                        
                            obj = line_l[2]
                            obj = obj.rstrip(',')
                            gap = line_l[7]
                            gap = gap.rstrip()
                             
                            #if gap == '-':
                                #gap = 'nan'
                            check = 1
                            #print("obj", obj)
                            #print(gap)
                        if "Explored" in line:
                            time = line_l[7]
                            time = float(time.rstrip())
                            time = round(time, 4)
                            node = line_l[1]
                            node = node.rstrip()
                            #print('node', node)
                            check = 1
                        if "Changed value of parameter TimeLimit to" in line:
                            time_limit = line_l[6]
                            time_limit = time_limit.rstrip()
                        if "time to find feasible solution is" in line and feas_time_check == 0:
                            feas_time = line_l[6]
                            feas_time = feas_time.rstrip()
                            feas_time = float(feas_time)
                            feas_time = round(feas_time,4)
                            feas_time_check = 1
                            #print('feas_time', feas_time)
                        if "Optimal solution found" in line:
                            opt =1
                            feas = 1
                        if "Model is infeasible" in line:
                            infeas = 1
                            check_infeasibility = check_infeasibility +1
                        if "Optimization reaches the time limit" in line or "Time limit reached" in line: #shouldn't be in this line always??!!
                            time_limit_reached = 1
                    if check == 0:
                        obj, gap, node, time, feas_time = "nan", "nan", "nan", "nan", "nan"
    
            if time_limit_reached ==1:
                if feas ==1 and opt ==0:
                    writer.writerow([file1, file_size, obj, node, time, feas_time, gap, "feasible"])
                    # print("line", file1, file_size, obj, node, time, feas_time, gap, "feasible")
                elif opt ==1:
                    writer.writerow([file1, file_size, obj, node, time, feas_time, gap, "optimal"])  
                    # print("line", file1, file_size, obj, node, time, feas_time, gap, "optimal")                
                else:            
                    writer.writerow([file1, file_size, obj, node, time, feas_time, gap, "time_limit_reached"])
                    # print("line", file1, file_size, obj, node, time, feas_time, gap, "time_limit_reached")
            else:
                if opt == 1:
                    writer.writerow([file1, file_size, obj, node, time, feas_time, gap, "optimal"])  
                    # print("line", file1, file_size, obj, node, time, feas_time, gap, "optimal")
                elif check_infeasibility == 1:
                    gap = 0 #infeasible instances have optimal gap of 0
                    # print("time is", time)
                    writer.writerow([file1, file_size, "nan", node, time, "nan", gap, "infeasible"])
                    # print("line",file1, file_size, "nan", node, time, "nan", gap, "infeasible")
            
            # infile.close()            

#to read output of specific instance
# =============================================================================
# opt, check, feas, infeas, feas_time_check, time_limit_reached, feas_time, check_infeasibility = 0, 0, 0, 0, 0, 0, 0, 0 
# obj, node, time, feas_time, gap = 0,0,0,0,0 #initialize them for the next instance
# file1 = "20_90.txt"
# 
# print("file_name", "number_commodities", "obj", "number_nodes", "time_optimality", "time_feasibility", "gap", "solution_status")
# fname = 'C:/Python/SRP/results_m2'+"/"+file1
# with open(fname) as infile:
#     #print("file_name", file1)
#     file_size = int(file1.split("_")[0])
#     for line in infile:
#         #print("line", line)
#         line_l = line.split()
#         if "Best objective" in line:                        
#             obj = line_l[2]
#             obj = obj.rstrip(',')
#             gap = line_l[7]
#             gap = gap.rstrip()
#              
#             #if gap == '-':
#                 #gap = 'nan'
#             check = 1
#             #print("obj", obj)
#             #print(gap)
#         elif "Explored" in line:
#             time = line_l[7]
#             time = float(time.rstrip())
#             time = round(time, 4)
#             node = line_l[1]
#             node = node.rstrip()
#             #print('node', node)
#             check = 1
#         elif "Changed value of parameter TimeLimit to" in line:
#             time_limit = line_l[6]
#             time_limit = time_limit.rstrip()
#         elif "time to find feasible solution is" in line and feas_time_check == 0:
#             feas_time = line_l[6]
#             feas_time = feas_time.rstrip()
#             feas_time = float(feas_time)
#             feas_time = round(feas_time,4)
#             feas_time_check = 1
#             #print('feas_time', feas_time)
#         elif "Optimal solution found" in line:
#             opt =1
#             feas = 1
#         elif "Model is infeasible" in line:
#             infeas = 1
#             check_infeasibility = check_infeasibility +1
#         elif "Optimization reaches the time limit" in line or "Time limit reached" in line: #shouldn't be in this line always??!!
#             print("time limit line", line)
#             time_limit_reached = 1
#     if check == 0:
#         obj, gap, node, time, feas_time = "nan", "nan", "nan", "nan", "nan"
# 
#     elif time_limit_reached ==1:
#         if feas ==1 and opt ==0:
#             print("line", file1, file_size, obj, node, time, feas_time, gap, "feasible")
#         elif opt ==1:
#             print("line", file1, file_size, obj, node, time, feas_time, gap, "optimal")                
#         else:            
#             print("line", file1, file_size, obj, node, time, feas_time, gap, "time_limit_reached")
#     else:
#         if opt == 1:
#             print("line", file1, file_size, obj, node, time, feas_time, gap, "optimal")
#         elif check_infeasibility == 1:
#             gap = 0 #infeasible instances have optimal gap of 0
#             print("line",file1, file_size, "nan", node, time, "nan", gap, "infeasible")
# 
# infile.close()            
# 
# 
# 
# 
# 
# 
# 
# =============================================================================



















