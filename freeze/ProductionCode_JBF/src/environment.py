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
import random

from network import Network
from parameter import Parameter




#-------------------------------------------------------------------------
#
#  class Environment
#
#-------------------------------------------------------------------------
class Environment(object):
    
    #
    # METHODS
    #
    def __init__(self,  identifier):
        self.identifier = identifier
        self.network = Network(self.identifier)
        self.parameter = Parameter(self.identifier)
    


    def __str__(self):
        text = "<environment identifier='" + self.identifier + "'>\n"
        text += str(self.network)
        text += str(self.parameter)
        text += "</environment>\n"
        
        return text
    
    
#
# INITIALIZATON FUNCTIONS
#
    #-------------------------------------------------------------------------
    # read_environment_file
    #-------------------------------------------------------------------------
    def read_environment_file(self,  environment_filename):
        logging.info('reading environment file %s',  environment_filename)
        
        from xml.etree import ElementTree
        xmlText = open(environment_filename).read()
        
        element = ElementTree.XML(xmlText)
        self.identifier = element.attrib['title']
        
        self.parameter.identifier = self.identifier
        
        # loop over all entries in the xml file
        for subelement in element:
            # the first set of parameters will be valid for the whole simulation
            if (subelement.attrib['type'] == 'num_sweeps'):
                self.parameter.num_sweeps = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'num_simulations'):
                self.parameter.num_simulations = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'num_agents'):
                self.parameter.num_agents = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'alpha'):
                self.parameter.alpha = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'beta'):
                self.parameter.beta = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'gamma'):
                self.parameter.gamma = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'theta'):
                self.parameter.theta = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal0_mean'):
                self.parameter.signal0_mean = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal0_variance'):
                self.parameter.signal0_variance = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal1_mean'):
                self.parameter.signal1_mean = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal1_variance'):
                self.parameter.signal1_variance = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'p'):
                self.parameter.p = float(subelement.attrib['value'])
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # initialize_environment
    #-------------------------------------------------------------------------
    def initialize(self):
        self.network.initialize(self.parameter.num_agents)
    #-------------------------------------------------------------------------


#
# HELPER FUNCTIONS
#
    #-------------------------------------------------------------------------
    # get_probability_density(s)
    #-------------------------------------------------------------------------
    def get_probability_density(self,  s,  state):
        probability_density=0.0
        
        if state == 0:
            probability_density = random.normalvariate(self.parameter.signal0_mean,  self.parameter.signal0_variance)
        else:
            probability_density = random.normalvariate(self.parameter.signal1_mean,  self.parameter.signal1_variance)           
        
        return probability_density
    #-------------------------------------------------------------------------
