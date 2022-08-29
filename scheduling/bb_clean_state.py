NbHouses = 5
NbWorkers = 2
AllStates = ["clean", "dirty"]

TaskNames = ["masonry","carpentry", "plumbing", "ceiling","roofing","painting","windows","facade","garden","moving"]

Duration =  [35,15,40,15,5,10,5,10,5,5]

States = [("masonry","dirty"),("carpentry","dirty"),("plumbing","clean"),
          ("ceiling","clean"),("roofing","dirty"),("painting","clean"),
          ("windows","dirty")]

Precedences = [("masonry","carpentry"),("masonry","plumbing"),("masonry","ceiling"),
               ("carpentry","roofing"),("ceiling","painting"),("roofing","windows"),
               ("roofing","facade"),("plumbing","facade"),("roofing","garden"),
               ("plumbing","garden"),("windows","moving"),("facade","moving"),
               ("garden","moving"),("painting","moving")]
Houses = range(NbHouses)

import sys
from docplex.cp.model import *

mdl6 = CpoModel()

task = {}
for h in Houses:
    for i,t in enumerate(TaskNames):
        task[(h,t)] = mdl6.interval_var(size = Duration[i])

workers = step_at(0, 0)
for h in Houses:
    for t in TaskNames:
        workers += mdl6.pulse(task[h,t], 1)

Index = {s : i for i,s in enumerate(AllStates)}
ttvalues = [[0, 0], [0, 0]]
ttvalues[Index["dirty"]][Index["clean"]] = 1
ttime = transition_matrix(ttvalues, name='TTime')


state = { h: state_function(ttime, name="house"+str(h)) for h in Houses }

for h in Houses:
    for p in Precedences:
        mdl6.add( mdl6.end_before_start(task[h,p[0]], task[h,p[1]]) )

    for s in States:
        mdl6.add( mdl6.always_equal(state[h], task[h,s[0]], Index[s[1]]) )

mdl6.add( workers <= NbWorkers )

mdl6.add(mdl6.minimize( mdl6.max( mdl6.end_of(task[h,"moving"]) for h in Houses )))
