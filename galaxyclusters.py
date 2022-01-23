import os
import csv
import math
import json
import pprint
import numpy as np
import pandas as pd

# Cosmological Model Used: WMAP5
# H0=71
# Omega_lambda = 0.73
# Omega_M = 0.27
# Omega_R = 0.0
# Omega_K = 0.0

# Data Visualization is done in a Python Jupyter-Notebook

def create_cluster_data_array(csv_data_fname):
    """Create a numpy data array given a csv data filename"""
    data_array_str = []
    # Row 1 and 2 are table headers
    with open(csv_data_fname, newline='') as csvfile: 
        data = csv.reader(csvfile)
        for row in data: 
            data_array_str.append(row)
    header = [data_array_str[0], data_array_str[1]]
    data_array = np.array(data_array_str[2:]).astype(np.float64)
    return header, data_array


def compute_galaxies_physical_size(data_z_Da_Ho71, header, data_galaxies):
    """Compute the galaxies physical size and return this parameter 
    appended on the previously existing galaxy data"""
    new_data_galaxies = []
    for data_galaxy in data_galaxies:
        # Get the Angular Distance for a specific Redshift (z)
        # (from Table Data of AG)
        data_galaxy = list(data_galaxy)
        z_from_galaxy = data_galaxy[3]
        Da = 0.0
        for z_Da in data_z_Da_Ho71:
            if z_Da[0] > z_from_galaxy:
                break
            Da = z_Da[1]
        if Da == 0.0:
            raise Exception("Angular Distance to Galaxy cannot be 0")
        # Galaxies half-light radius (effective angular radius) [arcsec]
        deVRad_r = data_galaxy[2]
        # angular diameter of the galaxies [radians] 
        theta = 2 * deVRad_r * (1/3600.0) * (math.pi / 180.0)
        # d: Physical Size (Diameter) of the Galaxy [kpc]
        d = theta * Da * 1000
        theta = round(theta, 10)
        d = round(d, 5)
        # Append to Galaxy data
        data_galaxy.append(Da)
        data_galaxy.append(theta)
        data_galaxy.append(d)
        new_data_galaxies.append(data_galaxy)
    header[1].append("Da [Mpc]")
    header[1].append("theta [rad]")
    header[1].append("d [kpc]")
    return header[1], new_data_galaxies


def compute_galaxies_size(z_Da_Ho71_fname, 
                          clusters_and_field_galaxies_fnames):
    """Compute galaxies size and return a python dictionary with all 
    galaxies data, organized by cluster(s) and/or field galaxies"""
    # Create empty dictionary
    galaxies_by_cluster_or_field_dict = {}

    # Loading data
    # Angular_Distance = f(Redshift) for WMAP5 -> Ho ~ 71
    csv_data_fname = "z_Da_WMAP5.csv"
    header_z_Da, data_z_Da_Ho71 = create_cluster_data_array(csv_data_fname)
    
    # Loading clusters and field galaxies data
    # Process Da (angular distance[Mpc]) and d (physical size [kpc]) 
    #   cluster and field galaxies data
    # Store in Python dictionary and return it
    for csv_data_fname in (clusters_and_field_galaxies_fnames):
        header_key = "header_" + os.path.splitext(csv_data_fname)[0]
        data_key = "data_" + os.path.splitext(csv_data_fname)[0]
            
        (header_galaxies_by_cluster_or_field, 
         data_galaxies_by_cluster_or_field) = create_cluster_data_array(
            csv_data_fname)
        header_galaxies, data_galaxies = compute_galaxies_physical_size(
            data_z_Da_Ho71, 
            header_galaxies_by_cluster_or_field, 
            data_galaxies_by_cluster_or_field)    
        galaxies_by_cluster_or_field_dict.update(
            {header_key: header_galaxies, data_key: data_galaxies})
       
    return galaxies_by_cluster_or_field_dict
        
    
def store_to_json_file(galaxies_dict, galaxies_json_fname):
    with open(galaxies_json_fname, "w") as galaxies_file:
        json.dump(galaxies_dict, galaxies_file)
        

if __name__ == "__main__":

    # File Names
    z_Da_Ho71_fname = "data_cosmoWMAP_AG1.csv"
    clusters_and_field_galaxies_fnames = ["field.csv", 
        "virgo.csv", "coma.csv", "abell85.csv"]

    # Extract data, process it and store it on a python dictionary
    galaxies_by_cluster_and_field_dict = compute_galaxies_size(
        z_Da_Ho71_fname, clusters_and_field_galaxies_fnames)

    # Prints (optional)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(galaxies_by_cluster_and_field_dict)

    # Store to JSON file
    store_to_json_file(galaxies_by_cluster_and_field_dict,
                       "cluster_and_field_galaxies_data.json")



