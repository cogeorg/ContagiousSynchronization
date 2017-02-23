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


#-------------------------------------------------------------------------
#
#  class Updater
#
#-------------------------------------------------------------------------
class Updater(object):
    
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
    # do_update()
    #-------------------------------------------------------------------------
    def do_update(self):
        
        #
        # compute decision and individual utility for all agents
        #
        print "agent actions:"
        for agent in self.environment.network.network.nodes():
            # first, loop over all agents
            
            # each agent is provided with a private signal
            s = random.random()
            F0s = self.environment.get_probability_density(s,  0)
            F1s = self.environment.get_probability_density(s,  1)
                #print "signals: " + str(F0s) + " " + str(F1s) + " " + str(s)
            
            # and the former decision of her neighbors
            neighbors_previous_decision=[]
            for neighbor in self.environment.network.network.neighbors(agent):
                neighbors_previous_decision.append(neighbor.previous_x)
            
            # compute decision of agent
            agent.compute_decision(neighbors_previous_decision,  self.environment.parameter.num_agents, F0s,  F1s)
            # compute and set individual utility
            if (agent.x == self.environment.parameter.theta):
                agent.individual_utility = 1
            else:
                agent.individual_utility = 0
            
                #print agent
        
        #
        # compute pairwise utility and find new network structure
        #
        self.environment.network.network.remove_edges_from(self.environment.network.network.edges()) # clear edges
        for agent in self.environment.network.network.nodes():
            #compute pairwise utility
            for potential_neighbor in self.environment.network.network.nodes():
                if potential_neighbor != agent and [agent, potential_neighbor] not in self.environment.network.network.edges():
                    if (self.compute_pairwise_utility(agent,  potential_neighbor) > 0.0 and 
                        self.compute_pairwise_utility(potential_neighbor,  agent) > 0.0
                        ):
                            self.environment.network.network.add_edge(agent,  potential_neighbor)
        
        print self.environment.network
        #
        # finally, sync the previous decisions
        #
        for agent in self.environment.network.network.nodes():
            agent.sync()
        
    
    
    #-------------------------------------------------------------------------
    # compute_pairwise_utility(agent, potential_neighbor)
    #-------------------------------------------------------------------------
    def compute_pairwise_utility(self,  agent,  potential_neighbor):
        parameter = self.environment.parameter
        network_density = float(len(self.environment.network.network.edges())) / (parameter.num_agents*(parameter.num_agents - 1))
        
        pairwise_utility_agent = parameter.alpha - parameter.gamma*network_density*(1.0 - potential_neighbor.individual_utility)
        
        return pairwise_utility_agent
    #-------------------------------------------------------------------------
