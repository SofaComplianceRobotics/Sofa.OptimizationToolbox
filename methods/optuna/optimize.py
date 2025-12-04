import optuna
import sys
import os
import importlib
import argparse

# Argument parser
parser = argparse.ArgumentParser(description='Optimize an objective function.')
parser.add_argument('objective', metavar='module.py', type=str, nargs=1,
                    help='a python script that should contain an objective function with the following signature: '
                         'def objective(trial). See objective.py in this directory for example')
parser.add_argument('-n', '--nTrials', type=int, nargs='?', help='number of trials (default: 20)', default=20)

args = parser.parse_args()

# Import the objective module
print("Importing objective module from: ", args.objective[0])
module = args.objective[0]
sys.path.append(os.path.dirname(os.path.abspath(module)))
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0]))+"/../..")
o = importlib.import_module(os.path.splitext(os.path.basename(module))[0])

# Create a study for optimization
# You can choose different samplers and pruners here
study = optuna.create_study(
    # Samplers basically continually narrow down the search space using the records of suggested parameter values and
    # evaluated objective values, leading to an optimal search space which giving off parameters leading to better
    # objective values.
    sampler=optuna.samplers.CmaEsSampler(),  # CMA-ES based algorithm
    # sampler=optuna.samplers.TPESampler(),  # Tree-structured Parzen Estimator algorithm
    # sampler=optuna.samplers.GridSampler(),  # Grid Search
    # sampler=optuna.samplers.RandomSampler(),  # Random Search

    # Pruners automatically stop unpromising trials at the early stages of the training
    # (a.k.a., automated early-stopping).
    pruner=optuna.pruners.SuccessiveHalvingPruner()  # Asynchronous Successive Halving algorithm (best performances)
    # pruner= optuna.pruners.HyperbandPruner()  # Hyperband algorithm
    # pruner=optuna.pruners.MedianPruner()  # Median pruning algorithm
    # pruner=optuna.pruners.ThresholdPruner()  # Threshold pruning algorithm
)

# Optimize the objective function
print(o.objective.__doc__)
study.optimize(o.objective, n_trials=args.nTrials)
trial = study.best_trial
print('Best trial with parameters: ', trial.params)

# Visualize the optimization history
fig = optuna.visualization.plot_optimization_history(study)
fig.show()

