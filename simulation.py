#!/usr/bin/env python
# encoding: utf-8
"""
simulation.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
#from __future__ import division
import sys
import os
import unittest

from commondefs import *


from action import *
from structure import *
from unit import *
from scresource import *
from collections import *
import numpy
import pylab
import matplotlib.pyplot as plt



class simulation(object):
    def __init__(self, filepath, simlength):
        self.tstep = 0.5
        self.time = [x*self.tstep for x in range(int(simlength//self.tstep))]
        self.curstep = 0
        self.minerals = 50
        self.vespene = 0
        self.supplyused = 0
        self.mineralvect = [0] * len(self.time)
        self.gasvect = [0] * len(self.time)
        self.supplyvect = [0] * len(self.time)
        self.spendvect = [None] * len(self.time)
        self.structures = [Nexus(self)]
        self.resourcenodes = [MineralNode(self) for i in range(8)]
        self.units=[Worker(self) for i in range(6)]
        for unit in self.units:
            unit.clearStatus()
        for struct in self.structures:
            struct.clearStatus()
        self.inprogress = []
        self.actionstack = []
        self.loadsim(filepath)
    
    def __len__(self):
        return len(self.time)
        
    #TODO: these should all be dynamic
    @property
    def freeSupply(self):
        return self.supplyMax - self.supplyused
    @property
    def supplyMax(self):
        return reduce(lambda x, y: x + y.SupplyValue, self.structures, 0)
    @property
    def workers(self):
        return filter(lambda x: x.type == WORKERTYPE, self.units)
    @property
    def idleworkers(self):
        return filter(lambda x: x.node == None, self.workers)
    @property
    def mineralnodes(self):
        return filter(lambda x: x.nodeType == "Mineral", self.resourcenodes)
    @property
    def gasnodes(self):
        return filter(lambda x: x.nodeType == "Vespene", self.resourcenodes)
    
    def loadsim(self, filepath):
        file = open(filepath, 'r')
        for line in file.readlines():
            self.actionstack.append(makeAction(line.rstrip()))
    
    def run(self):
        for self.curstep in range(0,len(self)):
            self.executeStack(1)
            #Step each structure
            for struct in self.structures:
                struct.step(self.curstep)
            print self.curstep
            #Step each unit
            for unit in self.units:
                unit.step(self.curstep)
            #Assign newunits
            self._workerAssignments()
            self.supplyvect[self.curstep] = self.supplyused
            self.mineralvect[self.curstep] = self.minerals
            self.gasvect[self.curstep] = self.vespene
        self.plotsim()
        
    def plotsim(self):
        pylab.subplot(211)
        pylab.plot(self.time, self.mineralvect, 'b-', self.time, self.gasvect, 'g-')
        for el in self.spendvect:
            if el is not None:
                ind = self.spendvect.index(el)
                pylab.annotate(str(el), (self.time[ind], self.mineralvect[ind]+25), rotation='vertical')
        pylab.xlabel('time')
        pylab.ylabel('money')
        pylab.subplot(212)
        pylab.plot(self.time, self.supplyvect, 'r-', self.time, self.availableStruct("Nexus").qstatvect, 'b-')
        pylab.show()
    
    def _workerAssignments(self):
        """handles dispatching workers under the logic: occupy your vespene, then your minerals"""
        gasnodes = self.gasnodes
        if len(gasnodes) > 0:
            for node in gasnodes:
                if len(node.workers) < 3:
                    self._lamestworker().setnode(node)
        if len(self.idleworkers) > 0:
            #Assign idleworkers to lowest occupancy nodes
            self.idleworkers[0].setnode(sorted(self.mineralnodes,key=lambda x: len(x.workers))[0])
            
        
    def _lamestworker(self):
        try:
            return self.idleworkers[0]
        except IndexError:
            possibles = filter(lambda x: x.node.nodeType == "Mineral", self.workers)
            try:
                return filter(lambda x: x.currentstat() == "Walking" or x.currentstat() == "Waiting", self.workers)[0]
            except IndexError:
                return possibles[0]
    
    #TODO: ValueError seems inaproppriate here
    def spend(self, minerals, vespene):
        if self.minerals < minerals:
            raise ValueError("More Minerals")
        if self.vespene < vespene:
            raise ValueError("Insufficient Vespene Gas")
        self.vespene -= vespene
        self.minerals -= minerals
    
    def executeStack(self, max):
        """Trys to execute one element off the stack"""
        if self.actionstack:
            try:
                self.actionstack[0].assign(self)
            except ValueError as e:
                print e
                return False
            self.spendvect[self.curstep] = self.actionstack[0]
            self.actionstack.pop(0)
    
    def availableStruct(self, structtype):
        """returns the most available structure"""
        #print "Looking for:", structtype
        available = filter(lambda x: x.currentstat() == None, self._allStructures(structtype))
        if len(available) > 0:
            return available[0]
        else:
            raise ValueError("No available buildings")
    
    def _allStructures(self, structtype):
        return filter(lambda x: x.type == structtype, self.structures)
    
    def wehavebuilding(self, build):
        return len(self._allStructures(build)) > 0
    
    def wehave(self, prereqs):
        """Takes in a list of prereqs and validates them"""
        for req in prereqs:
            if req[:9].upper() == 'STRUCTURE':
                return self.wehavebuilding(req[10:])
            else:
                return False
        return True
        

class simulationTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    foo = simulation('buildorder', 60*3)
    foo.run()
    #bar = MineralNode(foo)
    #foo.units[0].setnode(bar)
        
#    unittest.main()
