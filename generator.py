import os
import re
from sys import argv
import random
from random import randint
import io

def write_file(file_inst, seed_num, points0, seats_0, config_0, q, ro, n, Q, L, C):
    file1 = io.open(file_inst,"w", encoding="UTF-8")

    line1 = str(seed_num)+ ' '+ str(n)+' '+ str(Q)+' '+ str(L)+' '+ str(C)
    file1.writelines(line1)
    file1.writelines('\n')
    
    line2 = str(config_0[0])+' '+ str(config_0[1])
    file1.writelines(line2)
    file1.writelines('\n')
    
    for i in range(2*n+1):
        line3 = str(seats_0[i]) + ' '
        file1.writelines(line3)
    file1.writelines('\n')
    
    for i in range(2*n+1):
        line = str(i) + ' '+  str(points0[i][0]) + ' '+ str(points0[i][1]) + ' '+  str(q[i]) + ' ' + str(ro[i])
        file1.writelines(line)
        file1.writelines('\n')
    file1.close() 
    return

def generate_inst(inst_dir, n, count):

    
    S = 6 #maximum number of passengers/seats in a flight
    L = 100 #removal of one seat can add 10 kg of cargo
    C = 200 #When aircraft is full of passengers, we can carry up to C kg of cargo
    path = os.path.join(inst_dir, "new_instance_200")

    # path = os.path.join(inst_dir, "new_instance_"  + str(n))
    
    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")
        
    
    for k in range(count):
        r = random.randint(1,1000)
        random.seed(r)

        name_of_file = str(n)+"_"+str(r)+".txt"
        file_inst = os.path.join(path, name_of_file)    
        print("file_inst", file_inst)

        S_0 = random.randint(0, S)
        C_0 = C+S*L - S_0*L
        config_0 = [S_0, C_0] #the aircraft start configuration (it doesn't have to be full)
        seats_0 = [ random.randint(0, S) for i in range(2*n+1) ] #does not make sense to have more than Q seats at bases, but it could be changed
        points0 = [ ( random.randint(0, 100), random.randint(0, 100) ) for i in range(2*n+1) ]
        # points0.append(points0[0])

        sum_q_ro = {i+1: randint(1,int(S+C/100)) for i in range(n)}
        
        ro = {i+1: randint(0,min(sum_q_ro[i+1], S)) for i in range(n)} #for now we assumed only half of the passenger capacity can be full
        # ro_list.insert(0, 0)
        q = {i+1: 100*(sum_q_ro[i+1] - ro[i+1]) for i in range(n)} #for now we assumed only half of the cargo capacity can be full
        # q_list.insert(0, 0)
            
        for i in range(1, n+1):
            ro[n+i] = -ro[i]
            q[n+i] = -q[i]
        q[0] = q[2*n+1] = 0
        ro[0] = ro[2*n+1] = 0

        write_file(file_inst, r, points0, seats_0, config_0, q, ro, n, S, L, C)

def generate_all_inst(inst_dir,inst_sizes_list,count):
    for n in inst_sizes_list:
        generate_inst(inst_dir, n, count)
    print("All the instances are generated")


# inst_sizes_list = [4,6,8]
# count=1
# generate_all_inst(inst_sizes_list, count)