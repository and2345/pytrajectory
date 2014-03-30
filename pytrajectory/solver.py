import numpy as np
from numpy.linalg import solve, norm
import scipy as scp

import log
#from log import IPS
from IPython import embed as IPS
from time import time


class Solver:
    '''
    This class provides solver for the collocation equation system.
    
    :param callable F: The callable function that represents the equation system
    :param callable DF: The function for the jacobian matrix of the eqs
    :param ndarray x0: The start value for the sover
    :param real tol: The (absolute) tolerance of the solver
    :param int maxx: The maximum number of iterations of the solver
    :param str algo: The solver to use
    '''
    def __init__(self, F, DF, x0, tol=1e-2, maxx=10, algo='leven'):
        self.F = F
        self.DF = DF
        self.x0 = x0
        self.tol = tol
        self.reltol = tol #1e-3
        self.maxx = maxx
        self.algo = algo
        
        self.sol = None
    

    def solve(self):
        '''
        This is just a wrapper to call the chosen algorithm for solving the
        equation system
        '''
        if (self.algo == 'newton'):
            log.info( "Run Newton solver")
            log.warn(" ... not implemented")
            #self.newton()
            return self.x0
        elif (self.algo == 'gauss'):
            log.info( "Run Gauss solver")
            log.warn(" ... not implemented")
            #self.gauss()
            return self.x0
        elif (self.algo == 'leven'):
            log.info( "Run Levenberg-Marquardt method")
            self.leven()

        if (self.sol == None):
            log.warn("Wrong solver")
            return self.x0
        else:
            return self.sol


    def leven(self):
        '''
        This method is an implementation of the Levenberg-Marquardt-Method
        to approximatively solve a system of non-linear equations by minimizing \n
        :math:`\| F'(x_k)(x_{k+1} - x_k) + F(x_k) \|_2^2 + \\mu^2 \|x_{k+1} - x_k \|`
        '''
        i = 0
        x = self.x0
        res = 1
        res_alt = 1e10
        
        eye = np.eye(len(self.x0))

        mu = 0.1

        # borders for convergence-control ##!! Ref zu Doku
        b0 = 0.2
        b1 = 0.8

        roh = 0.0

        ##?? warum Bed. 1 und 3? (--> retol und abstol)
        while((res > self.tol) and (self.maxx > i) and (abs(res-res_alt) > self.reltol)):
            i += 1
            
            Fx = self.F(x)
            DFx = self.DF(x)
            
            # SPARSE
            DFx = scp.sparse.csr_matrix(DFx)
            
            while (roh < b0):
                ##?? warum J.T*F? (Gleichung (4.18) sagt: J*F)
                ## -> .T gehoert eigentlich oben hin
                
                A = DFx.T.dot(DFx) + mu**2*eye
                b = DFx.T.dot(Fx)
                
                s = -solve(A, b)

                xs = x + np.array(s).flatten()
                
                Fxs = self.F(xs)

                normFx = norm(Fx)
                normFxs = norm(Fxs)

                roh = (normFx**2 - normFxs**2) / (normFx**2 - (norm(Fx+DFx.dot(s)))**2)
                
                if (roh<=b0): mu = 2.0*mu
                if (roh>=b1): mu = 0.5*mu
                #log.info("  roh= %f    mu= %f"%(roh,mu))

            roh = 0.0
            x = x + np.array(s).flatten()
            res_alt = res
            res = normFx
            log.info("nIt= %d    res= %f"%(i,res))

        self.sol = x