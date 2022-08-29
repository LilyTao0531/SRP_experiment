NbWorkers = 3
NbHouses  = 5

TaskNames = {"masonry","carpentry","plumbing",
             "ceiling","roofing","painting",
             "windows","facade","garden","moving"}

Duration =  [35, 15, 40, 15, 5, 10, 5, 10, 5, 5]

ReleaseDate = [31, 0, 90, 120, 90]

Precedences = [("masonry", "carpentry"), ("masonry", "plumbing"), ("masonry", "ceiling"),
               ("carpentry", "roofing"), ("ceiling", "painting"), ("roofing", "windows"),
               ("roofing", "facade"), ("plumbing", "facade"), ("roofing", "garden"),
               ("plumbing", "garden"), ("windows", "moving"), ("facade", "moving"),
               ("garden", "moving"), ("painting", "moving")]

Houses = range(NbHouses)

import sys
from docplex.cp.model import *

mdl4 = CpoModel()

itvs = {}
for h in Houses:
    for i, t in enumerate(TaskNames):
        itvs[h,t] = mdl4.interval_var(start = [ReleaseDate[h], INTERVAL_MAX], size=Duration[i])

# Two cumulative functions: workers, cash balance.
## Workers
workers_usage = step_at(0, 0)
for h in Houses:
    for t in TaskNames:
        workers_usage += mdl4.pulse(itvs[h,t], 1)
## Cash
cash = step_at(0, 0)
for p in Houses:
    cash += mdl4.step_at(60*p, 30000)

for h in Houses:
    for i,t in enumerate(TaskNames):
        cash -= mdl4.step_at_start(itvs[h,t], 200*Duration[i])

for h in Houses:
    for p in Precedences:
        mdl4.add(mdl4.end_before_start(itvs[h, p[0]], itvs[h, p[1]]))

mdl4.add(workers_usage <= NbWorkers)
mdl4.add(cash>=0)

mdl4.add(
    mdl4.minimize(
        mdl4.max(mdl4.end_of(itvs[h,"moving"]) for h in Houses)
    )
)

print("\nSolving model....")
msol4 = mdl4.solve(FailLimit=30000)
print("done")

if msol4:
    print("Cost will be " + str( msol4.get_objective_values()[0] ))

    import docplex.cp.utils_visu as visu
    import matplotlib.pyplot as plt
    # %matplotlib inline
    #Change the plot size
    from pylab import rcParams
    rcParams['figure.figsize'] = 15, 3

    workersF = CpoStepFunction()
    cashF = CpoStepFunction()
    for p in range(5):
        cashF.add_value(60 * p, INT_MAX, 30000)
    for h in Houses:
        for i,t in enumerate(TaskNames):
            itv = msol4.get_var_solution(itvs[h,t])
            workersF.add_value(itv.get_start(), itv.get_end(), 1)
            cashF.add_value(itv.start, INT_MAX, -200 * Duration[i])

    visu.timeline('Solution SchedCumul')
    visu.panel(name="Schedule")
    for h in Houses:
        for i,t in enumerate(TaskNames):
            visu.interval(msol4.get_var_solution(itvs[h,t]), h, t)
    visu.panel(name="Workers")
    visu.function(segments=workersF, style='area')
    visu.panel(name="Cash")
    visu.function(segments=cashF, style='area', color='gold')
    visu.show()
else:
    print("No solution found")