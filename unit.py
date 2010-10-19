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
from simulation import InProgressError

units = json.load(open("./units.json", "r"))
#Variable for race compatibility
WORKERTYPE = "Probe"


class Unit(object):
    def __init__(self, simulation, unittype):
        self.simulation = simulation
        self.type = unittype
        #self.mineralcost = units[unittype]["MineralCost"]
        #self.vespenecost = units[unittype]["VespeneCost"]
        #self.supplyCost = units[unittype]["Supply"]
        #self.buildtime = units[unittype]["BuildTime"]
        self.clearStatus()
        self.status[simulation.curstep:simulation.curstep + int(self.BuildTime // simulation.tstep)] = int(self.BuildTime // simulation.tstep) * ["Building"]
        if simulation.freeSupply < self.SupplyCost:
            raise InProgressError("MOAR FOOOD")
        else:
            simulation.supplyused += self.SupplyCost
    
    def __del__(self):
        self.simulation.supplyused -= self.SupplyCost
        
    def __getattr__(self, name):
        try:
            return super(Unit, self).__getattr__(self, name)
        except:
            return units[self.type][name]
        
    #Default case, I don't need to do anything
    def step(self, curstep):
        pass
    
    def currentstat(self):
        return self.status[self.simulation.curstep]
    
    def clearStatus(self):
        self.status = [None] * len(self.simulation)
        
class Worker(Unit):
    def __init__(self, simulation):
        super(Worker, self).__init__(simulation, WORKERTYPE)
        #walktime = units["Probe"]["WalkTime"]
        #walktime = 1 #time to go from nexus to resource
        self.walksteps = int(self.WalkTime // simulation.tstep)
        self.node = None
        self.carrying = None
        self.buildinprogress = []
    
    def setnode(self,node):
        if self.node is not None:
            self.node._removeWorker(self)
        self.node = node
        node._attachWorker(self)
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
    
    def build(self, struct):
        self.buildinprogress.append(struct)

    def returnresource(self):
        curstep = self.simulation.curstep
        if self.carrying is not None:
            self.status[curstep:curstep + self.walksteps] = ["Returning"] * self.walksteps

    def step(self, curstep):
        """step is called on every iteration"""
        for struct in self.buildinprogress:
            if struct.currentstat() is None:
                self.simulation.structures.append(struct)
                self.buildinprogress.remove(struct)
                
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
            if self.carrying.type == "Mineral":
                self.simulation.minerals += self.carrying.quant
            else:
                self.simulation.vespene += self.carrying.quant
            
            self.carrying = None
    
   