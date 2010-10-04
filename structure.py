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


#This is mostly polymorphism for the sake of documentation
#Every structure has
#a queue
#
class Structure(object):
    def __init__(self, structtype, simulation):
        self.simulation = simulation
        self.actions = {}
        self.queue = []
        self.activeunits = [None]
        self.status[0:len(self.simulation.time)-1] = None
    
    def queueAction(self):
        """Appends action to the queue - equivalent to pressing the button"""
        #if weknowhow and wehavethemoney
        #eat the money
        
    def build(self, unittype):
        """If we are allowed to build this, start build cycle"""
        if we know how
        #eat the supply
        unit = Unit(unittype)
        if self.activeunits == [None]:
    
    def finish(self, unittype):
        '''if this object def '''
    
    def step(self, curstep):
        """Generalized algorithm:
                we need a queue.
                if our previous status was x, new status = x if previous state's action is still going.
                Our stack of functions must conform to the guideline that they have a return value
                that indicates: keeptrying or goontothenextfunction
                """
                
                """Build unittype
                Upgrade upgradename"""
        action, args = self.stack[0]
        

class Gateway(Structure):
    def __init__(self,simulation):
        super(Gateway, self).__init__(self, simulation)
        
        
        
class Nexus(Structure):
    def __init__(self, simulation):
        super(Nexus, self).__init__(self, simulation)
        #TODO:this needs real actions
        self.actions["BuildWorker":None]
        
    def perform(self, action):
        self.actions[action].perform(self.simulation)
        
    def recieve(self, resource, quant):
        self.simulation.resources[resource] += quant

class Gateway(Structure):
    


if __name__ == '__main__':
    unittest.main()