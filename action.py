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

"""An action has
a cost
a time to perform it
a structure type needed to perform it
"""



class Action(object):
    """This is a class that represents any user interaction possible"""
    def __init__(self):
        self.mineralcost
        self.delay = 0
        self.returns = None

    def execute(self,simulation):
        pass

class BuildUnitActionFactory(Action):
    def __init__(self, unittype):
        super(BuildUnitActionFactory, self).__init__()
        units = json.load(open("./units.json", "r"))
        self.cost = (units[unittype]["minerals"], units[unittype]["vespene"])
        self.delay = units[unittype]["buildtime"]

class UpgradeActionFactory(Action):

if __name__ == '__main__':
    foo = BuildUnitFactory("Zealot")