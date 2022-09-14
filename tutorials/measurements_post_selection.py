"""
Measurements and Post-Selection

Measurment operators and uses in Strawberry Fields
Quantum transformation operators

#########

Homodyne measurements

MeasureHomodyne(phi=0)

#########

Heterodyne Detection

MeasureHeterodyne()


#########

Photon-counting

- MeasureFock()


"""

# Building a circuit with two Fock states are directed on a beamsplitter
# Two photon detectors at the output

# Import libraries

import numpy as np

import strawberryfields as sf
from strawberryfields.ops import *

np.random.seed(42)

prog = sf.Program(2)
eng = sf.Engine("fock", backend_options={"cutoff_dim": 6})

with prog.context as q:
    Fock(2) | q[0]
    Fock(3) | q[1]
    BSgate() | (q[0], q[1])
    MeasureFock() | q[0]

results = eng.run(prog)

print(results.samples[0][0])

# Second mode

prog2 = sf.Program(2)
with prog2.context as q:
    MeasureFock() | q[1]

results = eng.run(prog2)

print(results.samples[0][0])

# Rewrite above using Post-selection

prog = sf.Program(2)
eng = sf.Engine("fock", backend_options = {"cutoff_dim": 6})

with prog.context as q:
    Fock(2) | q[0]
    Fock(3) | q[1]
    BSgate() | (q[0], q[1])
    MeasureFock(select=0) | q[0]
    MeasureFock() | q[1]

result = eng.run(prog)

print(result.samples)

