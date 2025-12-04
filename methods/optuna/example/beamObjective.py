import optuna
import params

import Sofa
import SofaRuntime
from sofascene import createScene

def getScore(node):
    # Compute the score as the distance between the current position
    position = node.Beam.getMechanicalState().position.value[-1]
    # The score is the absolute distance in y direction to the target
    score = abs(position[1] - params.target)
    return score

def objective(trial):
    """
    In this example our objective is to find the beam design (only length and radius)
    that will get the extremity of the beam to be as close as possible 
    to a target position when subjected to gravity (along y axis).
    """
    # Suggest values for the design parameters
    params.length = trial.suggest_float('length', 50.0, 200.0)  # Length between 50mm and 200mm
    params.radius = trial.suggest_float('radius', 1.0, 10.0)    # Radius between 1mm and 10mm

    # Create the Sofa simulation scene
    SofaRuntime.importPlugin('Sofa.Component')
    SofaRuntime.importPlugin('Sofa.GUI.Component')
    SofaRuntime.importPlugin('Sofa.GL.Component')
    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    # Run the simulation for a fixed number of steps
    dt = 0.01
    for step in range(1500):
        Sofa.Simulation.animate(root, dt)

        # Report intermediate objective value.
        score = getScore(root)
        trial.report(score, step)

        # Handle pruning based on the intermediate value.
        # if trial.should_prune():
            # raise optuna.TrialPruned()

    return score # Return the final score at the end of the simulation
