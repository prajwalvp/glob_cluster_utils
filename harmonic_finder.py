import sys
import glob
import subprocess



"""
This script takes in an input period and par file path and prints out ratios and reciprocal ratios
"""

def get_psr_details(par):
    """
    Get all pulsar details
    """         
    psr_name = subprocess.check_output("grep 'PSR' {} | awk '{{print $2}}'".format(par), shell=True).decode('utf-8').split('\n')[0]
    psr_dm  = subprocess.check_output("grep 'DM' {} | awk '{{print $2}}'".format(par), shell=True).decode('utf-8').split('\n')[0]
    psr_f0  = subprocess.check_output("grep 'F0' {} | awk '{{print $2}}'".format(par), shell=True).decode('utf-8').split('\n')[0]
    
    return psr_name, psr_dm, psr_f0


if __name__ == "__main__":
    period = float(sys.argv[2]) # Input in ms
    spin_freq = 1000.0/period

    for par in sorted(glob.glob(sys.argv[1]+'/*.par')):
        psr_name, psr_dm, psr_f0 = get_psr_details(par)   
        #if float(psr_dm) < 237.28 or float(psr_dm) > 239.28:
        #    continue 
        print("{} {}  {} {}".format(psr_name, psr_dm, spin_freq/float(psr_f0), float(psr_f0)/spin_freq))

