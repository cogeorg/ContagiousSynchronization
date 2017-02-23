#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2012 Co-Pierre Georg (co-pierre.georg@keble.ox.ac.uk)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging

#-------------------------------------------------------------------------
#  class Tests
#-------------------------------------------------------------------------
class Tests(object):
    #
    # VARIABLES
    #
    
    
    # 
    # METHODS
    #
    
    #-------------------------------------------------------------------------
    # __init__
    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # print_info(text)
    #-------------------------------------------------------------------------
    def print_info(self, text):
        print '##############################################################################\n'
        print text
        print '##############################################################################\n'
    #-------------------------------------------------------------------------

        
#-------------------------------------------------------------------------
#  TESTS FOR AGENT
#-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # agent__sync(self)
    #-------------------------------------------------------------------------    
    def agent__sync(self):
        from agent import Agent
        agent = Agent('1')
        agent.x = 1.0
        print agent
        agent.sync()
        print agent
    #-------------------------------------------------------------------------    


    #-------------------------------------------------------------------------
    # agent__sync(self)
    #-------------------------------------------------------------------------    
    def agent__compute_decision(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)

        print environment
        
        print "<<< TEST 1"
        # set all agent actions and sync them to their previous actions
        for agent in environment.network.network.nodes():
            agent.x = 1.0
            agent.sync()
        # then compute action for each action
        for agent in environment.network.network.nodes():
            F0s = 1.0
            F1s = 1.0
            print "        F0s, F1s: ", F0s, F1s            
            
            # we need the previous decisions of neighbors
            neighbors_previous_decision=[]
            for neighbor in environment.network.network.neighbors(agent):
                neighbors_previous_decision.append(neighbor.previous_x)
            agent.compute_decision(neighbors_previous_decision, environment.parameter.num_agents, F0s, F1s)
            print agent
            
        print "<<< TEST 2"
        # set all agent actions and sync them to their previous actions
        for agent in environment.network.network.nodes():
            agent.x = 0.0
            agent.sync()
        # then compute action for each action
        for agent in environment.network.network.nodes():
            print agent
            F0s = 0.1
            F1s = 1.0
            print "        F0s, F1s: ", F0s, F1s
            
            # we need the previous decisions of neighbors
            neighbors_previous_decision=[]
            for neighbor in environment.network.network.neighbors(agent):
                neighbors_previous_decision.append(neighbor.previous_x)
            agent.compute_decision(neighbors_previous_decision, environment.parameter.num_agents, F0s, F1s)
            print agent
            print

    #-------------------------------------------------------------------------    


#-------------------------------------------------------------------------
#  TESTS FOR NETWORK
#-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # updater__check_reinitialization(identifier)
    #-------------------------------------------------------------------------    
    def network__clear_network(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from updater import Updater
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)
        print environment
        
        environment.network.clear_network()
        print environment
    #-------------------------------------------------------------------------            

#-------------------------------------------------------------------------
#  TESTS FOR UPDATER
#-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # updater__check_reinitialization(identifier)
    #-------------------------------------------------------------------------    
    def updater__check_reinitialization(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from updater import Updater
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)        
        
        updater = Updater(identifier, environment)
        print "<<< BEFORE UPDATE"
        print updater
        
        print "<<< UPDATING "
        updater.do_update()        
        print updater
        
        updater.reinitialize(identifier, environment)
        print"<<< AFTER REINITIALIZATION"
        print updater
    #-------------------------------------------------------------------------    
    

#-------------------------------------------------------------------------
#  TESTS FOR RUNNER
#-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # runner__check_runner(self, identifier)
    #-------------------------------------------------------------------------    
    def runner__check_runner(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from measurement import Measurement            
        from runner import Runner
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)
        # and also a measurement
        measurement = Measurement()
        
        runner = Runner(identifier, environment, measurement)
        print runner
        print
        runner.do_run()
        print runner
    #-------------------------------------------------------------------------    


    #-------------------------------------------------------------------------
    # runner__get_new_state_of_world(self, identifier)
    #-------------------------------------------------------------------------    
    def runner__get_new_state_of_world(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from measurement import Measurement            
        from runner import Runner
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)
        # and also a measurement
        measurement = Measurement()
        
        runner = Runner(identifier, environment, measurement)
        print runner
        print
        runner.get_new_state_of_world(1)
        print runner
        runner.get_new_state_of_world(0)
        print runner
        runner.get_new_state_of_world(-1)
        print runner
    #-------------------------------------------------------------------------    

#
# TEST FOR MEASUREMENT
#
    #-------------------------------------------------------------------------
    # measurement__measure_average_actions(self, identifier)
    #-------------------------------------------------------------------------    
    def measurement__measure_average_actions(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from measurement import Measurement            
        from runner import Runner
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'        
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)
        # and also a measurement
        measurement = Measurement()
        for agent in environment.network.network.nodes():
            F0s = 1.0
            F1s = 1.0
            
            # we need the previous decisions of neighbors
            neighbors_previous_decision=[]
            for neighbor in environment.network.network.neighbors(agent):
                neighbors_previous_decision.append(neighbor.previous_x)
            agent.compute_decision(neighbors_previous_decision, environment.parameter.num_agents, F0s, F1s)
        
        runner = Runner(identifier, environment, measurement)
        print runner
        
        runner.do_run()
        print runner
    #-------------------------------------------------------------------------    


    #-------------------------------------------------------------------------
    # measurement__measure_average_actions(self, identifier)
    #-------------------------------------------------------------------------    
    def measurement__write_measurement(self, identifier):
        #
        # VARIABLES
        #
        from environment import Environment
        from measurement import Measurement            
        from runner import Runner
        
        #
        # CODE
        #
        
        # we need the environment
        environment_directory = 'environments/'
        measurement_directory = 'measurements/'
        environment = Environment(identifier)
        environment.read_environment_file("./" + environment_directory + identifier + ".xml")
        environment.initialize()
        
        # and we need to create an exogenous network
        environment.network.create_exogenous_network(environment.parameter.network_density)
        # and also a measurement
        measurement = Measurement()
        for agent in environment.network.network.nodes():
            F0s = 1.0
            F1s = 1.0
            
            # we need the previous decisions of neighbors
            neighbors_previous_decision=[]
            for neighbor in environment.network.network.neighbors(agent):
                neighbors_previous_decision.append(neighbor.previous_x)
            agent.compute_decision(neighbors_previous_decision, environment.parameter.num_agents, F0s, F1s)
        
        runner = Runner(identifier, environment, measurement)
        print runner
        
        runner.do_run()
        print runner
        
        measurement.write_measurement(measurement_directory + identifier)
    #-------------------------------------------------------------------------    
