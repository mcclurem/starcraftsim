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

class Unit(object):
    def __init__(self, simulation, unittype):
        self.simulation = simulation
        self.type = unittype
        self.mineralcost = units[unittype]["Minerals"]
        self.vespenecost = units[unittype]["Vespene"]
        self.supplycost = units[unittype]["Supply"]
        self.buildtime = units[unittype]["BuildTime"]
        self.status = [None] * len(self.simulation.time)
        
        self.status[simulation.curstep:simulation.curstep + self.buildtime // simulation.tstep] = (self.buildtime // simulation.tstep) * ["Building"]
    #Default case, I don't need to do anything
    def step(self, curstep):
        pass
        
class Worker(Unit):
    def __init__(self, simulation):
        super(Worker, self).__init__(simulation, "Probe")
        walktime = units["Probe"]["WalkTime"]
        #walktime = 1 #time to go from nexus to resource
        self.walksteps = walktime // simulation.tstep
        self.node = None
        self.carrying = None
    
    def setnode(self,node):
        if self.node is not None:
            self.node.removeWorker(self)
        self.node = node
        node.attachWorker(self)
        self.walk()
    
    def walk(self):
        curstep = self.simulation.curstep
        self.status[curstep:curstep + self.walksteps] = ["Walking"] * self.walksteps
        
    def trygather(self):
        if self.node is not None:
            curstep = self.simulation.curstep
            ret = self.node.requestpickup(self)
            print ret
            if ret == "Busy":
                self.status[curstep] = "Waiting"
            elif ret == "Wait":
                self.status[curstep] = "Gathering"
            elif ret == "Empty":
                #TODO: Do something here to re-assign probe
                pass
            else:
                self.status[curstep] = "Returning"
                self.carrying = ret
                self.returnresource()
        else:
            print "nonode"
            return


    def returnresource(self):
        curstep = self.simulation.curstep
        if self.carrying is not None:
            self.status[curstep:curstep + self.walksteps] = ["Returning"] * self.walksteps

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
    
   