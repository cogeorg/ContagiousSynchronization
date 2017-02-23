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
import networkx as nx
from agent import Agent

#-------------------------------------------------------------------------
#
#  class Network
#
#-------------------------------------------------------------------------
class Network(object):
    
    #
    # METHODS
    #

    #-------------------------------------------------------------------------
    # __init__(identifier)
    #-------------------------------------------------------------------------
    def __init__(self,  identifier, network_type, network_density):
        self.identifier = identifier
        self.network = nx.Graph()
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # __str__
    #-------------------------------------------------------------------------
    def __str__(self):
        text = "    <network identifier='" + self.identifier + "'>\n"
        for agent in self.network.nodes():
            text += str(agent) + "\n"
        for edge in self.network.edges():
            text += "      <edge from='" + str(edge[0].identifier) + "' to='" + str(edge[1].identifier) + "'>\n"
        text += "    </network>\n"
        
        return text
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # initialize(num_agents)
    #-------------------------------------------------------------------------
    def initialize(self,  num_agents, network_type, network_density, network_topology, network_parameter1, network_parameter2):
        for i in range(0,  num_agents):
            agent = Agent(str(i))
            self.network.add_node(agent)
            
        if network_type == "star": # this is used for testing purposes only
            self.create_star_network()
        if network_topology == "random":
            self.create_exogenous_network(float(network_density))
        if network_topology == "ws": # watts-strogaz network
            self.create_watts_strogatz_network(int(network_parameter1), network_parameter2) # k,p
        if network_topology == "ba": # barabasi-albert network
            self.create_barabasi_albert_network(int(network_parameter1)) # m
        else:
            self.create_exogenous_network(float(network_density))
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # create_star_network
    #-------------------------------------------------------------------------
    def create_star_network(self):
        for agent in self.network.nodes():
            for neighbor in self.network.nodes():
                if neighbor != agent and [agent, neighbor] not in self.network.edges():
                    if agent.identifier == "0":
                        self.network.add_edge(agent, neighbor)
    #-------------------------------------------------------------------------
    

    #-------------------------------------------------------------------------
    # create_exogenous_network
    # this is a bit cumbersome, but since nodes are not integers in this model
    # the usual graph generation functions of networkx do not simply work out 
    # of the box and have to be re-implemented
    #-------------------------------------------------------------------------
    def create_exogenous_network(self,  network_density):
        # create a local random network to get the structure
        ws_network = nx.gnp_random_graph(len(self.network.nodes()), network_density)
        # then add all edges in self.network
        for edge in ws_network.edges():
            self.network.add_edge(self.find_node_by_id(edge[0]), self.find_node_by_id(edge[1]))
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # create_watts_strogatz_network
    # this is a bit cumbersome, but since nodes are not integers in this model
    # the usual graph generation functions of networkx do not simply work out 
    # of the box and have to be re-implemented
    #-------------------------------------------------------------------------
    def create_watts_strogatz_network(self, n, p):
        # create a local watts strogatz network to get the structure
        ws_network = nx.watts_strogatz_graph(len(self.network.nodes()), n, p)
        # then add all edges in self.network
        for edge in ws_network.edges():
            self.network.add_edge(self.find_node_by_id(edge[0]), self.find_node_by_id(edge[1]))
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # create_barabasi_albert_network
    # this is a bit cumbersome, but since nodes are not integers in this model
    # the usual graph generation functions of networkx do not simply work out 
    # of the box and have to be re-implemented
    #-------------------------------------------------------------------------
    def create_barabasi_albert_network(self, m):
        # create a local barabasi-albert graph to get the structure
        ba_network = nx.barabasi_albert_graph(len(self.network.nodes()), m)
        for edge in ba_network.edges():
            self.network.add_edge(self.find_node_by_id(edge[0]), self.find_node_by_id(edge[1]))
    #-------------------------------------------------------------------------


#
# HELPER ROUTINES
#
    #-------------------------------------------------------------------------
    # find_node_by_id(id)
    #-------------------------------------------------------------------------
    def find_node_by_id(self, id):
        found = None
        for node in self.network.nodes():
            if int(node.identifier) == id:
                found = node
        return found
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # clear_network()
    #-------------------------------------------------------------------------
    def clear_network(self):
        self.network.remove_edges_from(self.network.edges())
    #-------------------------------------------------------------------------
