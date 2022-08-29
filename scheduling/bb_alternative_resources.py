from asyncio import Task
import sys
from docplex.cp.model import *

mdl5 = CpoModel()

NbHouses  = 5
Deadline = 318

Workers = ["Joe", "Jack", "Jim"]

TaskNames = {"masonry","carpentry","plumbing",
             "ceiling","roofing","painting",
             "windows","facade","garden","moving"}

Duration =  [35, 15, 40, 15, 5, 10, 5, 10, 5, 5]

Skills = [("Joe","masonry",9),("Joe","carpentry",7),("Joe","ceiling",5),("Joe","roofing",6), 
          ("Joe","windows",8),("Joe","facade",5),("Joe","garden",5),("Joe","moving",6),
          ("Jack","masonry",5),("Jack","plumbing",7),("Jack","ceiling",8),("Jack","roofing",7),
          ("Jack","painting",9),("Jack","facade",5),("Jack","garden",5),("Jim","carpentry",5),
          ("Jim","painting",6),("Jim","windows",5),("Jim","garden",9),("Jim","moving",8)]

Precedences = [("masonry", "carpentry"), ("masonry", "plumbing"), ("masonry", "ceiling"),
               ("carpentry", "roofing"), ("ceiling", "painting"), ("roofing", "windows"),
               ("roofing", "facade"), ("plumbing", "facade"), ("roofing", "garden"),
               ("plumbing", "garden"), ("windows", "moving"), ("facade", "moving"),
               ("garden", "moving"), ("painting", "moving")]

Continuities = [("Joe","masonry","carpentry"),("Jack","roofing","facade"), 
                ("Joe","carpentry", "roofing"),("Jim","garden","moving")]

nbWorkers = len(Workers)
Houses = range(NbHouses)

itvs={}
wtasks={}
for h in Houses:
    for i, t in enumerate(TaskNames):
        itvs[(h,t)] = mdl5.interval_var(start=[0, Deadline],size = Duration[i])
    for s in Skills:
        wtasks[(h,s)] = mdl5.interval_var(optional=True)

for h in Houses:
    for p in Precedences:
        mdl5.add(mdl5.end_before_start(itvs[h, p[0]], itvs[h, p[1]]))

#Alternative Constraints
for h in Houses:
    for t in TaskNames:
        mdl5.add( mdl5.alternative(itvs[h,t], [wtasks[h,s] for s in Skills if s[1]==t]))

for h in Houses:
    for c in Continuities:
        for (w1, t1, level1) in Skills:
            if w1 == c[0] and t1 == c[1]:
                for (w2, t2, level2) in Skills:
                    if w2 == c[0] and t2 == c[2]:
                        mdl5.add(
                            mdl5.presence_of(wtasks[h, (c[0], t1, level1)])
                            ==
                            mdl5.presence_of(wtasks[h, (c[0], t2, level2)])
                        )

for w in Workers:
    mdl5.add( mdl5.no_overlap([wtasks[h,s] for h in Houses for s in Skills if s[0]==w]))

mdl5.add(
    mdl5.maximize(
        mdl5.sum( s[2] * mdl5.presence_of(wtasks[h,s]) for h in Houses for s in Skills)
    )
)

print("\nSolving model....")
msol5 = mdl5.solve(FailLimit=30000)
print("done")

if msol5:
    print("Cost will be "+str( msol5.get_objective_values()[0] ))

    worker_idx = {w : i for i,w in enumerate(Workers)}
    worker_tasks = [[] for w in range(nbWorkers)]  # Tasks assigned to a given worker
    for h in Houses:
        for s in Skills:
            worker = s[0]
            wt = wtasks[(h,s)]
            worker_tasks[worker_idx[worker]].append(wt)

    import docplex.cp.utils_visu as visu
    import matplotlib.pyplot as plt
    # %matplotlib inline
    #Change the plot size
    from pylab import rcParams
    rcParams['figure.figsize'] = 15, 3

    visu.timeline('Solution SchedOptional', 0, Deadline)
    for i,w in enumerate(Workers):
        visu.sequence(name=w)
        for t in worker_tasks[worker_idx[w]]:
            wt = msol5.get_var_solution(t)
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
