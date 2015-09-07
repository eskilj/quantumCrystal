#!/usr/bin/env python

import yaml
from yaml import CLoader as Loader
import numpy as np
from phonopy import BulkModulus

volumes = []
energies = []
for line in open("e-v.dat"):
    v, e = line.split()
    volumes.append(float(v))
    energies.append(float(e))


blk = BulkModulus(volumes,
                         energies)

print blk.get_parameters()

blk.plot()
