import os
import json
import optparse
import pandas as pd
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord



"""
This script reports closest beams in meta file w.r.t. reference beam. Also gives option to find closest beams in another meta file. 

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



def get_reference_beam_coords(opts):
    with open(opts.meta_path,'r') as f:
        all_info = json.load(f)

    ref_beam_ra = all_info['beams'][opts.ref_beam].split(', ')[-2]
    ref_beam_dec = all_info['beams'][opts.ref_beam].split(', ')[-1]

    ref_beam_coords = SkyCoord(frame='icrs', ra=ref_beam_ra, dec=ref_beam_dec, unit=(u.hour, u.deg)) 

    return ref_beam_coords



def find_neighbours(opts):

    ref_beam_coords = get_reference_beam_coords(opts)
    coherent_beam_coords = get_coherent_beam_coords(opts.meta_path)
 
    all_seps = ref_beam_coords.separation(coherent_beam_coords)
    all_beams_sorted = np.argsort(all_seps)
    neighbour_beam_list = all_beams_sorted[1:min(11, len(all_beams_sorted))]
    print('Neighbouring beams are..')
    for i, beam_num in enumerate(neighbour_beam_list):
        print('cfbf00{:03d}, {}'.format(beam_num, sorted(all_seps)[i+1].deg))


    if os.path.exists(opts.meta_path2):
        coherent_beam_coords2 = get_coherent_beam_coords(opts.meta_path2)
        all_seps2 = ref_beam_coords.separation(coherent_beam_coords2)
        all_beams_sorted2 = np.argsort(all_seps2)
        neighbour_beam_list = all_beams_sorted2[0:min(11, len(all_beams_sorted))]
        print('Neighbouring beams from different epoch ({}) are..'.format(opts.meta_path2))
        for i, beam_num in enumerate(neighbour_beam_list):
            print('cfbf00{:03d}, {}'.format(beam_num, sorted(all_seps2)[i].deg))

        



if __name__=='__main__':
    # Select options
    parser = optparse.OptionParser()
    parser.add_option('--meta_path',type=str, help= 'Path to meta file',dest='meta_path')
    parser.add_option('--meta_path2',type=str, help= 'Path to another epoch meta file',dest='meta_path2', default='None')
    parser.add_option('--reference_beam',type=str, help= 'Reference beam number',dest='ref_beam', default='cfbf00000')

    opts, args = parser.parse_args()

    
    # Report 10 closest beams and separations
    find_neighbours(opts)
     
 


