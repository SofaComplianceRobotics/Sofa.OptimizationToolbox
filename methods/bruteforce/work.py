import sys                 
import os
import csv
from launcher import *  


dirpath = os.path.dirname(os.path.abspath(__file__))

# File to launch                 
filenames = ["_sofascene.py"]
filesandtemplates = []
for filename in filenames:                
    filesandtemplates.append( (open(os.path.join(dirpath,filename)).read(), filename) )

# Parameters
listParameters = []
nbIterations = 150

for length_i in range(100, 200, 10):
    for radius_i in range(1, 5):
        parameters = {}
        parameters["length"] = length_i
        parameters["radius"] = radius_i
        parameters["nbIterations"] = nbIterations
        listParameters.append(parameters)

results = startSofa(listParameters, filesandtemplates, launcher=ParallelLauncher(10))

# Process results to find the best design
best_score = float('inf')
best_params = None
for res in results:
    with open(os.path.join(res["directory"],"output.csv"), 'r') as csvfile:
        lines = csvfile.readlines()
        y_position = float(lines[2].strip().split(';')[1])  # y position of the beam tip
        score = abs(y_position + 30.0)  # Assuming target is - 30.0
        if score < best_score:
            best_score = score
            best_params = [float(lines[0].strip().split(';')[1]), 
                           float(lines[1].strip().split(';')[1])]

print("Best design parameters: ", best_params)
print("Best score (distance to target): ", best_score)