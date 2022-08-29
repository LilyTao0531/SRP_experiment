import sys
from docplex.cp.model import *

mdl0 = CpoModel()

masonry = mdl0.interval_var(size=35)
carpentry = mdl0.interval_var(size=15)
plumbing = mdl0.interval_var(size=40)
ceiling = mdl0.interval_var(size=15)
roofing = mdl0.interval_var(size=5)
painting = mdl0.interval_var(size=10)
windows = mdl0.interval_var(size=5)
facade = mdl0.interval_var(size=10)
garden = mdl0.interval_var(size=5)
moving = mdl0.interval_var(size=5)

mdl0.add( mdl0.end_before_start(masonry, carpentry) )
mdl0.add( mdl0.end_before_start(masonry, plumbing) )
mdl0.add( mdl0.end_before_start(masonry, ceiling) )
mdl0.add( mdl0.end_before_start(carpentry, roofing) )
mdl0.add( mdl0.end_before_start(ceiling, painting) )
mdl0.add( mdl0.end_before_start(roofing, windows) )
mdl0.add( mdl0.end_before_start(roofing, facade) )
mdl0.add( mdl0.end_before_start(plumbing, facade) )
mdl0.add( mdl0.end_before_start(roofing, garden) )
mdl0.add( mdl0.end_before_start(plumbing, garden) )
mdl0.add( mdl0.end_before_start(windows, moving) )
mdl0.add( mdl0.end_before_start(facade, moving) )
mdl0.add( mdl0.end_before_start(garden, moving) )
mdl0.add( mdl0.end_before_start(painting, moving) )

print("\nSolving model....")
msol0 = mdl0.solve(TimeLimit=10)
print("done")

if msol0:
    var_sol = msol0.get_var_solution(masonry)
    print("Masonry : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(carpentry)
    print("Carpentry : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(plumbing)
    print("Plumbing : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(ceiling)
    print("Ceiling : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(roofing)
    print("Roofing : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(painting)
    print("Painting : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(windows)
    print("Windows : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(facade)
    print("Facade : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
    var_sol = msol0.get_var_solution(moving)
    print("Moving : {}..{}".format(var_sol.get_start(), var_sol.get_end()))
else:
    print("No solution found")

import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
# %matplotlib inline
#Change the plot size
from pylab import rcParams
rcParams['figure.figsize'] = 15, 3

if msol0:
    wt = msol0.get_var_solution(masonry)   
    visu.interval(wt, 'lightblue', 'masonry')   
    wt = msol0.get_var_solution(carpentry)   
    visu.interval(wt, 'lightblue', 'carpentry')
    wt = msol0.get_var_solution(plumbing)   
    visu.interval(wt, 'lightblue', 'plumbing')
    wt = msol0.get_var_solution(ceiling)   
    visu.interval(wt, 'lightblue', 'ceiling')
    wt = msol0.get_var_solution(roofing)   
    visu.interval(wt, 'lightblue', 'roofing')
    wt = msol0.get_var_solution(painting)   
    visu.interval(wt, 'lightblue', 'painting')
    wt = msol0.get_var_solution(windows)   
    visu.interval(wt, 'lightblue', 'windows')
    wt = msol0.get_var_solution(facade)   
    visu.interval(wt, 'lightblue', 'facade')
    wt = msol0.get_var_solution(moving)   
    visu.interval(wt, 'lightblue', 'moving')
    visu.show()