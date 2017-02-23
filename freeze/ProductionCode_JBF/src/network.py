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
    def __init__(self,  identifier):
        self.identifier = identifier
        self.network = nx.Graph()


    def __str__(self):
        text = "  <network identifier='" + self.identifier + "'>\n"
        for agent in self.network.nodes():
            text += str(agent) + "\n"
        for edge in self.network.edges():
            text += "    <edge from='" + str(edge[0].identifier) + "' to='" + str(edge[1].identifier) + "'>\n"
        text += "  </network>\n"
        
        return text


    #-------------------------------------------------------------------------
    # initialize(num_agents)
    #-------------------------------------------------------------------------
    def initialize(self,  num_agents):
        
        for i in range(0,  num_agents):
            agent = Agent(str(i))
            self.network.add_node(agent)
    #-------------------------------------------------------------------------
