#!/usr/bin/env python

"""
Sets up De Jong's Fourth function. This is problem 4 of testbed 1 in [1].

This is function fitting "with noise."
Reference:

[1] Storn, R. and Price, K. Differential Evolution - A Simple and Efficient
Heuristic for Global Optimization over Continuous Spaces. Journal of Global
Optimization 11: 341-359, 1997.

[2] Storn, R. and Proce, K. Same title as above, but as a technical report.
try: http://www.icsi.berkeley.edu/~storn/deshort1.ps
"""

from mystic.differential_evolution import DifferentialEvolutionSolver
from mystic.termination import ChangeOverGeneration, VTR
from mystic.strategy import Best1Exp, Rand1Exp
from mystic.models.dejong import quartic as DeJong4

import random
random.seed(123)

ND = 30
NP = 10
MAX_GENERATIONS = 2500

def main():
    solver = DifferentialEvolutionSolver(ND, NP)

    solver.SetRandomInitialPoints(min = [-1.28]*ND, max = [1.28]*ND)

    solver.Solve(DeJong4, Rand1Exp, termination = VTR(15) , \
                 maxiter= MAX_GENERATIONS, CrossProbability=0.3, ScalingFactor=1.0)

    solution = solver.Solution()
  
    print solution



if __name__ == '__main__':
    from timeit import Timer

    # optimize with DESolver
    t = Timer("main()", "from __main__ import main")
    timetaken =  t.timeit(number=1)
    print "CPU Time: %s\n" % timetaken

    # optimize with fmin
    from mystic.scipy_optimize import fmin
    print fmin(DeJong4, [0 for i in range(ND)])

# end of file