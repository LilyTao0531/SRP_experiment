from asyncio import Task
import sys
from docplex.cp.model import *

mdl3 = CpoModel()

NbHouses = 5;

WorkerNames = ["Joe", "Jim" ]

TaskNames = ["masonry","carpentry","plumbing","ceiling","roofing","painting","windows","facade","garden","moving"]

Duration =  [35,15,40,15,5,10,5,10,5,5]

Worker = {"masonry":"Joe","carpentry":"Joe","plumbing":"Jim","ceiling":"Jim",
          "roofing":"Joe","painting":"Jim","windows":"Jim","facade":"Joe",
          "garden":"Joe","moving":"Jim"}


Precedences = { ("masonry","carpentry"),("masonry","plumbing"),
               ("masonry","ceiling"),("carpentry","roofing"),
               ("ceiling","painting"),("roofing","windows"),
               ("roofing","facade"),("plumbing","facade"),
               ("roofing","garden"),("plumbing","garden"),
               ("windows","moving"),("facade","moving"),  
               ("garden","moving"),("painting","moving") }

Houses = range(NbHouses)

Breaks ={
  "Joe" : [
     (5,14),(19,21),(26,28),(33,35),(40,42),(47,49),(54,56),(61,63),
     (68,70),(75,77),(82,84),(89,91),(96,98),(103,105),(110,112),(117,119),
     (124,133),(138,140),(145,147),(152,154),(159,161),(166,168),(173,175),
     (180,182),(187,189),(194,196),(201,203),(208,210),(215,238),(243,245),(250,252),
     (257,259),(264,266),(271,273),(278,280),(285,287),(292,294),(299,301),
     (306,308),(313,315),(320,322),(327,329),(334,336),(341,343),(348,350),
     (355,357),(362,364),(369,378),(383,385),(390,392),(397,399),(404,406),(411,413),
     (418,420),(425,427),(432,434),(439,441),(446,448),(453,455),(460,462),(467,469),
     (474,476),(481,483),(488,490),(495,504),(509,511),(516,518),(523,525),(530,532),
     (537,539),(544,546),(551,553),(558,560),(565,567),(572,574),(579,602),(607,609),
     (614,616),(621,623),(628,630),(635,637),(642,644),(649,651),(656,658),(663,665),
     (670,672),(677,679),(684,686),(691,693),(698,700),(705,707),(712,714),
     (719,721),(726,728)
  ],
  "Jim" : [
     (5,7),(12,14),(19,21),(26,42),(47,49),(54,56),(61,63),(68,70),(75,77),
     (82,84),(89,91),(96,98),(103,105),(110,112),(117,119),(124,126),(131,133),
     (138,140),(145,147),(152,154),(159,161),(166,168),(173,175),(180,182),(187,189),
     (194,196),(201,225),(229,231),(236,238),(243,245),(250,252),(257,259),
     (264,266),(271,273),(278,280),(285,287),(292,294),(299,301),(306,315),
     (320,322),(327,329),(334,336),(341,343),(348,350),(355,357),(362,364),(369,371),
     (376,378),(383,385),(390,392),(397,413),(418,420),(425,427),(432,434),(439,441),
     (446,448),(453,455),(460,462),(467,469),(474,476),(481,483),(488,490),(495,497),
     (502,504),(509,511),(516,518),(523,525),(530,532),(537,539),(544,546),
     (551,553),(558,560),(565,581),(586,588),(593,595),(600,602),(607,609),
     (614,616),(621,623),(628,630),(635,637),(642,644),(649,651),(656,658),
     (663,665),(670,672),(677,679),(684,686),(691,693),(698,700),(705,707),
     (712,714),(719,721),(726,728)]
  }

from collections import namedtuple
Break = namedtuple('Break', ['start', 'end'])  

Calendar = {}
mymax = max(max(v for k,v in Breaks[w]) for w in WorkerNames)
for w in WorkerNames:
    step = CpoStepFunction()
    step.set_value(0, mymax, 100)
    for b in Breaks[w]:
        t = Break(*b)
        step.set_value(t.start, t.end, 0)
    Calendar[w] = step


#House interval variables
itvs = {}
for h in Houses:
    for i, t in enumerate(TaskNames):
        _name = str(h) + "_" + str(t)
        itvs[(h,t)] = mdl3.interval_var(size=Duration[i], intensity=Calendar[Worker[t]], name = _name)

#Constraint on the orders of tasks
for h in Houses:
    for p in Precedences:
        mdl3.add(mdl3.end_before_start(itvs[h, p[0]], itvs[h, p[1]]) )

#Constraint to exclude overlapping interval variables
for w in WorkerNames:
    mdl3.add(mdl3.no_overlap([itvs[h,t] for h in Houses for t in TaskNames if Worker[t]==w]))

for h in Houses:
    for t in TaskNames:
        mdl3.add(mdl3.forbid_start(itvs[h,t], Calendar[Worker[t]]))
        mdl3.add(mdl3.forbid_end(itvs[h,t], Calendar[Worker[t]]))

mdl3.add(mdl3.minimize(max(mdl3.end_of(itvs[h,"moving"]) for h in Houses)))

print("\nSolving model....")
msol3 = mdl3.solve(FailLimit=30000)
print("Done")

if msol3:
    print("Cost will be " + str( msol3.get_objective_values()[0] ))    # Allocate tasks to workers
    tasks = {w : [] for w in WorkerNames}
    for k,v in Worker.items():
        tasks[v].append(k)
    types = {t: i for i, t in enumerate(TaskNames)}
    
    import docplex.cp.utils_visu as visu
    import matplotlib.pyplot as plt    
    from pylab import rcParams
    rcParams['figure.figsize'] = 15, 3

    # visu.timeline('Solution SchedCalendar')
    for w in WorkerNames:
        visu.panel()
        visu.pause(Calendar[w])
        visu.sequence(name = w,
                    intervals = [(msol3.get_var_solution(itvs[h,t]), types[t], t) for t in TaskNames if Worker[t]==w for h in Houses  ])
    visu.show()
else:
    print("No solution found")
