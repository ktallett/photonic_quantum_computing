"""
Quantum Teleportation tutorial from Strawberry Field's website
"""


# Import libraries 

import strawberryfields as sf
from strawberryfields.ops import *

import numpy as np
from numpy import pi, sqrt

from matplotlib import pyplot as plt

# Set the random seed starting position

np.random.seed(42)

# Starts a quantum circuit with 3 modes
prog = sf.Program(3)

# Set a complex number

alpha = 1 + 0.5j

# Work out r and phi using alpha
r = np.abs(alpha)
phi = np.angle(alpha)

# 
with prog.context as q:
    # Prepare initial states

    Coherent(r, phi) | q[0]
    Squeezed(-2) | q[1]
    Squeezed(2) | q[2]

    # Apply gates
    BS = BSgate(pi/4, pi)
    BS | (q[1], q[2])
    BS | (q[0], q[1])

    # Perform homodyne measurements
    MeasureX | q[0]
    MeasureP | q[1]

    # Displacement gates conditioned on the measurements
    Xgate(sqrt(2) * q[0].par) | q[2]
    Zgate(-sqrt(2) * q[1].par) | q[2]

    eng = sf.Engine('fock', backend_options={"cutoff_dim": 15})

    result = eng.run(prog, shots = 1, modes=None, compile_options = {})

    print(result.samples)

    print(result.state)

    state = result.state

    print(state.dm().shape)

    rho2 = np.einsum('kkllij->ij', state.dm())
    print(rho2.shape)

    probs = np.real_if_close(np.diagonal(rho2))
    print(probs)

    plt.bar(range(7), probs[:7])
    plt.xlabel('Fock state')
    plt.ylabel('Marginal probability')
    plt.title('Mode 2')
    plt.show()

    fock_probs = state.all_fock_probs()
    fock_probs.shape
    np.sum(fock_probs, axis=(0, 1))
    
