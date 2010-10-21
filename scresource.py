#!/usr/bin/env python
# encoding: utf-8
"""
resource.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest

class Resource(object):
    def __init__(self, typ, quant):
        self.type = typ
        self.quant = quant
    
class ResourceNode(object):
    def __init__(self, simulation):
        self.simulation = simulation
        self.remaining = 0
        self.returned = 0
        self.occupant = [None] * len(self.simulation.time)
        self.workers = []
        self.timeToCollect = 1
        self.stepsToCollect = int(self.timeToCollect // simulation.tstep)
    
    def _attachWorker(self, worker):
        if worker in self.workers:
            return
        else:
            self.workers.append(worker)
    
    def _removeWorker(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
    
    def workercount(self):
        return len(self.workers)
    
    def requestpickup(self, worker):
        sim = self.simulation
        if self.remaining == 0:
            return "Empty"
        if self.occupant[sim.curstep] is None:
            if self.occupant[sim.curstep - 1] is worker:
                retval = min(self.remaining, self.returned)
                self.remaining -= retval
                return Resource(self.nodeType,self.returned)
            else:
                self.occupant[sim.curstep:sim.curstep + self.stepsToCollect] = [worker] * (self.stepsToCollect)
                return "Wait"
        if self.occupant[self.simulation.curstep] is worker:
            return "Wait"
        else:
            return "Busy"
    
class MineralNode(ResourceNode):
    def __init__(self, simulation):
        super(MineralNode, self).__init__(simulation)
        self.remaining = 1500 #todo: check this number
        self.returned = 5
        self.nodeType = "Mineral"

class RichNode(ResourceNode):
    def __init__(self,simulation):
        super(RichNode, self).__init__(simulation)
        self.remaining = 1500 #todo: check this number
        self.returned = 7
        self.nodeType = "Mineral"   

class GasNode(ResourceNode):
    def __init__(self, simulation):
        super(GasNode, self).__init__(simulation)
        self.remaining = 1500 #todo: check this number
        self.returned = 5
        self.nodeType = "Vespene"


if __name__ == '__main__':
    unittest.main()