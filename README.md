# glob_cluster_utils
Utlilities for searching and timing pulsars in globular clusters



## beam_strategy.py

Aim: To segregate beams based on core, half-mass, half-light and tidal radius
```
Usage: beam_strategy.py [options]

Options:
  -h, --help            show this help message and exit
  --meta_path=META_PATH
                        Path to meta file
  --gc_name=GC_NAME     Name of globular cluster
  --gc_file=GC_FILE     Name of globular cluster properties file
  --user_radius=RADIUS  User specified radius in deg. Defaults to core, half-
                        light and half mass values derived from the Baumgardt
                        reference
```
Use the *glob_cluster_properties_HB.txt* file as input for `--gc_file`

## harmonic_finder.py

Aim: To check if a candidate is a harmonic of another known pulsar within the globular cluster of interest 

```
Usage: python harmonic_finder.py <path to all known pulsar ephemeris files> <Spin period of candidate (in milliseconds)>
```

## neighbour_finder.py

Aim: Lists the top 10 closest beams w.r.t the reference beam from multiple epochs.

```
Usage: neighbour_finder.py [options]

Options:
  -h, --help            show this help message and exit
  --meta_path=META_PATH
                        Path to meta file
  --meta_path2=META_PATH2
                        Path to another epoch meta file
  --reference_beam=REF_BEAM
                        Reference beam name (cfbfxxxxx)
  --reference_coord=REF_COORDS
                        Reference coordinates
```

