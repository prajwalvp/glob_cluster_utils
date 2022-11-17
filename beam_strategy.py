import json
import optparse
import pandas as pd
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, search_around_sky



"""
This script reports beams  within different radii (core, half mass, tidal etc) based on an input reference from Baumgardt 2021. The user can also specify a specific radius.

@inputs:
1. radius (user or from standard reference i.e. Baumgardt)
2. Standard TRAPUM meta file
@outputs: List of beams within the selected radius
"""

def get_coherent_beam_coords(meta):
    """
    Return beam coordinates for all coherent beams
    """     
    with open(meta,'r') as f:
        all_info = json.load(f)
 
    # Get all key value pairs for beams and sort them based on beam number
    vals = list(all_info['beams'].values())
    keys = list(all_info['beams'].keys())
    vals = [x for _, x in sorted(zip(keys,vals))]
    keys = sorted(keys)
   
    
    # Convert beam coordinates into Astropy dataframe
    coherent_beams_ra = [] 
    coherent_beams_dec = [] 

    for i in range(len(vals)):
        if 'unset' in vals[i]:
            continue
        coherent_beams_ra.append(vals[i].split(',')[-2])
        coherent_beams_dec.append(vals[i].split(',')[-1])
    
    # Convert equatorial beam coordinates to pixel coordinates
    beam_coords = SkyCoord(frame='icrs', ra= coherent_beams_ra, dec= coherent_beams_dec, unit=(u.hour, u.deg))

    return beam_coords[:-1]

def get_boresight_coords(meta):
    with open(meta,'r') as f:
        all_info = json.load(f)

    boresight_ra = all_info['boresight'].split(',')[-2]     
    boresight_dec = all_info['boresight'].split(',')[-1]
    boresight_coords = SkyCoord(frame='icrs', ra=boresight_ra, dec=boresight_dec, unit=(u.hour, u.deg)) 

    return boresight_coords


def derive_from_user(opts):

    print(opts.meta_path)

def derive_values(opts, data):    
    D = float(data[data['Cluster'] == opts.gc_name]['R_Sun'])
    r_c = float(data[data['Cluster'] == opts.gc_name]['rc'])
    r_hl = float(data[data['Cluster'] == opts.gc_name]['rh,l'])
    r_hm = float(data[data['Cluster'] == opts.gc_name]['rh,m'])
    r_t = float(data[data['Cluster'] == opts.gc_name]['rt'])

    r_c_deg = (180/np.pi)*(r_c/(D*1000))
    r_hl_deg = (180/np.pi)*(r_hl/(D*1000))
    r_hm_deg = (180/np.pi)*(r_hm/(D*1000))
    r_t_deg = (180/np.pi)*(r_t/(D*1000))


    beam_coords = get_coherent_beam_coords(opts.meta_path)
    boresight_coords = get_boresight_coords(opts.meta_path)

    rc_beams = []
    r_hl_beams = []
    r_hm_beams = []
    r_t_beams = []

    for i, beam_coord in enumerate(beam_coords):
        d2d = boresight_coords.separation(beam_coord)
        if float(d2d.deg) < r_c_deg:
            rc_beams.append(i)
        if float(d2d.deg) < r_hl_deg:
            r_hl_beams.append(i)
        if float(d2d.deg) < r_hm_deg:
            r_hm_beams.append(i)
        if float(d2d.deg) < r_t_deg:
            r_t_beams.append(i)
  
    
    core_radius_beams = ["cfbf00{:03d}".format(i) for i in rc_beams]      
    hm_radius_beams = ["cfbf00{:03d}".format(i) for i in r_hm_beams]      
    hl_radius_beams = ["cfbf00{:03d}".format(i) for i in r_hl_beams]      
    tidal_radius_beams = ["cfbf00{:03d}".format(i) for i in r_t_beams]      


    print("Beams within the core radius:{}".format(",".join(map(str, core_radius_beams))))   
    print("Beams within the half-mass radius:{}".format(",".join(map(str, hm_radius_beams))))   
    print("Beams within the half-light radius:{}".format(",".join(map(str, hl_radius_beams))))   
    print("Beams within the tidal radius:{}".format(",".join(map(str, tidal_radius_beams))))   
 
    if opts.radius != "default":
        user_beams = [] 
        for i, beam_coord in enumerate(beam_coords):
            d2d = boresight_coords.separation(beam_coord)
            if float(d2d.deg) < float(opts.radius):
                user_beams.append(i)
         

        user_radius_beams = ["cfbf00{:03d}".format(i) for i in user_beams]      
        print("Beams within the user specified radius:{}".format(",".join(map(str, user_radius_beams))))   

if __name__=='__main__':
    # Select options
    parser = optparse.OptionParser()
    parser.add_option('--meta_path',type=str, help= 'Path to meta file',dest='meta_path')
    parser.add_option('--gc_name',type=str, help='Name of globular cluster',dest='gc_name',default='Ter_5') 
    parser.add_option('--gc_file',type=str, help='Name of globular cluster properties file',dest='gc_file',default='glob_cluster_properties_HB.txt') 
    parser.add_option('--user_radius',type=str, help='User specified radius in deg. Defaults to core, half-light and half mass values derived from the Baumgardt reference',dest='radius',default='default') 
    opts, args = parser.parse_args()

    
    # Read in the file
    data = pd.read_csv('glob_cluster_properties_HB.txt', sep='\s+', skiprows=[1]) 


    derive_values(opts, data)

