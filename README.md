# GalaxySize

*01/2022 by Marc Rosanes*  
*Licensed under GNU General Public License V3 (GPLv3) or any later version (GPLv3+)*

**Cosmology Project Software**  
GalaxySize has been developed during the Cosmology subject when following the 
Master of Astronomy & Astrophysics at VIU (Valencia International University)  

This project contains a set of Python functions and a Jupyter-Notebook 
for data visualization with the purpose to determine the size of galaxies from different 
galaxy clusters (and/or from field galaxies) thanks to the knowledge of redshifts **z**, 
angular distances **Da** and DeVaucouleurs radius **deVRad_r** (angular radius of the galaxy as 
it is seen from Earth in the Sloan red filter) of the galaxies belonging to each cluster.

**Input files**
- A set of CSV input files that have been created with searches in NED and SDSS SQL:
    - field.csv
    - virgo.csv
    - coma.csv
    - abell85
- The precedent files contain the fields *RA*, *Dec*, and *deVRad_r* and *z* (radius in Sloan red filter) for each galaxy belonging to a given Galaxy Cluster (or being Field Galaxies)  
- z_Da_WMAP5.csv: data table provinding **Da = f(z)**; provided by dra. Beatriz Ruiz during the course of the Cosmology subject at VIU

**The script is executed with:**  
*python galaxyclusters.py*  

**galaxyclusters.py Python script performs:**  
1- Assuming WMAP5, i.e. H0=71 (~70.5), and given a table of Da = f(z), it finds Da associated with the z of each galaxy  
2- It converts deVRad_r in arcsec to an angular diameter **θ** in radians  
3- It computes the size/diametar **d** of each galaxy with: **d = Da·θ**  
4- It stores the results in a Python dictionary, with:  
&nbsp;&nbsp;&nbsp;&nbsp; 4.1- List of galaxies for each cluster and/or list of field galaxies  
&nbsp;&nbsp;&nbsp;&nbsp; 4.2- List of parameters for each galaxy: **z, Da, deVRad_r, θ, d**  
5- It serializes the dictionary using JSON and stores it in a JSON file   

**GalaxyDistancesCosmo.ipynb Jupyter-Notebook performs:**  
1- It loads the JSON files previously created with galaxyclusters.py  
2- It displays 10 galaxies for each cluster with its associated parameters, the final row being the galaxy size in kpc  
3- It displays histograms representing the number of galaxies in function of its size  
4- It computes the mean and the standard deviation of each group of galaxies object (field, specific cluster of galaxies, all)  


