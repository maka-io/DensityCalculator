#!/usr/bin/env python
'''
Created: 07/14/2015
Updated: 07/18/2015

DensityCalculator.py will use a netCDF input file with x and y data
points and apply a Gaussian KDE algorithm to the dataset.
The output is a netCDF file where z is the dependent density value,
and x/y are it's independent locations.
'''

__author__ = "M@Campbell"

import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import netCDF4
import copy
import datetime
import logging

class DensityCalc(object):
    # setup containers
    tx = []
    ty = []

    GRID_SIZE = 9500

    def __init__(self):
        object.__init__(self)


    def from_ncdf(self, ncdf_file):
        '''
        DensityCalc.fro_ncdf(<file_name.nc>)

        ncdf_file:  location of the input NetCDF file

        Input file should contain 'x' and a 'y' variables
        '''
        nc = None
        try:
            # attempt to open the netcdf file.
            nc = netCDF4.Dataset(ncdf_file)
            self.tx = copy.deepcopy(nc.variables['x'][:])
            self.ty = copy.deepcopy(nc.variables['y'][:])
            logging.info('[i] size of data set is: %s' % len(self.tx))
        except:
            raise
        finally:
            if nc is not None:
                nc.close()

    def to_ncdf(self, ncdf_file):
        '''
        DensityCalc.to_ncdf(output)

        Runs the KDE algorithm, creates the netCDF file and writes the data
        to it.

        '''
        try:
            logging.info('[*] Running, please wait...')
            print '[+] Time: %s' % datetime.datetime.now()
            print '[*] Running, please wait...'
            ## This is where one may choose a different
            ## density calculation:
            # ----------------------------------- #
            (x,y,z) = self._kde(self.tx, self.ty)
            # ----------------------------------- #

            print '[+] Complete!'
            print '[+] Time: %s' % datetime.datetime.now()
            logging.info('[+] Complete!')
        except:
            print '[-] Please ensure input file path is correct, and readable.'
            raise
        finally:
            pass

        logging.info('[*] Creating NetCDF File...')

        # create the file and add some history info
        nc_file_out = netCDF4.Dataset(ncdf_file,'w', format='NETCDF4')

        try:
            nc_file_out.history = "Created on: %s " % datetime.datetime.now()

            # create the dimentions for the variables
            nc_file_out.createDimension('y' ,y.shape[1])
            nc_file_out.createDimension('x',x.shape[0])

            # create the variables themselves
            lats = nc_file_out.createVariable('y','d',('y'))
            lons = nc_file_out.createVariable('x','d',('x'))
            data = nc_file_out.createVariable('density','f8', ('x','y'))

            # define some meta data
            lats.units = 'Meters'
            lats.standard_name = "projection_y_coordinate"
            lats.long_name = "y coordinate of projection"

            lons.units = 'Meters'
            lons.standard_name = "projection_x_coordinate"
            lons.long_name = "x coordinate of projection"

            data.units = 'percent'
            data.grid_mapping = 'albers_conical_equal_area'
            data.coordinates = 'x y'

            # store the data to the variables

            lats[:] = y[0,:]
            lons[:] = x[:,0]
            data[:] = z

            logging.info('[+] NetCDF File created!')
            logging.info('[i] %s' % ncdf_file)
        except Exception as e:
            logging.info('[-] Error saving data to netcdf!')
            logging.info('[-] Message: %s' % e)
        finally:
            nc_file_out.close()

        return

    def _kde(self,tx=tx, ty=ty, grid_size=GRID_SIZE):
        '''
        DensityCalc._kde(tx,ty,grid_size)

            tx:         X axis variable. Defaults to 'x'
            ty:         Y axis variable. Defaults to 'y'
            grid_size:  In meters

        Usage:
            dc = DensityCalc('path/to/netcdf_file.nc')
            x, y, z = dc.kde(<tx>, <ty>, <grid_size>)
        '''
        try:
            bounds = (np.amin(tx),np.amin(ty),np.amax(tx),np.amax(ty))

            ## evaluate the estimated PDF on a grid
            x,y = np.mgrid[
                bounds[0]:bounds[2]:grid_size,
                bounds[1]:bounds[3]:grid_size
            ]

            positions = np.vstack([x.ravel(), y.ravel()])

            values = np.vstack([tx, ty])

            ## calculate the density
            kernel = gaussian_kde(values)

            ## suggested to only use these when absolutly certain.
            ## default is scotts_factor: power(self.n, -1./(self.d+4))
            #kernel.covariance_factor = lambda: .337
            #kernel._compute_covariance()

            z = np.reshape(kernel(positions).T, x.shape)*grid_size*grid_size

            ##Scale the data to between 0-1, while preserving ratio
            old_range = (z.max() - z.min())
            new_range = (1 - 0)
            z_scaled = (((z - z.min()) * new_range) / old_range) + 0

            tuple_return = (x,y,z_scaled)
            return tuple_return
        except:
            print '[-] Time: %s' % datetime.datetime.now()
            raise
