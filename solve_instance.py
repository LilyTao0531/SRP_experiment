import os, sys

def solve_m2(inst_name, time_lim):

    #new_inst_dir = "C:/Python/SRP/test_rand_inst"
    new_inst_dir = "/Users/user/SRPproject/Cplex_copy/new_instance"

    name_of_file =  inst_name#argv[1]#"5_426.txt" #"5_34_c109.txt" #"5-101-"+str(r) argv[1]#
    
    file_inst = os.path.join(new_inst_dir, name_of_file)   
    
    new_result_dir = "/Users/user/SRPproject/Cplex_copy/results_m2"
    
    path = new_result_dir
    # Check whether the specified path exists or not
    check_existed = os.path.exists(path)
    if not check_existed:  
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")
    result_file = os.path.join(new_result_dir, name_of_file)  
    
    instanceName = file_inst
    
    with open(instanceName,"r") as instance:
        line = instance.readline()
        nb_seed, n, S_hat, L, C_hat = (int(x) for x in line.split())
        line = instance.readline()
        config_0_seat, config_0_cargo = (int(x) for x in line.split())
        line = instance.readline()
        seats_0 = line.split()
        seats_0 = [int(k) for k in seats_0]
        dist_V = {}
        dist_v_0 = {}
        dist_v_N1 ={}
        q_hat = {}
        pi_hat = {}
        line = instance.readline()
        i = int(line.split()[0])
        x = int(line.split()[1])
        y = int(line.split()[2])
        q_hat0 = int(line.split()[3]) 
        pi_hat0 = int(line.split()[4])
        point0 = (x,y)
        dist_v_0[i] = point0 #depot node
        dist_v_N1[2*n+1] = point0
        q_hat[i] = q_hat0
        pi_hat[i] = pi_hat0
        for j in range(1,2*n+1):
            line = instance.readline()
            i = int(line.split()[0])
            x = int(line.split()[1])
            y = int(line.split()[2])
            q_hat0 = int(line.split()[3]) 
            pi_hat0 = int(line.split()[4])
            point0 = (x,y)
            dist_V[i] = point0
            q_hat[i] = q_hat0
            pi_hat[i] = pi_hat0
    
    q_hat[2*n+1] = q_hat[0]
    pi_hat[2*n+1] = pi_hat[0]
    
    #print("q_hat is", q_hat)
    
    #print("pi_hat is", pi_hat)
    
    def subtour(edges):
        #print("edges are", type(edges))
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
# =============================================================================
# =============================================================================
# #     def subtour(edges):
# #         unvisited = list(range(n))
# #         cycle = range(n+1)  # initial length has 1 more city
# #         while unvisited:  # true if list is non-empty
# #             thiscycle = []
# #             neighbors = unvisited
# #             while neighbors:
# #                 current = neighbors[0]
# #                 thiscycle.append(current)
# #                 unvisited.remove(current)
# #                 neighbors = [j for i, j in edges.select(current, '*')
# #                              if j in unvisited]
# #             if len(cycle) > len(thiscycle):
# #                 cycle = thiscycle
# #             #print(cycle)
# #         return cycle
# #     
# =============================================================================
# =============================================================================
    dist_V_0 = merge_two_dicts(dist_V,dist_v_0) #set(V).union(v_0)
    dist_V_N1 = merge_two_dicts(dist_V,dist_v_N1)#set(V).union(v_N1) #V_{N+1}
    dist_V_0N1 = merge_two_dicts(dist_V_0,dist_v_N1)
    
    
    
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
                arc_dist[(i,j)] = get_dist(p1 , p2)
    
    arcs = list(arc_dist.keys())
    
    P = list(range(1,n+1))#dict(list(V.items())[:n]) #pickup vertices
    D = list(range(n+1,2*n+1)) #dict(list(V.items())[n:]) #delivery vertices
    
    arcs = list(arc_dist.keys())
       
            
    Big_M = len(V)
    Big_M_cargo = C_hat+2*S_hat*L
    Big_M_passenger = 2*S_hat
    
                
    #time_lim = 1000
    S_0 = seats_0#0 #for now there are no seats at bases, and these are added as upperbound, when variable I think they be added as constraints
    
    start_time = time.time()
    
    #print("start_time", start_time)
    
    
    
    start_time = time.time()
    
    m = Model("SRP-VRP")
    vars = m.addVars(arcs,vtype=GRB.BINARY, name='vars')
    t = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, name='t') #arrival time at vertex i #lb = 0
    
    u = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='u') #remaining cargo space
    y = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='y') #remaining passenger seats
    #s = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = -9, ub = S_0, name='s') #number of seats picked up or stored at base i (positive or negative)
    s = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb =  -S_hat, ub = S_hat, name='s') #number of seats picked up or stored at base i (positive or negative)
    pi = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, name='pi') #number of passengers in the aircraft when leaving location j
    q = m.addVars(len(V_0N1),vtype=GRB.CONTINUOUS, lb = 0, ub = C_hat+S_hat*L, name='q') #kg of cargo in the aircraft when leaving location i
    
    
    #initial values of t, u and y (since definition of u in VRP and SRP are different the initial values will be different)
    m.addConstr(t[0] == 0)
    m.addConstr(u[0] == config_0_cargo) #C_hat
    m.addConstr(y[0] == config_0_seat) #S_hat
    #m.addConstr(s[0] == 0)
    #m.addConstr(s[1] == 0)
    #m.addConstr(s[2] == 0)
    #m.addConstr(s[3] == 0)
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
            
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(u[j] <= u[i] -L*s[i]- q_hat[i]*vars[(i,j)] + Big_M_cargo*(1-vars[(i,j)]), "cargo_delivery"+str(i)+","+str(j))
    
    
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(u[j] >=  u[i] -L*s[i]-q_hat[i]*vars[(i,j)]-Big_M_cargo*(1-vars[(i,j)]) , "cargo_delivery"+str(i)+","+str(j))
    
    
    
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(y[j] <= y[i]+s[i]- pi_hat[i]*vars[(i,j)] + Big_M_passenger*(1-vars[(i,j)]), "passenger_delivery"+str(i)+","+str(j))
    
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(y[j] >= y[i]+s[i]- pi_hat[i]*vars[(i,j)] -Big_M_passenger*(1-vars[(i,j)]), "passenger_delivery"+str(i)+","+str(j))
    
    
# =============================================================================
#     for i in V_N1:
#         m.addConstr( u[i]+L*y[i] <= C_hat+S_hat*L, "u_y_relationship"+ str(i))
# =============================================================================
        
    for i in V_N1:
        m.addConstr( -y[i] <= s[i], "seats_lb"+ str(i))
            
        
    for i in V_0:
        m.addConstr( s[i] <= S_0[i], "s_ub_domain"+ str(i)) 
    
     
    pi[0] == 0
    for i in V_0:
        for j in V_N1: 
            if i != j:
                m.addConstr(pi[j] >= pi[i] + pi_hat[i]*vars[(i,j)]-(1-vars[(i,j)])*S_hat, "current_pass"+str(i)+","+str(j)) 
    
    
    
    for i in V_0:
        m.addConstr(y[i]+pi[i] <= S_hat, "max_seats"+str(i)) 
    
    
    for i in V_0:
        m.addConstr(u[i]+q[i]+L*y[i]+L*pi[i] <= C_hat+S_hat*L, "u_y_relationship"+str(i)) 
   
    for i in V_0N1:
        m.addConstr(y[i]+pi[i]+s[i] <= S_hat, "max_seats"+str(i)) 
    
    
    for i in V_0N1:
        m.addConstr(pi[i]+pi_hat[i] <= S_hat, "max_seats"+str(i)) 
    
    
    big_k = C_hat+S_hat*L  
    q[0] == 0
    for i in V_0:
        for j in V_N1:
            if i != j:
                m.addConstr(q[j] >= q[i] + q_hat[i]*vars[(i,j)]-(1-vars[(i,j)])*big_k, "current_cargo"+str(i)+","+str(j)) 
    
    
    
    m.setObjective(sum(vars[(i,j)]*arc_dist[(i,j)] for i in V_0 for j in V_N1 if i !=j),GRB.MINIMIZE)
    
    #sys.stdout = open(result_file, "w")
    
    m.Params.LogToConsole = 0
    m.setParam('TimeLimit', time_lim)
    m.Params.Threads = 4
    m.Params.OptimalityTol = 1e-6
    m.params.FeasibilityTol = 1e-6
    m.Params.LogFile = result_file
    #m.setParam('TimeLimit', time_lim)
    #m.Params.LogFile = result_file
    #m.params.FeasibilityTol = 1e-6
    m.optimize(get_time_feas)
    
    #name = "PD-2SRP"
    #name_lp_ell = name+".lp"
    #m.write(name_lp_ell)
    
