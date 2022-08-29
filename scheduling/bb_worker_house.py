import sys
from docplex.cp.model import *

NbHouses = 5

WorkerNames = ["Joe", "Jim"]

TaskNames = ["masonry", "carpentry", "plumbing", 
             "ceiling", "roofing", "painting", 
             "windows", "facade", "garden", "moving"]

Duration =  [35, 15, 40, 15, 5, 10, 5, 10, 5, 5]

Worker = {"masonry"  : "Joe" , 
          "carpentry": "Joe" , 
          "plumbing" : "Jim" , 
          "ceiling"  : "Jim" , 
          "roofing"  : "Joe" , 
          "painting" : "Jim" , 
          "windows"  : "Jim" , 
          "facade"   : "Joe" , 
          "garden"   : "Joe" , 
          "moving"   : "Jim"}

ReleaseDate = [  0,     0,   151,    59,   243]
DueDate     = [120,   212,   304,   181,   425]
Weight      = [100.0, 100.0, 100.0, 200.0, 100.0]

Precedences = [("masonry", "carpentry"),("masonry", "plumbing"),
               ("masonry", "ceiling"), ("carpentry", "roofing"),
               ("ceiling", "painting"), ("roofing", "windows"),  
               ("roofing", "facade"), ("plumbing", "facade"),
               ("roofing", "garden"), ("plumbing", "garden"),
               ("windows", "moving"), ("facade", "moving"),  
               ("garden", "moving"), ("painting", "moving")]

Houses = range(NbHouses)

mdl2 = CpoModel()

houses = [mdl2.interval_var(start = (ReleaseDate[i], INTERVAL_MAX), name ="house"+str(i)) for i in Houses]
TaskNames_ids = {}
itvs = {}
for h in Houses:
    for i, t in enumerate(TaskNames):
        _name = str(h) + "_" + str(t)
        itvs[(h,t)] = mdl2.interval_var(size = Duration[i], name = _name)
        TaskNames_ids[_name] = i

for h in Houses:
    for p in Precedences:
        mdl2.add(mdl2.end_before_start(itvs[(h, p[0])], itvs[(h, p[1])]))

for h in Houses:
    mdl2.add(mdl2.span(houses[h], [itvs[(h,t)] for t in TaskNames]))

transitionTimes = transition_matrix([[int(abs(i-j)) for i in Houses] for j in Houses])

workers = {w: mdl2.sequence_var([ itvs[(h,t)] for h in Houses for t in TaskNames if Worker[t]==w ],
                                types = [h for h in Houses for t in TaskNames if Worker[t]==w ], name="workers_"+w)
            for w in WorkerNames}
for w in WorkerNames:
    mdl2.add( mdl2.no_overlap(workers[w], transitionTimes) )

mdl2.add(
    mdl2.minimize(
        mdl2.sum(Weight[h] *mdl2.max([0, mdl2.end_of(houses[h]) - DueDate[h]]) + mdl2.length_of(houses[h]) for h in Houses)
    )
)

print("\nSolving model....")
msol2 = mdl2.solve(FailLimit=30000)
print("done")

if msol2:
    print("Cost will be " + str(msol2.get_objective_values()[0]))
else:
    print("No solution found")

import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
# %matplotlib inline
#Change the plot size
from pylab import rcParams
rcParams['figure.figsize'] = 15, 3

visu.timeline('Solution SchedOptional', 0, msol5.get_var_solution(var))

for var in itvs:
    wt = msol5.get_var_solution(var)
    if wt.is_present():
        #if desc[t].skills[w] == max(desc[t].skills):
            # Green-like color when task is using the most skilled worker
        #    color = 'lightgreen'
        #else:
                # Red-like color when task does not use the most skilled worker
        #    color = 'salmon'
        color = 'salmon'
        visu.interval(wt, color, wt.get_name())
visu.show()
else:
    print("No solution found")