"""
Blackbird programming language essentials

Blackbird is a quantum assembly language focusing on continous variable
quantum computers.

State preparations, gate applications, measurements, and subsystems
are the key Operations. 
"""

# Import Libaries

import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *

prog = sf.Program(3)

# Applying state preparations

with prog.context as q:

    # State preparation

    # Single photo state in qumode 0
    Fock(1) | q[0]

    # Coherent state with alpha being 0.5 + 2i in qumode 1
    Coherent(0.5, 2) | q[1]

# Applying gates

with prog.context as q:

    # Apply the displacement in phase state gate to qumode 0
    alpha = 2.0 + 1j
    Dgate(np.abs(alpha), np.angle(alpha)) | q[0]

    # Apply the rotation gate

    phi = 3.14/2
    Rgate(phi) | q[0]

    # Apply the squeezing phase space gate

    Sgate(2.0, 0.17) |q[0]

    # Apply the Beamsplitter gate to qumodes 0 and 1
    BSgate(3.14/10, 0.223) | (q[0], q[1])

    # Apply the cubic phase gate (Vgate) to qumode 0
    gamma = 0.1
    Vgate(gamma) | q[0]

    # Applying the Hermitian conjugate of a gate operator

    with prog.context as q:
        V = Vgate(gamma)
        V.H | q[0]
    

# Measurments

with prog.context as q:
    # Homodyne measurement at angle phi
    phi = 0.25 * 3.14
    MeasureHomodyne(phi) | q[0]

    # Special homodyne measurements
    MeasureX | q[0]
    MeasureP | q[1]

    # Heterodyne measurement
    MeasureHeterodyne() | q[0]
    MeasureHD | q[1]

    # Number state measurements of various qumodes
    MeasureFock() | q[0]
    MeasureFock() | (q[1], q[2])