# =============================================================================
#     def subtour(edges):
#         #print("edges are", type(edges))
#         unvisited = list(range(2*n+2)) # or V_0N1
#         cycle = range(2*n+3)  # initial length has 1 more city
#         while unvisited:  # true if list is non-empty
#             thiscycle = []
#             neighbors = unvisited
#             while neighbors:
#                 current = neighbors[0]
#                 thiscycle.append(current)
#                 unvisited.remove(current)
#                 neighbors = [j for i, j in edges.select(current, '*')
#                              if j in unvisited]
#             if len(cycle) > len(thiscycle):
#                 cycle = thiscycle
#             #print(cycle)
#         return cycle
# =============================================================================
    
    
    
    
    with open(result_file, 'a') as file:  # Use file to refer to the file object
        #try:
        if m.status == GRB.INFEASIBLE:
            file.write("No solution is found")  

        
        else:
            file.write("status is:"+ str(m.status))
            dict_y = m.getAttr('x', y) #pass
        
            dict_u = m.getAttr('x', u) #cargo
         
            dict_s = m.getAttr('x', s)
          
            dict_z = m.getAttr('x', vars)
            
            dict_pi = m.getAttr('x', pi)
            dict_q = m.getAttr('x', q)
            
            dict_seats = rounded_dict(dict_s,6)
            dict_remaining_cargo = rounded_dict(dict_u,6)
            dict_remaining_pass = rounded_dict(dict_y,6)
            
            dict_cargo = rounded_dict(dict_q,6)
            dict_pass = rounded_dict(dict_pi,6)
            
            
            
            vals = m.getAttr('x', vars)
            
            selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
            #gp.tuplelist((i, j) for i, j in edge_val)
            
            
            
            tour = subtour(selected)
            
            #print('')
            file.write('\nOptimal tour: '+ str(tour))
            #print('Optimal tour: %s' % str(tour))
            #print('Optimal cost: %g' % m.objVal)
            file.write('\nOptimal cost: ' + str(m.objVal))
            #print('')
            #print('Seats changes: %s' %str(dict_seats))
            file.write('\nSeats changes: ' + str(dict_seats))
            
            #print('\npicked up seats\n')            
            file.write('\npicked up seats\n')       
            for i in V_0N1:
                if s[i].x >= 0.0001:
                    #print("number of seats picked up at base:",i,round(s[i].x,4))         
                    file.write("\nnumber of seats picked up at base "+str(i)+" is "+str(round(s[i].x,4))) 
            #print('\narrival time:\n')  
            file.write('\narrival time:\n')
            #continue from here
            for i in V_0:
                if t[i].x>= 0.99:
                    #print("arrival time of vertex:",i,round(t[i].x,6))
                    file.write("\narrival time of vertex "+str(i)+" is "+str(round(t[i].x,6)))
                                
            file.write("\ntotal time: "+ str(round(time.time()- start_time,2)))
            file.write("\nFinal MIP gap value:"+ str(m.MIPGap))
            #file.write("\ntime to find feasible solution is "+ str(m.cbGet(GRB.Callback.RUNTIME)))
            file.write("\nChecking:\n")
            
            file.write("Remaining cargo space:"+ str(dict_remaining_cargo))
            file.write("\n")
            file.write("Remaining passenger space:\n"+ str(dict_remaining_pass))
            file.write("\n")
            
            file.write("current passenger:"+ str(dict_pass))
            file.write("\n")
            file.write("current cargo:"+ str(dict_cargo))
            file.write("\n")