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
#  MAIN
#
#-------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    sys.path.append('../src/')
    from tests import Tests
    
    #
    # VARIABLES
    #
    tests = Tests()
 
    args=['./do_tests.py',  "environments/", "test1",  "log/",  "measurements/"]
    
    #
    # CODE: CALL TESTS
    #
#
# AGENT
#
    #tests.agent__sync()
    #tests.agent__compute_decision('test1')
    
#
# NETWORK
#
    #tests.network__clear_network('test1')
    
#
# UPDATER
#
    #tests.updater__check_reinitialization('test1')
#
# RUNNER
#
    #tests.runner__check_runner('test1')
    #tests.runner__get_new_state_of_world('test1')
    
#
# MEASUREMENT
#
    #tests.measurement__measure_average_actions('test_measurements')
    tests.measurement__write_measurement('test_measurements')