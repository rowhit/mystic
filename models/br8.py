#!/usr/bin/env python

"""
References:

[5] Bevington & Robinson (1992). Data Reduction and Error Analysis for the Physical Sciences, Second Edition, McGraw-Hill, Inc., New York.
"""
from poly import AbstractModel

from numpy import array, asarray, sqrt
from numpy import sum as numpysum
from numpy import exp
from mystic.forward_model import CostFactory as CF

class BevingtonDecay(AbstractModel):
    """
Computes dual exponential decay [5].
y = a1 + a2 Exp[-t / a4] + a3 Exp[-t/a5]
    """

    def __init__(self,name='decay',metric=lambda x: numpysum(x*x)):
        AbstractModel.__init__(self,name,metric)
        return

    def evaluate(self,coeffs,evalpts):
        """evaluate dual exponential decay with given coeffs over given evalpts
coeffs = (a1,a2,a3,a4,a5)"""
        a1,a2,a3,a4,a5 = coeffs
        t = asarray(evalpts)
        return a1 + a2*exp(-t/a4) + a3*exp(-t/a5)

    def ForwardFactory(self,coeffs):
        """generates a dual decay model instance from a list of coefficients"""
        a1,a2,a3,a4,a5 = coeffs
        def forward_decay(evalpts):
            """a dual exponential decay over a 1D numpy array
with (a1,a2,a3,a4,a5) = (%s,%s,%s,%s,%s)""" % (a1,a2,a3,a4,a5)
            return self.evaluate((a1,a2,a3,a4,a5),evalpts)
        return forward_decay

    def CostFactory(self,target,pts):
        """generates a cost function instance from lists of coefficients & evaluation points"""
        datapts = self.evaluate(target,pts)
        F = CF()
        F.addModel(self.ForwardFactory,self.__name__,len(target))
        self.__cost__ = F.getCostFunction(evalpts=pts,observations=datapts,sigma=sqrt(datapts),metric=self.__metric__)
        return self.__cost__

    def CostFactory2(self,pts,datapts,nparams):
        """generates a cost function instance from datapoints & evaluation points"""
        F = CF()
        F.addModel(self.ForwardFactory,self.__name__,nparams)
        self.__cost__ = F.getCostFunction(evalpts=pts,observations=datapts,sigma=sqrt(datapts),metric=self.__metric__)
        return self.__cost__

    pass
 

# prepared instances
decay = BevingtonDecay() #FIXME: look up the correct name for the model!

# data from Chapter 8 of [5].
data = array([[15, 775], [30, 479], [45, 380], [60, 302],
[75, 185], [90, 157], [105,137], [120, 119], [135, 110],
[150, 89], [165, 74], [180, 61], [195, 66], [210, 68],
[225, 48], [240, 54], [255, 51], [270, 46], [285, 55],
[300, 29], [315, 28], [330, 37], [345, 49], [360, 26],
[375, 35], [390, 29], [405, 31], [420, 24], [435, 25],
[450, 35], [465, 24], [480, 30], [495, 26], [510, 28],
[525, 21], [540, 18], [555, 20], [570, 27], [585, 17],
[600, 17], [615, 14], [630, 17], [645, 24], [660, 11],
[675, 22], [690, 17], [705, 12], [720, 10], [735, 13],
[750, 16], [765, 9], [780, 9], [795, 14], [810, 21],
[825, 17], [840, 13], [855, 12], [870, 18], [885, 10]])

# cost function with br8.data as the target
cost = decay.CostFactory2(data[:,0],data[:,1],5)


# End of file