import Sofa
import csv
from math import pi


class Monitor(Sofa.Core.Controller):
    """
        Monitor, at each time step of the simulation:
        - The position of the beam tip
    """

    def __init__(self, beam):

        Sofa.Core.Controller.__init__(self)
        self.name = "Monitor"
        self.beam = beam
        self.root = beam.getRoot()

        # Prepare the output data
        self.length = ["length", $length]
        self.radius = ["radius", $radius]
        self.position = ["y_position", 0]

        return

    def onAnimateEndEvent(self, e):
        """
            You can store the data at each time step of the simulation, or just at the end like in this example.
            Save a csv file with the data at the end of the simulation.
            Sofa-launcher will only run a predefined number of iterations. 
        """

        # If last time step, save the data
        if (self.root.time.value >= self.root.dt.value * ($nbIterations - 1)):
            self.position[1] = self.beam.getMechanicalState().position.value[-1][1]  # y position of the beam tip
            self.saveCSVFile()

    def saveCSVFile(self):
        """
            Save the data in a csv file
        """
        with open('output.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow(self.length)
            spamwriter.writerow(self.radius)
            spamwriter.writerow(self.position)


def addSceneHeader(node):

    settings = node.addChild("Settings")
    settings.addObject("RequiredPlugin", name="BeamAdapter")

    node.addObject("DefaultAnimationLoop")
    node.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Projective') # Needed to use components [FixedProjectiveConstraint]  
    node.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Iterative') # Needed to use components [CGLinearSolver]  
    node.addObject('RequiredPlugin', name='Sofa.Component.ODESolver.Backward') # Needed to use components [EulerImplicitSolver]  
    node.addObject('RequiredPlugin', name='Sofa.Component.StateContainer') # Needed to use components [MechanicalObject]  
    node.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Constant') # Needed to use components [MeshTopology]  


def createScene(rootnode):
    # We design a simple beam fixed at one end
    # This scene will be used to evaluate the design parameters (length and radius)
    # The density and Young modulus are fixed in this example

    addSceneHeader(rootnode)

    # Add gravity
    rootnode.gravity = [0, -9810, 0]

    # Create the beam
    beam = rootnode.addChild("Beam")
    beam.addObject("EulerImplicitSolver")
    beam.addObject("SparseLDLSolver", template="CompressedRowSparseMatrixMat3x3d")
    beam.addObject("MeshTopology", position=[[0, 0, 0], [$length/2, 0, 0], [$length, 0, 0]], edges=[[0,1], [1,2]])
    beam.addObject("MechanicalObject", template="Rigid3", showObject=True, showObjectScale=5)
    beam.addObject('BeamInterpolation', 
                    crossSectionShape="circular",
                    defaultYoungModulus=1e4,  
                    defaultPoissonRatio=0.45,
                    radius=$radius)
    beam.addObject('AdaptiveBeamForceFieldAndMass', computeMass=True, massDensity=1e-6)
    beam.addObject("FixedProjectiveConstraint", indices=[0])  # Fix one end of the beam

    visual = beam.addChild("Visual")
    visual.addObject("MeshOBJLoader", name="loader", filename="mesh/cylinder.obj", rotation=[0, 0, -90], scale3d=[$radius*2, $length/10, $radius*2])
    visual.addObject("OglModel", name="VisualModel", src=visual.loader.linkpath, color=[0.8, 0.3, 0.3, 1.0])
    visual.addObject("SkinningMapping")

    # Add the monitor to track the beam tip position
    rootnode.addObject(Monitor(beam))

