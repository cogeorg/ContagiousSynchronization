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
import math
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
    #-------------------------------------------------------------------------
    # __init__(identifier)
    #-------------------------------------------------------------------------
    def __init__(self,  identifier):
        self.identifier = identifier
        self.parameter = Parameter(self.identifier)
        self.network = Network(self.identifier, self.parameter.network_type, self.parameter.network_density)
    #-------------------------------------------------------------------------
    

    #-------------------------------------------------------------------------
    # __str__()
    #-------------------------------------------------------------------------
    def __str__(self):
        text = "<environment identifier='" + self.identifier + "'>\n"
        text += str(self.network)
        text += str(self.parameter)
        text += "</environment>\n"
        
        return text
    #-------------------------------------------------------------------------

    
    #-------------------------------------------------------------------------
    # initialize_environment
    #-------------------------------------------------------------------------
    def initialize(self):
        self.network.initialize(self.parameter.num_agents, 
                                self.parameter.network_type, 
                                self.parameter.network_density,
                                self.parameter.network_topology,
                                self.parameter.network_parameter1,
                                self.parameter.network_parameter2)
    #-------------------------------------------------------------------------

    
#
# INITIALIZATON FUNCTIONS
#
    #-------------------------------------------------------------------------
    # read_environment_file(environment_filename)
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
            #
            # simulation parameters for single run
            #
            # the first set of parameters will be valid for the whole simulation
            if (subelement.attrib['type'] == 'num_sweeps'):
                self.parameter.num_sweeps = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'num_simulations'):
                self.parameter.num_simulations = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'num_agents'):
                self.parameter.num_agents = int(subelement.attrib['value'])
            # model parameters
            if (subelement.attrib['type'] == 'rho'):
                self.parameter.rho = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'lamb'):
                self.parameter.lamb = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'alpha'):
                self.parameter.alpha = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'beta'):
                self.parameter.beta = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'gamma'):
                self.parameter.gamma = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'theta'):
                self.parameter.theta = int(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal0_mean'):
                self.parameter.signal0_mean = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal0_variance'):
                self.parameter.signal0_variance = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal1_mean'):
                self.parameter.signal1_mean = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'signal1_variance'):
                self.parameter.signal1_variance = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'fixed_network'): # watch out with converting a string to a bool
                if subelement.attrib['value'] == "True": # bool("non-empty string") = True 
                    self.parameter.fixed_network = True
                else: 
                    self.parameter.fixed_network = False
            if (subelement.attrib['type'] == 'network_topology'):
                self.parameter.network_topology = subelement.attrib['value']
            if (subelement.attrib['type'] == 'network_parameter1'):
                self.parameter.network_parameter1 = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'network_parameter2'):
                self.parameter.network_parameter2 = float(subelement.attrib['value'])            
            if (subelement.attrib['type'] == 'network_density'):
                self.parameter.network_density = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'network_type'):
                self.parameter.network_type = subelement.attrib['value']
                
            if (subelement.attrib['type'] == 'agent_heterogeneity'): # watch out with converting a string to a bool
                if subelement.attrib['value'] == "True": # bool("non-empty string") = True 
                    self.parameter.agent_heterogeneity = True
                else: 
                    self.parameter.agent_heterogeneity = False
            if (subelement.attrib['type'] == 'agent_heterogeneity_parameter'):
                self.parameter.agent_heterogeneity_parameter = subelement.attrib['value']
            #
            # parameters for computing the goodness value
            #
            if (subelement.attrib['type'] == 'compute_goodness'):
                self.parameter.compute_goodness = subelement.attrib['value']
            # theta
            if (subelement.attrib['type'] == 'theta_min'):
                self.parameter.theta_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'theta_max'):
                self.parameter.theta_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'theta_step'):
                self.parameter.theta_step = subelement.attrib['value']
            # alpha, beta, gamma
            if (subelement.attrib['type'] == 'alpha_min'):
                self.parameter.alpha_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'alpha_max'):
                self.parameter.alpha_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'alpha_step'):
                self.parameter.alpha_step = subelement.attrib['value']
            if (subelement.attrib['type'] == 'beta_min'):
                self.parameter.beta_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'beta_max'):
                self.parameter.beta_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'beta_step'):
                self.parameter.beta_step = subelement.attrib['value']
            if (subelement.attrib['type'] == 'gamma_min'):
                self.parameter.gamma_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'gamma_max'):
                self.parameter.gamma_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'gamma_step'):
                self.parameter.gamma_step = subelement.attrib['value']
            # signal
            if (subelement.attrib['type'] == 'signal_dist_min'):
                self.parameter.signal_dist_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'signal_dist_max'):
                self.parameter.signal_dist_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'signal_dist_step'):
                self.parameter.signal_dist_step = subelement.attrib['value']
            if (subelement.attrib['type'] == 'signal_var_min'):
                self.parameter.signal_var_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'signal_var_max'):
                self.parameter.signal_var_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'signal_var_step'):
                self.parameter.signal_var_step = subelement.attrib['value']
                
            # density
            if (subelement.attrib['type'] == 'network_density_min'):
                self.parameter.network_density_min = subelement.attrib['value']
            if (subelement.attrib['type'] == 'network_density_max'):
                self.parameter.network_density_max = subelement.attrib['value']
            if (subelement.attrib['type'] == 'network_density_step'):
                self.parameter.network_density_step = subelement.attrib['value']

    #-------------------------------------------------------------------------


#
# HELPER FUNCTIONS
#
    #-------------------------------------------------------------------------
    # get_probability_density(s)
    #-------------------------------------------------------------------------
    def get_probability_density(self, s, state):
        # this function returns the *value* of the pdf of F0, F1 evaluated at s
        probability_density=0.0
        
        if self.parameter.agent_heterogeneity: # if we actually have agent heterogeneity
            if random.random() < self.parameter.agent_heterogeneity_parameter: # if p<p_inf : we have an informed agent
                if state == 0.0:
                    mu = 0.25
                    sigma2 = self.parameter.signal0_variance
                else:
                    mu = 0.75
                    sigma2 = self.parameter.signal1_variance                
            else: # else the agent is uninformed
                if state == 0.0:
                    mu = 0.49
                    sigma2 = self.parameter.signal0_variance
                else:
                    mu = 0.51
                    sigma2 = self.parameter.signal1_variance
        else: # no agent heterogeneity, the default            
            if state == 0.0:
                mu = self.parameter.signal0_mean
                sigma2 = self.parameter.signal0_variance
            else:
                mu = self.parameter.signal1_mean
                sigma2 = self.parameter.signal1_variance
            
        probability_density = 1.0/(math.sqrt(2.0*math.pi*sigma2))*math.exp(-(s-mu)*(s-mu)/(2.0*sigma2))
        
        return probability_density
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # get_signal()
    #-------------------------------------------------------------------------
    def get_signal(self):
        theta = self.parameter.theta
        if (theta == 0.0): # check if theta == 0
            mu = self.parameter.signal0_mean
            sigma2 = self.parameter.signal0_variance
        elif (theta == 1.0): # or theta == 1.0
            mu = self.parameter.signal1_mean
            sigma2 = self.parameter.signal1_variance
        else: # or throw an error
            print "ERROR: theta \ni {0,1}"
        s = random.normalvariate(mu, sigma2) # draw signal
        
        return s
    #-------------------------------------------------------------------------
