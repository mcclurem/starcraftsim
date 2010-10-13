#!/usr/bin/env python
# encoding: utf-8
"""
simulation.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
from action import *
from structure import *
from unit import *
from scresource import *


class simulation(object):
    def __init__(self, filepath, simlength):
        self.tstep = 1
        self.time = range(0, simlength, self.tstep)
        self.curstep = 0
        self.resources = {"Mineral":0, "Vespene":0}
        self.structures = [Nexus(self)]
        self.units=[Worker(self), Worker(self), Worker(self), Worker(self), Worker(self)]
        for aunit in self.units:
            aunit.status = [None for a in aunit.status]
        self.inprogress = []
        self.actionstack = []
        self.loadsim(filepath)
    
    def loadsim(self, filepath):
        file = open(filepath, 'r')
        for line in file.readlines():
            self.actionstack.append(makeAction(line))
    
    def run(self):
        for self.curstep in range(0,len(self.time)):
            self.executeStack(1)
            #for struct in self.structures:
            #    struct.step(self.curstep)
            print self.curstep
            for unit in self.units:
                unit.step(self.curstep)
            
    def executeStack(self, max):
        """Trys to execute one element off the stack"""
        try:
            self.actionstack[0].execute()
        except:
            return False
        self.actionstack.pop(0)
    

class simulationTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    foo = simulation('buildorder', 100)
    bar = MineralNode(foo)
    foo.units[0].setnode(bar)
        
#    unittest.main()