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
#import logging

#-------------------------------------------------------------------------
#
#  class Agent
#
#-------------------------------------------------------------------------
class Agent(object):
    
    #
    # METHODS
    #
    #-------------------------------------------------------------------------
    # __init__(identifier)
    #-------------------------------------------------------------------------
    def __init__(self,  identifier):
        self.identifier = identifier
        self.x = None # action taken by the agent
        self.previous_x = None # previous action taken by agent
        self.individual_utility = None # Bayesian utility of agent
        self.private_belief = None # the priavte belief of the agent
        self.q = None # q is a measure of how close the private belief is to the threshold
        self.r = None # r is the measure of how close the private + social belief are to the threshold
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # reinitialize()
    #-------------------------------------------------------------------------
    def reinitialize(self, identifier):
        self.identifier = identifier
        self.x = None # action taken by the agent
        self.previous_x = None # previous action taken by agent
        self.individual_utility = None # Bayesian utility of agent
        self.private_belief = None # the priavte belief of the agent
        self.q = None # q is a measure of how close the private belief is to a state
        self.r = None # r is the measure of how close the private + social belief are to the threshold
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # __str__()
    #-------------------------------------------------------------------------
    def __str__(self):
        text = "      <agent identifier='" + self.identifier + "' action='" + str(self.x) + "'"
        text += " previous_x='" + str(self.previous_x) + "'"
        text += " individual_utility='" + str(self.individual_utility) + "'"
        text += " private_belief='" + str(self.private_belief) + "'"
        text += " q='" + str(self.q) + "'"
        text += " r='" + str(self.r) + "'"
        text += "></agent>"        
        return text
    #-------------------------------------------------------------------------


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
        self.previous_x = self.x
    #-------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------
    # compute_decision
    #-------------------------------------------------------------------------
    def compute_decision(self, previous_decisions_of_neighbors, num_agents, F0s,  F1s):
        self.x = 0.0 # action chosen
        debug = False # show debug print statements

        # compute private belief        
        self.private_belief = 1.0/(1.0 + F0s/F1s)
        
        # now compute the distance to threshold as proxy for how sure the agent is given
        # the private belief
        if self.private_belief <= 0.5:
            self.q = 2.0*self.private_belief
        else:
            self.q = 2.0*(1.0-self.private_belief)
        
        
        # compute the social belief if possible
        try: # we need to check for the case when there is no previous neighbor
            social_belief = float(sum(previous_decisions_of_neighbors))/len(previous_decisions_of_neighbors)
        except: 
            social_belief = 0.0 

        # compute the threshold for computing the action
        threshold = 1.0#0.5*( 1.0 + float(len(previous_decisions_of_neighbors))/(num_agents-1) )
        # now compute the distance to threshold as proxy for how sure the agent is given
        # the private belief
        if self.private_belief + social_belief <= threshold:
            self.r = 2.0*(self.private_belief + social_belief)
        else:
            self.r = 2.0*(threshold - self.private_belief - social_belief)
            
        # and compare if private and social belief exceed threshold
        if (self.private_belief + social_belief > threshold):
            self.x = 1.0
            
        if (debug): # debug
            print "      <private_belief, social_belief, threshold, q, r, x: ", self.private_belief, social_belief, threshold, self.q, self.r, self.x, ">"
    #-------------------------------------------------------------------------

