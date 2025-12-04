# Sofa.OptimizationToolbox

The Sofa.OptimizationToolbox is a collection of tools used to perform design optimization based on simulation with SOFA.

## Requirements to launch the simulation

SOFA with SofaPython3 and BeamAdapter plugins installed.

## Methods

- __BruteForce__: Use the `sofa-launcher` tool to perform brute-force optimization by exploring a defined parameter space.
- __Optuna__: Automated hyperparameter optimization framework that allows users to define and optimize objective functions using various algorithms. Define your objective function with SOFA simulations and run the optimization process.

## Example

In this repository, you can find an example of design optimization. 
The objective is to find the dimensions of a cantilever beam that result in a tip position 
as close as possible to a target position, while the beam is subject to gravity.
The mass density and Young's modulus of the beam material are fixed.
Only the `length` and the `radius` of the beam are optimized.

<div style="display: flex; justify-content: space-around;">
<img src="./images/beam.png" alt="Cantilever Beam" width="45%"/>
<img src="./images/beam_solution.png" alt="Cantilever Beam" width="45%"/>
</div>

__Cantilever beam before (left) and after (right) optimization__

In the file `sofascene.py`, you will find the definition of the SOFA scene that simulates the cantilever beam under gravity.
In the file `params.py` you will find the definition of the parameters to optimize, and the definition of the target.

You can run the simulation with the default parameters using the command:
```bash
$ runSofa -l SofaPython3 sofascene.py
```

To try each method of optimization, follow the instructions in the respective folders.

