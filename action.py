#!/usr/bin/env python
# encoding: utf-8
"""
action.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import json

from unit import *
from structure import *
"""An action has
a cost
a time to perform it
a structure type needed to perform it
"""
units = json.load(open("./units.json", "r"))
structdata = json.load(open("./structures.json", "r"))

def makeAction(string):
    if string.startswith('Build'):
        string = string[6:]
        print string
        try:
            act = BuildUnitAction(string)
        except:
            act = BuildStructAction(string)
            #raise ValueError("Improperly formatted action string %s" %(string) )
        return act
    else:
        raise ValueError("Invalid action string")

class Action(object):
    """This is a class that represents any user interaction possible"""
    def __init__(self):
        self.mineralcost = 0
        self.vespenecost = 0
        self.delay = 0
        self.returns = None

    def execute(self,simulation):
        pass


class BuildUnitAction(Action):
    def __init__(self, unittype):
        super(BuildUnitAction, self).__init__()
        self.unittype = unittype
        self.MineralCost = units[unittype]["MineralCost"]
        self.VespeneCost = units[unittype]["VespeneCost"]
        self.delay = units[unittype]["BuildTime"]
   
    def __str__(self):
        return "Build %s" % self.unittype

    def assign(self, simulation):
        print "assign"
        self.simulation = simulation
        if simulation.wehave(units[self.unittype]['Requires']):
            self.parentstruct = simulation.availableStruct(units[self.unittype]['BuiltBy'])
            simulation.spend(self.MineralCost, self.VespeneCost)
            self.parentstruct.queueAction(self)
    
    def execute(self):
        """Raises an InProgressError, or appends the unit"""
        sim = self.simulation
        if self.returns is None:
            #intentionally uncaught exception here
            #If not enough supply, constructor throws exception
            if self.unittype == WORKERTYPE:
                self.returns = Worker(sim)
            else:
                self.returns = Unit(sim, self.unittype)
            
        if self.returns.currentstat() is "Building":
            raise InProgressError("Building Unit")
        else:
            sim.units.append(self.returns)

class BuildStructAction(Action):
    def __init__(self, structtype):
        super(BuildStructAction, self).__init__()
        self.structtype = structtype
        self.MineralCost = structdata[structtype]['MineralCost']
        self.VespeneCost = structdata[structtype]["VespeneCost"]
        self.delay = structdata[structtype]["BuildTime"]
   
    def __str__(self):
        return "Build %s" % self.structtype

    def assign(self, simulation):
        self.simulation = simulation
        if simulation.wehave(structdata[self.structtype]['Requires']):
            simulation.spend(self.MineralCost, self.VespeneCost)
            thestruct = Structure(simulation, self.structtype)
            simulation._lamestworker().build(thestruct)
            

if __name__ == '__main__':
    foo = BuildUnitFactory("Zealot")
