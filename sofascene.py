import params
from math import pi

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
    beam.addObject("MeshTopology", position=[[0, 0, 0], [params.length/2, 0, 0], [params.length, 0, 0]], edges=[[0,1], [1,2]])
    beam.addObject("MechanicalObject", template="Rigid3", showObject=True, showObjectScale=5)
    beam.addObject('BeamInterpolation', 
                    crossSectionShape="circular",
                    defaultYoungModulus=1e4,  
                    defaultPoissonRatio=0.45,
                    radius=params.radius)
    beam.addObject('AdaptiveBeamForceFieldAndMass', computeMass=True, massDensity=1e-6)
    beam.addObject("FixedProjectiveConstraint", indices=[0])  # Fix one end of the beam

    visual = beam.addChild("Visual")
    visual.addObject("MeshOBJLoader", name="loader", filename="mesh/cylinder.obj", rotation=[0, 0, -90], scale3d=[params.radius*2, params.length/10, params.radius*2])
    visual.addObject("OglModel", name="VisualModel", src=visual.loader.linkpath, color=[0.8, 0.3, 0.3, 1.0])
    visual.addObject("SkinningMapping")

