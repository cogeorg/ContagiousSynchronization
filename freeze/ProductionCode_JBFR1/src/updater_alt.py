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
import random
import networkx as nx
import numpy as np

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
    # __str__()
    #-------------------------------------------------------------------------
    def __str__(self):
        text = self.environment.__str__()        
        return text
    #-------------------------------------------------------------------------

    
    #-------------------------------------------------------------------------
    # reinitialize(identifier, environment)
    #-------------------------------------------------------------------------
    def reinitialize(self, identifier, environment):
        debug = False
        
        self.identifier = identifier
        self.environment = environment
                
        # clear edges if network is endogenous
        if not self.environment.parameter.fixed_network:
            self.environment.network.network.remove_edges_from(self.environment.network.network.edges())
        
        for agent in self.environment.network.network.nodes():
            agent.reinitialize(agent.identifier)
        
        if (debug):
            print self.environment.network
    #-------------------------------------------------------------------------

    
    #-------------------------------------------------------------------------
    # do_update()
    #-------------------------------------------------------------------------
    def do_update(self):
        network = self.environment.network
        debug = False # debug

        A = nx.adjacency_matrix(network)
        k = np.sum(A,axis=1)
        k_alt = np.copy(k)
        k[k == 0] = 1

        x = np.zeros((len(self.environment.network.network.nodes()),1))
        p = np.zeros((len(self.environment.network.network.nodes()),1))
        cnt = 0
        for agent in self.environment.network.network.nodes():
            s = self.environment.get_signal()
            F0s = self.environment.get_probability_density(s, 0.0)
            F1s = self.environment.get_probability_density(s, 1.0)
            x[cnt,0] = agent.x
            p[cnt,0] = 1./(1 + F0s/F1s)
            cnt += 1


        q = A.dot(x)/k
        x = np.around(0.5*(p + q))
        x[k_alt == 0] = np.around(p[k_alt == 0])

        cnt = 0
        for agent in self.environment.network.network.nodes():
            agent.x = x[cnt,0]
            cnt += 1

            # and compute and set individual utility
            if (agent.x == self.environment.parameter.theta):
                agent.individual_utility = 1
            else:
                agent.individual_utility = 0

        #
        # compute decision and individual utility for all agents
        #
        if (debug): # debug
            print "  << BAYESIAN UPDATING >>"


            
        
        #
        # compute pairwise utility and find new network structure
        #
        if (debug): # debug
            print "  << NETWORK FORMATION >>"
        # if we not have a fixed network create network endogenously, alternatively, keep existing network
        if (not self.environment.parameter.fixed_network): # if we not have a fixed network create network endogenously
        #
        # ENDOGENOUS NETWORK FORMATION
        #
            # clear edges
            network.network.remove_edges_from(self.environment.network.network.edges())
            
            # loop over all agents and compute pairwise utility
            for agent in self.environment.network.network.nodes():
                # by looping over all potential neighbors (all other nodes in the network)
                for potential_neighbor in self.environment.network.network.nodes():
                    # no self loops and to speed up things we also exclude pairs we already checked
                    if potential_neighbor != agent and [agent, potential_neighbor] not in self.environment.network.network.edges():
                        # add a link if utility of both agents is larger than zero
                        agent_utility = self.compute_pairwise_utility(agent)
                        neighbor_utility = self.compute_pairwise_utility(potential_neighbor)
                        
                        if (False): # debug
                            print agent
                            print potential_neighbor
                            print "      <agent_utility, neighbor_utility: ", agent_utility, neighbor_utility, ">"
                            
                        if (agent_utility > 0.0 and neighbor_utility > 0.0 ):
                            self.environment.network.network.add_edge(agent, potential_neighbor)
        
        #
        # finally, sync the previous decisions
        #
        for agent in self.environment.network.network.nodes():
            agent.sync()
    #-------------------------------------------------------------------------
    
    
    #-------------------------------------------------------------------------
    # compute_pairwise_utility(agent, potential_neighbor)
    #-------------------------------------------------------------------------
    def compute_pairwise_utility(self,  agent):
        parameter = self.environment.parameter
        network_density = float(len(self.environment.network.network.edges())) / (parameter.num_agents*(parameter.num_agents - 1))
        
        pairwise_utility_agent = parameter.alpha \
                                    + parameter.beta*(2.0*agent.q - 1.0) \
                                    - parameter.gamma*network_density*agent.q
        
        return pairwise_utility_agent
    #-------------------------------------------------------------------------
    