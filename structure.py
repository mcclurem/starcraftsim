#!/usr/bin/env python
# encoding: utf-8
"""
structure.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
from commondefs import *

import json
from action import *
from scresource import *

#This is mostly polymorphism for the sake of documentation
#Every structure has
#a queue
#
structdata = json.load(open("./structures.json", "r"))
GASTYPE = "Assimilator"

class Structure(object):
    def __init__(self, simulation, structtype):
        self.type = structtype
        self.simulation = simulation
        self.activeunits = []
        self.clearStatus()
        self.stack = []
        self.status[simulation.curstep:simulation.curstep + int(self.BuildTime // simulation.tstep)] = int(self.BuildTime // simulation.tstep) * ["Building"]
        #self.status[0:len(self.simulation.time)-1] = None
    
    def __getattr__(self, name):
            try:
                return super(Structure, self).__getattr__(self, name)
            except:
                try:
                    return structdata[self.type][name]
                except:
                    raise AttributeError("No such var")
    
    def clearStatus(self):
        self.status = len(self.simulation) * [None]
        self.qstatvect = len(self.simulation) * [None]
        
    def currentstat(self):
        return self.status[self.simulation.curstep]
    
    def queueLength(self):
        return len(self.stack)
        
    def queueAction(self,action):
        """Appends action to the queue - equivalent to pressing the button"""
        self.stack.append(action)
        
        
    def step(self, curstep):
        """Generalized algorithm:
                we need a queue.
                if our previous status was x, new status = x if previous state's action is still going.
                Our stack of functions must conform to the guideline that they have a return value
                that indicates: keeptrying or goontothenextfunction
                """
        """Build unittype; Upgrade upgradename"""
        if self.type == GASTYPE:
            if not hasattr(self, "gasnode"):
                self.gasnode = GasNode(self.simulation)
                self.simulation.resourcenodes.append(self.gasnode)
        if self.stack:
            try:
                self.stack[0].execute()
                self.stack.pop(0)
            except InProgressError as e:
                print e.args[0]
                self.status[curstep] = e.args[0]
        self.qstatvect[curstep] = self.queueLength()
        

class Gateway(Structure):
    def __init__(self,simulation):
        super(Gateway, self).__init__( simulation, "Gateway")
        
        
        
class Nexus(Structure):
    def __init__(self, simulation):
        super(Nexus, self).__init__(simulation, "Nexus")
        #self.stack.append(BuildUnitAction("Probe"))
        
        
    def receive(self, resource, quant):
        if resource == "Mineral":
            self.simulation.minerals += quant
        elif resource == "Vespene":
            self.simulation.minerals += quant
        else:
            raise ValueError("Invalid resource type")
    

if __name__ == '__main__':
    unittest.main()