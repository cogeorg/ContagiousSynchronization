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
from updater import Updater
from numpy import array


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
    def __init__(self,  identifier,  environment, measurement):
        self.identifier = identifier
        self.environment = environment
        self.measurement = measurement
    #-------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # __str__()
    #-------------------------------------------------------------------------
    def __str__(self):
        
        text = self.identifier + "\n"
        text += self.environment.__str__()
        text += self.measurement.__str__()
        
        return text
    #-------------------------------------------------------------------------
    
    
    #-------------------------------------------------------------------------
    # get_new_state_of_world()
    #-------------------------------------------------------------------------
    def get_new_state_of_world(self, fix_state):
        if int(fix_state) == 0 or int(fix_state) == 1:
            self.environment.parameter.theta = int(fix_state)
        else:
            # first check if state of the world is revealed
            if (random.random() < self.environment.parameter.rho): # state of the world is revealed                 
                # then draw the new state of the world
                # if we have a new state, previous existing connections are worse than useless
                # and would give false signals; thus, remove them
                self.environment.network.clear_network()
                self.environment.network.initialize_network(self.environment.parameter.network_type, self.environment.parameter.network_density)
                if random.random() <= self.environment.parameter.lamb: # what is the new state of the world?
                    self.environment.parameter.theta = 1
                else:
                    self.environment.parameter.theta = 0
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # do_run()
    #-------------------------------------------------------------------------
    def do_run(self):
        debug = False # debug
        
        updater = Updater(self.identifier,  self.environment)
        
        for simulation in range(0, self.environment.parameter.num_simulations):
            
            if (debug): # debug
                print "<< SIMULATION #: " + str(simulation) + " >>"
                
            # reinitialize the network and the agents before every run
            updater.reinitialize(self.identifier, self.environment)
            
            #
            # do the sweeps                
            #
            for sweep in range(0, self.environment.parameter.num_sweeps):
                
                # see if we have a new state of the world (call with -1 for random new state based on parameters)
                self.get_new_state_of_world(self.environment.parameter.theta) # this implies that the state never changes
                
                if (debug): # debug
                    print "<<<< Sweep: " + str(sweep) + " State: " + str(self.environment.parameter.theta) + " >>>>"
                                
                # do the update step
                updater.do_update()
                
                if (debug): # debug
                    print self.environment.network
                
            # end for sweep
            self.measurement.measure_average_actions(self.environment.network.network, sweep) # average_actions is measured differently
            self.measurement.measure_network_density(self.environment.network.network, sweep) # density of network
            self.measurement.measure_path_length(self.environment.network.network, sweep) # average shortest path length
            self.measurement.measure_clustering(self.environment.network.network, sweep) # average clustering
            # utility is measured slightly different and the network instance is passed instead of the networkx graph
            self.measurement.measure_utility(self.environment.network, updater, sweep) 
            self.measurement.measure_individual_utility(self.environment.network, updater, sweep) 
            self.measurement.measure_pairwise_utility(self.environment.network, updater, sweep) 
            
        # end for simulation
        self.measurement.histo_average_actions.append(self.measurement.average_actions[:])
        self.measurement.histo_network_density.append(self.measurement.network_density[:])
        self.measurement.histo_path_length.append(self.measurement.path_length[:])
        self.measurement.histo_clustering.append(self.measurement.clustering[:])
        self.measurement.histo_utility.append(self.measurement.utility[:])        
        self.measurement.histo_individual_utility.append(self.measurement.individual_utility[:])
        self.measurement.histo_pairwise_utility.append(self.measurement.pairwise_utility[:])
        
    #-------------------------------------------------------------------------


