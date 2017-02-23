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


#-------------------------------------------------------------------------
#
#  class Parameter
#
#-------------------------------------------------------------------------
class Parameter(object):
    
    #
    # METHODS
    #
    def __init__(self,  identifier):
        self.identifier = identifier
        self.num_sweeps = 0
        self.num_simulations = 0
        self.num_agents = 0
        self.rho = 0.0
        self.lamb = 0.0
        self.alpha = 0.0
        self.beta = 0.0
        self.gamma = 0.0
        self.theta = 0
        self.signal0_mean = 0.0
        self.signal0_variance = 0.0
        self.signal1_mean = 0.0
        self.signal1_variance = 0.0
        self.fixed_network = False
        self.network_topology = ''
        self.network_parameter1 = 0.0
        self.network_parameter2 = 0.0
        self.network_density = 0.0
        self.network_type = ""
        self.agent_heterogeneity = False
        self.agent_heterogeneity_parameter = 0.0
        # parameters for computing the goodness value, i.e. parameters that might change during
        # a full parameter check
        self.compute_goodness = False
        self.theta_min = 0.0
        self.theta_max = 0.0
        self.theta_step = 0.0
        self.alpha_min = 0.0
        self.alpha_max = 0.0
        self.alpha_step = 0.0
        self.beta_min = 0.0
        self.beta_max = 0.0
        self.beta_step = 0.0
        self.gamma_min = 0.0
        self.gamma_max = 0.0
        self.gamma_step = 0.0
        self.signal_dist_min = 0.0
        self.signal_dist_max = 0.0
        self.signal_dist_step = 0.0
        self.signal_var_min = 0.0
        self.signal_var_max = 0.0
        self.signal_var_step = 0.0
        self.network_density_min = 0.0
        self.network_density_max = 0.0
        self.network_density_step = 0.0
        

    def __str__(self):
        text = "    <parameter identifier='" + self.identifier + "'>\n"
        text += "      <parameter type='num_sweeps' value='" + str(self.num_sweeps) + "'></parameter>\n"
        text += "      <parameter type='num_simulations' value='" + str(self.num_simulations) + "'></parameter>\n"
        text += "      <parameter type='num_agents' value='" + str(self.num_agents) + "'></parameter>\n"
        text += "      <parameter type='rho' value='" + str(self.rho) + "'></parameter>\n"
        text += "      <parameter type='lamb' value='" + str(self.lamb) + "'></parameter>\n"        
        text += "      <parameter type='alpha' value='" + str(self.alpha) + "'></parameter>\n"
        text += "      <parameter type='beta' value='" + str(self.beta) + "'></parameter>\n"
        text += "      <parameter type='gamma' value='" + str(self.gamma) + "'></parameter>\n"
        text += "      <parameter type='theta' value='" + str(self.theta) + "'></parameter>\n"
        text += "      <parameter type='signal0_mean' value='" + str(self.signal0_mean) + "'></parameter>\n"
        text += "      <parameter type='signal0_variance' value='" + str(self.signal0_variance) + "'></parameter>\n"
        text += "      <parameter type='signal1_mean' value='" + str(self.signal1_mean) + "'></parameter>\n"
        text += "      <parameter type='signal1_variance' value='" + str(self.signal1_variance) + "'></parameter>\n"
        text += "      <parameter type='fixed_network' value='" + str(self.fixed_network) + "'></parameter>\n"
        text += "      <parameter type='network_density' value='" + str(self.network_density) + "'></parameter>\n"      
        text += "    </parameter>\n"
        
        return text
