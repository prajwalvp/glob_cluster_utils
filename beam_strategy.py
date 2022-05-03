import optparse
import pandas as pd
import numpy as np
from ast import literal_eval


def get_radius_in_arcmin():
    """
    @
    """

def get_radius_in_degrees():
    """
    
    """



if __name__=='__main__':
    # Select options
    parser = optparse.OptionParser()
    parser.add_option('--meta_path',type=str, help= 'Path to meta file',dest='meta_path')
    parser.add_option('--gc_name',type=str, help='Name of globular cluster',dest='gc_name',default='Ter_5') 
    parser.add_option('--gc_file',type=str, help='Name of globular cluster properties file',dest='gc_file',default='glob_cluster_properties_HB.txt') 
    parser.add_option('--radius_type',type=str, help='Type of radius to use as beam separator (Options are core, half-mass or half-light)',dest='rad_type',default='core') 
    opts, args = parser.parse_args()

    

