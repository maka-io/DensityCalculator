#!/usr/bin/python
'''
Created: 07/14/2015
Updated: 07/18/2015

Module insertion point: run.py accepts the file i/o
Handles basic logging and execution of density calculations.

'''
__author__ = "M@Campbell"

import sys
import logging

# Our module
from DensityCalc import DensityCalc as DC

LOGFILE_NAME = 'output.log'

def main(argv):
    logging.info('------------------------------------------')
    try:
        input_file  = argv[0]
        output_file = argv[1]
    except Exception as e:
        logging.info('[-] Error!')
        logging.info('[-] Usage: run.py <input_file.nc> <output_file.nc>')
        logging.info('[-] Message: %s' % e)

    if input_file is not None and output_file is not None:
        logging.info('[+] Starting...')
        logging.info('[+] NetCDF input:    %s' % input_file)
        logging.info('[+] NetCDF output:   %s' % output_file)
        print '[+] Starting...'
        print '[i] NetCDF input:    %s' % input_file
        print '[i] NetCDF output:   %s' % output_file
        print '[i] Logfile:         %s' % LOGFILE_NAME

        # instantiate the DC
        dc = DC()

        # get the input file
        dc.from_ncdf(input_file)

        # compile and return the ncdf
        dc.to_ncdf(output_file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=LOGFILE_NAME, \
        filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    main(sys.argv[1:])
