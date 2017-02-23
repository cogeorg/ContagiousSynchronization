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


#-------------------------------------------------------------------------
#
#  class Agent
#
#-------------------------------------------------------------------------
class Agent(object):
    
    #
    # METHODS
    #
    def __init__(self,  identifier):
        self.identifier = identifier
        self.x = None # action taken by the agent
        self.previous_x = None # previous action taken by agent
        self.individual_utility = None # Bayesian utility of agent


    def __str__(self):
        text = "    <agent identifier='" + self.identifier + "' action='" + str(self.x) + "'></agent>"        
        return text


	#-------------------------------------------------------------------------
	# functions needed to make Agent() hashable
	#-------------------------------------------------------------------------
	def __key(self):
		return self.identifier

	def __eq__(self, other):
		return self.__key() == other.__key()

	def __hash__(self):
		return hash(self.__key())
	#-------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # sync
    #-------------------------------------------------------------------------
    def sync(self):
        self.previous_x=self.x
    #-------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------
    # compute_decision
    #-------------------------------------------------------------------------
    def compute_decision(self, previous_decisions_of_neighbors, num_agents, F0s,  F1s):
        
        #decision should be = self.x no??
        self.x = 0
        
        private_belief = 1.0/(1.0 + F0s/F1s)
        try:
            social_belief = float(sum(previous_decisions_of_neighbors))/len(previous_decisions_of_neighbors)
        except: 
            social_belief = 0.0 
        
        threshold = 0.5 + float(len(previous_decisions_of_neighbors))/(num_agents*(num_agents-1))
        if (private_belief + social_belief > threshold):
            self.x = 1
        
    #-------------------------------------------------------------------------