#
# COMPUTE GOODNESS
#    
    #-------------------------------------------------------------------------
    # do_run()
    #-------------------------------------------------------------------------
    def compute_goodness(self):
        # it is more efficient to state the hypotheses first, then compute their goodness
        goodness_h1 = 0.0 # the goodness of hypothesis 1
        goodness_h1_max = 0.0 # add std() to mean()
        goodness_h1_min = 0.0 # subtract std() from mean()
        
        parameter = self.environment.parameter
        theta_max = int(parameter.theta_max)
        theta_min = int(parameter.theta_min)
        theta_step = int(parameter.theta_step)
        signal_dist_max = float(parameter.signal_dist_max)
        signal_dist_min = float(parameter.signal_dist_min)
        signal_dist_step = float(parameter.signal_dist_step)
        signal_var_max = float(parameter.signal_var_max)
        signal_var_min = float(parameter.signal_var_min)
        signal_var_step = float(parameter.signal_var_step)
        
        theta_length = (theta_max - theta_min)/theta_step
        signal_dist_length = (signal_dist_max - signal_dist_min)/signal_dist_step
        signal_var_length = (signal_var_max - signal_var_min)/signal_var_step
        volume_element = theta_length*signal_dist_length*signal_var_length # used to normalize goodness with size of volume element
        
        # first loop over the parameters
        if theta_max >= theta_min:
            for theta in range(theta_min, theta_max, theta_step):
                if signal_dist_max >= signal_dist_min:
                    for signal_dist in self.drange(signal_dist_min, signal_dist_max, signal_dist_step):
                        if signal_var_max >= signal_var_min:
                            for signal_variance in self.drange(signal_var_min, signal_var_max, signal_var_step):
                                # clear the previous measurement
                                self.measurement.reinitialize()
                                
                                # then change the current environment accordingly
                                parameter.theta = theta
                                signal0_mean = 0.5 - float(signal_dist/2.0)
                                signal1_mean = 0.5 + float(signal_dist/2.0)
                                parameter.signal0_mean = signal0_mean
                                parameter.signal1_mean = signal1_mean
                                parameter.signal0_variance = signal_variance
                                parameter.signal1_variance = signal_variance
                                
                                # now do the individual run with the new environment
                                if (True):
                                    print "  NOW WORKING ON: ", self.identifier, self.environment.parameter.theta, signal0_mean, signal1_mean, signal_variance
                                self.do_run()
                                
                                #
                                # COMPUTE GOODNESS
                                #
                                # once the run is completed, there is a histogram of measurements for each observable
                                average_actions_array = array(self.measurement.average_actions)
                                #utility_array = array(self.measurement.utility)
                                
                                # hypothesis 1: banks choose the correct state of the world
                                hypothesis_1 = float(theta)
                                
                                # using the means of the histogram, we can compute the goodness
                                # since the goodness uses the integral over the phase space, we have to add up all differences
                                goodness_h1 += ( hypothesis_1 - average_actions_array.mean() )**2/(volume_element)  
                                goodness_h1_max += ( hypothesis_1 - average_actions_array.mean() + average_actions_array.std() )**2/(volume_element)  
                                goodness_h1_min += ( hypothesis_1 - average_actions_array.mean() - average_actions_array.std() )**2/(volume_element)  
                                
                        # end if signal_var
                # end if signal_dist
        # end if theta
        
        # compute goodness of hypothesis
        goodness_h1 = 1.0 - goodness_h1
        goodness_h1_max = 1.0 - goodness_h1_max
        goodness_h1_min = 1.0 - goodness_h1_min
        
        # compute network measures
        density = array(self.measurement.network_density).mean()
        path_length = array(self.measurement.path_length).mean()
        clustering = array(self.measurement.clustering).mean()
        
        # and append it to file
        out_text = str(density) + " " + str(path_length) + " " + str(clustering) + " " 
        out_text += str(goodness_h1) + " " + str(goodness_h1_max) + " " + str(goodness_h1_min) + " "
        out_text += str(self.environment.parameter.num_agents) + " " + str(self.environment.parameter.num_simulations) + " " + str(self.environment.parameter.num_sweeps) + " "
        out_text += str(self.environment.parameter.agent_heterogeneity_parameter)
        out_text += "\n"
        # TODO: this part should be moved into a separate routine
        output_file_name = self.environment.identifier + ".dat"
        with open(output_file_name, "a") as output_file:
            output_file.write(out_text)
    #-------------------------------------------------------------------------
 
   
#
# HELPER ROUTINES
#
    #-------------------------------------------------------------------------
    # def drange(start, stop, step)
    #-------------------------------------------------------------------------
    def drange(self, start, stop, step):
        r = start
        while r < stop:
            yield r
            r+= step
    #-------------------------------------------------------------------------