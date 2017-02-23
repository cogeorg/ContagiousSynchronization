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
from numpy import array

#-------------------------------------------------------------------------
#
#  class Measurement
#
#-------------------------------------------------------------------------
class Measurement(object):
    
    #
    # METHODS
    #
    
    #-------------------------------------------------------------------------
    # def __init__
    #-------------------------------------------------------------------------    
    def __init__(self):
        logging.info("    measurement started...")
        self.average_actions = []
        self.histo_average_actions = []
        
        self.network_density = []
        self.histo_network_density = []
        
        self.path_length = []
        self.histo_path_length = []
        
        self.clustering = []
        self.histo_clustering = []
        
        self.utility = []
        self.histo_utility = []
        self.individual_utility = []
        self.histo_individual_utility = []
        self.pairwise_utility = []
        self.histo_pairwise_utility = []
        
        # used for the "old" variant of measurement, i.e. without aggregating over the number of simulations
        self.actions = []
        self.degree_distribution = []
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # def __init__
    #-------------------------------------------------------------------------    
    def reinitialize(self):
        self.average_actions = []
        self.histo_average_actions = []
        
        self.network_density = []
        self.histo_network_density = []
        
        self.path_length = []
        self.histo_path_length = []
        
        self.clustering = []
        self.histo_clustering = []
        
        self.utility = []
        self.histo_utility = []
        self.individual_utility = []
        self.histo_individual_utility = []
        self.pairwise_utility = []
        self.histo_pairwise_utility = []
        
        # used for the "old" variant of measurement, i.e. without aggregating over the number of simulations
        self.actions = []
        self.degree_distribution = []
    #-------------------------------------------------------------------------
    
    
    #-------------------------------------------------------------------------
    # __str__()
    #-------------------------------------------------------------------------
    def __str__(self):
        text = "histo_average_actions: " + str(self.histo_average_actions) + "\n"
        text += "histo_network_density: " + str(self.histo_network_density) + "\n"
        text += "histo_path_length: " + str(self.histo_path_length) + "\n"
        text += "histo_clustering: " + str(self.histo_clustering) + "\n"
        text += "histo_utility: " + str(self.histo_utility) + "\n"
        text += "histo_individual_utility: " + str(self.histo_individual_utility) + "\n"
        text += "histo_pairwise_utility: " + str(self.histo_pairwise_utility)
        
        return text
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # measure_average_actions(network, sweep)
    #-------------------------------------------------------------------------
    def measure_average_actions(self, network, sweep):
        agent_actions = []
        for node in network.nodes():
            agent_actions.append(node.x)
            
        try:
            self.average_actions.append(float(sum(agent_actions))/len(agent_actions))
        except:
            pass
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # measure_average_actions(network, sweep)
    #-------------------------------------------------------------------------
    def measure_network_density(self, network, sweep):
        density = nx.density(network)
        self.network_density.append(density)
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # measure_average_actions(network, sweep)
    #-------------------------------------------------------------------------
    def measure_path_length(self, network, sweep):
        largest = 0
        length = 0.0
        for component in nx.connected_component_subgraphs(network):
            if (len(component) > largest):
                largest = len(component)
                try: # sometimes we get an empty network
                    length = nx.average_shortest_path_length(component)
                except:
                    length = 0.0
        self.path_length.append(length)
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # measure_average_actions(network, sweep)
    #-------------------------------------------------------------------------
    def measure_clustering(self, network, sweep):
        clustering = 0.0
        try:
            clustering = nx.average_clustering(network)
        except:
            clustering = 0.0
        self.clustering.append(clustering)
    #-------------------------------------------------------------------------

    
    #-------------------------------------------------------------------------
    # measure_utility(network, sweep)
    #-------------------------------------------------------------------------
    def measure_utility(self, network, updater, sweep):
        utility = 0.0

        for agent in network.network.nodes():
            utility += agent.individual_utility + updater.compute_pairwise_utility(agent)

        self.utility.append(utility)
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # measure_individual_utility(network, sweep)
    #-------------------------------------------------------------------------
    def measure_individual_utility(self, network, updater, sweep):
        individual_utility = 0.0

        for agent in network.network.nodes():
            individual_utility += agent.individual_utility

        self.individual_utility.append(individual_utility)
    #-------------------------------------------------------------------------

    
    #-------------------------------------------------------------------------
    # measure_utility(network, sweep)
    #-------------------------------------------------------------------------
    def measure_pairwise_utility(self, network, updater, sweep):
        pairwise_utility = 0.0

        for agent in network.network.nodes():
            pairwise_utility += updater.compute_pairwise_utility(agent)

        self.pairwise_utility.append(pairwise_utility)
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # def do_measurement(network)
    # DEPRECATED
    #-------------------------------------------------------------------------    
    def do_measurement(self, network, sweep):
        # sweep is used to make measurements with different
        # probability for state revelation comparable
        agent_actions = []
        degree_distribution = []
        for node in network.nodes():
            agent_actions.append(node.x)
            degree_distribution.append(network.degree(node))
        
        logging.info("      ...now measuring sweep: " + str(len(self.actions)) )
        #print "------------------------------------------------------"
        #print agent_actions
        #print "------------------------------------------------------"        
        self.actions.append(agent_actions[:])
        self.degree_distribution.append(degree_distribution[:])
    #-------------------------------------------------------------------------
        
    
    #-------------------------------------------------------------------------
    # def write_measurement(measurement_file_name)
    #-------------------------------------------------------------------------
    def write_measurement(self, measurement_file_name):
        #
        # WRITE HISTOGRAMS
        #
        self.write_histogram(self.actions, measurement_file_name + "-histo-actions.dat")
        self.write_histogram(self.degree_distribution, measurement_file_name + "-histo-degree_distribution.dat")
        
        self.write_histogram(self.histo_average_actions, measurement_file_name + "-histo-average_actions.dat")
        self.write_histogram(self.histo_network_density, measurement_file_name + "-histo-network_density.dat")
        self.write_histogram(self.histo_path_length, measurement_file_name + "-histo-path_length.dat")
        self.write_histogram(self.histo_clustering, measurement_file_name + "-histo-clustering.dat")
        self.write_histogram(self.histo_utility, measurement_file_name + "-histo-utility.dat")
        self.write_histogram(self.histo_individual_utility, measurement_file_name + "-histo-individual_utility.dat")
        self.write_histogram(self.histo_pairwise_utility, measurement_file_name + "-histo-pairwise_utility.dat")
        
        #
        # CONVERT TO NUMPY ARRAY AND WRITE MEAN, STD
        #
        average_actions_array = array(self.average_actions)
        self.write_results(average_actions_array.mean(), average_actions_array.std(),  measurement_file_name + "-res-actions.dat")
        network_density_array = array(self.network_density)
        self.write_results(network_density_array.mean(), network_density_array.std(),  measurement_file_name + "-res-network_density.dat")
        path_length_array = array(self.path_length)
        self.write_results(path_length_array.mean(), path_length_array.std(),  measurement_file_name + "-res-path_length.dat")
        clustering_array = array(self.clustering)
        self.write_results(clustering_array.mean(), clustering_array.std(),  measurement_file_name + "-res-clustering.dat")
        utility_array = array(self.utility)
        self.write_results(utility_array.mean(), utility_array.std(),  measurement_file_name + "-res-utility.dat")
        individual_utility_array = array(self.individual_utility)
        self.write_results(individual_utility_array.mean(), individual_utility_array.std(),  measurement_file_name + "-res-individual_utility.dat")
        pairwise_utility_array = array(self.pairwise_utility)
        self.write_results(pairwise_utility_array.mean(), pairwise_utility_array.std(),  measurement_file_name + "-res-pairwise_utility.dat")
        
        logging.info("    ...measurement written")
    #-------------------------------------------------------------------------
        
        
    #--------------------------------------------------------------------------
    # def write_histogram(histogram, file_name)
    #-------------------------------------------------------------------------
    def write_histogram(self,  histogram,  file_name):
        file = open(file_name,  "w")
        for line in histogram:
            print_line = True
            for entry in line:
                if (entry == None): # measurement before update step will produce None in first period
                    print_line = False
                else:
                    file.write(str(round(float(entry), 7)) + " ")
            
            if print_line: # clumsy but works; no new line when line is None, None, None
                file.write("\n")
        file.close()
    #-------------------------------------------------------------------------


    #--------------------------------------------------------------------------
    # def write_histogram(histogram, file_name)
    #-------------------------------------------------------------------------
    def write_results(self,  mean, std, file_name):
        file = open(file_name,  "w")
        out_text = str(round(float(mean),7)) + " " + str(round(float(std), 7))
        file.write(out_text + "\n")
        file.close()
    #-------------------------------------------------------------------------
