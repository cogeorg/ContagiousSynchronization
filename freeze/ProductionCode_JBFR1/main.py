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
    #import pdb # python debugger, for debugging purposes only
    
    import sys
    sys.path.append('src/')
    import logging
    from datetime import datetime

    from environment import Environment
    from runner import Runner
    from measurement import Measurement
    
    args = sys.argv


#
# INITIALIZATION
#
    environment_directory = str(args[1])
    identifier = str(args[2])
    log_directory = str(args[3])
    measurement_directory = str(args[4])

    # Configure logging parameters so we get output while the program runs
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S',  filename = log_directory + identifier + ".log", level=logging.INFO)
    logging.info('START logging for run: %s',  environment_directory + identifier + ".xml")

    environment = Environment(identifier)
    environment.read_environment_file("./" + environment_directory + identifier + ".xml")
    environment.initialize()
    
    measurement = Measurement()
    
#
# UPDATE STEP
#
    runner = Runner(identifier,  environment, measurement)
    if environment.parameter.compute_goodness == "True": # compute_goodness = False if we have a normal run
        #print "NOW RUNNING: " + environment.identifier
        #start_time = datetime.now()
        #print "START: " + str(start_time)
        
        runner.compute_goodness()

        #end_time = datetime.now()
        #print "END: " + str(end_time)
        #print "TIME: " + str(end_time - start_time) + "\n"
        
        #measurement.write_measurement(measurement_directory + identifier)
        #logging.info('FINISHED logging for run: %s \n', environment_directory + identifier + ".xml")
    else: # we do *not* want to compute goodness
        print "NOW RUNNING: " + environment.identifier
        start_time = datetime.now()
        print "START: " + str(start_time)

        runner.do_run()
        
        end_time = datetime.now()
        print "END: " + str(end_time)
        print "TIME: " + str(end_time - start_time) + "\n"

        measurement.write_measurement(measurement_directory + identifier)
        logging.info('FINISHED logging for run: %s \n', environment_directory + identifier + ".xml")
