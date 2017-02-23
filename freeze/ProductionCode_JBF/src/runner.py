#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""
Copyright (C) 2013 Co-Pierre Georg (co-pierre.georg@keble.ox.ac.uk)
Tarik Roukny Ornia (troukny@ulb.ac.be)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>

The development of this software has been supported by the ERA-Net 
on Complexity through the grant RESINEE.
"""
import logging

from updater import Updater

#-------------------------------------------------------------------------
#
#  class Runner
#
#-------------------------------------------------------------------------
class Runner(object):
    
    #
    # METHODS
    #
    #-------------------------------------------------------------------------
    # __init__(identifier)
    #-------------------------------------------------------------------------
    def __init__(self,  identifier,  environment):
        self.identifier = identifier
        self.environment = environment
    #-------------------------------------------------------------------------
    
    
    #-------------------------------------------------------------------------
    # do_run()
    #-------------------------------------------------------------------------
    def do_run(self):
        updater = Updater(self.identifier,  self.environment)

        for i in range(0, self.environment.parameter.num_sweeps):
            updater.do_update()
