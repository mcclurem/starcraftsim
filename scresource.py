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
    def __init__(self, simulation):
        self.simulation = simulation
        self.remaining = 0
        self.returned = 5 # quantity received per collection
        self.occupant = [None] * len(self.simulation.time)
        self.workers = []
        self.timeToCollect = 3
    
    def attachWorker(self, worker):
        if worker in self.workers:
            return
        else:
            self.workers.append(worker)
    
    def removeWorker(self, worker):
        if worker in self.workers:
            self.workers.remove(self.workers.index(worker))
    
    def workercount(self):
        return len(self.workers)
    
    def requestpickup(self, worker):
        if self.remaining == 0:
            return "Empty"
        if self.occupant[self.simulation.curstep] is None:
            self.occupant[self.simulation.curstep:self.simulation.curstep + self.timeToCollect // self.simulation.tstep] = [worker] * (self.timeToCollect // self.simulation.tstep)
            return "Wait"
        if self.occupant[self.simulation.curstep] is worker:
            if self.occupant[self.simulation.curstep + 1] is not worker:
                retval = min(self.remaining, self.returned)
                self.remaining -= retval
                return (self.nodeType, retval)
            else:
                return "Wait"
        return "Busy"
        

class MineralNode(Resource):
    def __init__(self, simulation):
        super(MineralNode, self).__init__(simulation)
        self.remaining = 1500 #todo: check this number
        self.nodeType = "Mineral"

class RichNode(Resource):
    def __init__(self):
        super(MineralNode, self).__init__(self)
        self.remaining = 1500 #todo: check this number
        self.nodeType = "Mineral"   
    
        


if __name__ == '__main__':
    unittest.main()