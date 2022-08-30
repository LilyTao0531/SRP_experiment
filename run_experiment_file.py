from Experiment import Experiment

# Create an Experiment Object with result path
a = Experiment("/home/lily/srp_experiment/") 



# a.compare_re([5, 10, 20], ["cp", "m3"], time_lim = 600, time_increment = 0.01)
# a.generate_instances([5], 20)

a.check_feasibility([5], ['cp'], 10)


# a.compare_re([2000], ['cp', 'm3'], time_lim = 60, time_increment = 0.01)

