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


class simulation:
    def __init__(self, filepath):
        self.tstep = 1
        self.time = range(0, simlength, tstep)
        self.curstep = 0
        self.resources = {"Minerals":0, "Vespene":0}
        self.structures = [Nexus()]
        self.units=[Worker(), Worker(), Worker()]
        self.inprogress = []
        self.actionstack = []
        self.loadsim(filepath)
        pass
    
    def loadsim(filepath):
        file = open(filepath, 'r')
        for line in self.readline():
            if line[0:]
            self.actionstack.append(line)
    
    def run():
        for self.curstep in range(0,len(self.time)):
            self.executeStack()
            for struct in self.structures:
                struct.step()
            for unit in self.units():
                unit.step()
            
    def executeStack(self, max):
        """Trys to execute one element off the stack"""
        try:
            self.actionstack[0].execute()
        except:
            return False
        self.actionstack.pop(0)
        
        
        
        
    
    def createunit(self):
        if 


class simulationTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()