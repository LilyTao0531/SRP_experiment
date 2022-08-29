from Experiment import Experiment
import os


# Create an Experiment Object with result path
path = os.getcwd()
a = Experiment(path) 
# a = Experiment("/home/tan/srp_experiment/") 



# a.compare_re([5, 10, 20], ["cp", "m3"], time_lim = 600, time_increment = 0.01)
# a.generate_instances([5], 20)

a.check_feasibility([10], ['cp'], 1)

# a.compare_re([2000], ['cp', 'm3'], time_lim = 60, time_increment = 0.01)

