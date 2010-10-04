#!/usr/bin/env python
# encoding: utf-8
"""
unit.py

Created by Morgan Mcclure on 2010-10-03.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import json

units = json.load(open("./units.json", "r"))

class Unit:
    def __init__(self, simulation, unittype):
        self.simulation = simulation
        self.type = unittype
        self.mineralcost = units[unittype].mineralcost        
        self.vespenecost = units[unittype].vespenecost
        self.supplycost = units[unittype].supplycost
        self.buildtime = units[unittype].buildtime 
        self.status = [None] * len(self.simulation.time)
        self.status[simulation.curstep:simulation.curstep + creation time] = "Building"
    
    def step(self, curstep):
        '''General step algorithm
        given my current state is none, should I be doing something'''
        
    
        
class Worker(Unit):
    def __init__(self, simulation):
        super(Worker,self).__init__(simulation)
        walktime = 1 #time to go from nexus to resource
        self.cost = (50, 0)
        self.walksteps = walktime // simulation.tstep
        self.node = None
        self.status = [None] * len(self.simulation.time)
        self.carrying = None
    
    def setnode(self,node):
        if self.node is not None:
            
        if self.node is None:
            self.node = 
    
    def walk(self):
        curstep = self.simulation.curstep
        self.status[curstep:curstep + self.walksteps] = "Walking"
        
    def trygather(self):
        if self.node is not None:
            self.simulation.curstep = curstep
            ret = self.node.requestpickup(self)
        if ret == "Busy":
            self.status[curstep] == "Waiting"
        elif ret == "Wait":
            self.status[curstep] == "Gathering"
        elif ret == "Empty":
            #TODO: Do something here to re-assign probe
            pass
        else:
            self.status = "Returning"
            self.carrying = ret
            self.returnresource()


    def returnresource(self):
        if self.carrying is not None:
            self.status[curstep:curstep + self.walksteps] = "Returning"

    def step(self, curstep):
        """step is called on every iteration"""
        #none, walking, waiting, collecting, returning
        prev = None if curstep == 0 else self.status[curstep - 1]
        if self.status[curstep] is None:
            if prev is None:
                return
            elif prev == "Returning":
                self.deposit()
                self.walk()
            elif prev == "Walking":
                self.trygather()
            elif prev == "Gathering" or prev == "Waiting":
                self.trygather()
    
                    
    def deposit(self):
        if self.carrying is not None:
            self.simulation.resources[self.carrying[0]] += self.carrying[1]
            self.carrying = None
    
   