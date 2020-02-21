## Albedo (alfa) landsat 5


import os
import linecache
import math
import re
from osgeo import gdal
import numpy as np


def get_landsat_bands(dirPath, bandNum):
    
    bandStr = str(bandNum)
    imageName = os.path.basename(dirPath) + "_B" + bandStr + ".TIF"
    imagePath = dirPath + "/" + imageName
    imageDict = {'fileName': imageName, 'fullPath': imagePath}
    return imageDict    


def read_doy(basename):

    metadata_filename = basename + "_ANG.txt"
    metadata = open(metadata_filename, "r")

    doyLine = linecache.getline(metadata_filename, 28)
    DOY = int(filter(str.isdigit, doyLine))
    return DOY


def read_top_left(basename):
    
    metadata_filename = basename + "_ANG.txt"
    metadata = open(metadata_filename, "r")
    UL_line = linecache.getline(metadata_filename, 21)
    return re.findall(r'[-+]?\d*\.\d+|\d+', UL_line)

def read_sol_elev_angle(basename):

    metadata_filename = basename + "_MTL.txt"
    metadata = open(metadata_filename, "r")
    betaLine = linecache.getline(metadata_filename, 67)
    beta = re.findall(r'[-+]?\d*\.\d+|\d+', betaLine)
    return float(beta[0])

def spectral_radiance(bandNum, DN):
    
    LMIN = (-1.765,  -3.576,  -1.502,  -1.763,  -0.411,  1.238,  -0.137)
    LMAX = (178.941, 379.055, 255.695, 242,303, 30.178,  15.600, 13.156)

    L = ((LMAX[bandNum-1] - LMIN[bandNum-1]) / 255) * np.array(DN) + LMIN[bandNum-1]
    return L


def reflectivity(bandNum, DOY, beta, L):

    ESUN = ( 1957.0, 1829.0, 1557.0, 1047.0, 219.3, 1.0, 74.52 )

    theta = ((math.pi/2) - math.radians(beta))
    cos_theta = math.cos(theta)

    dr = 1 + 0.033*(math.cos(DOY*2*math.pi/365))

    rho = (math.pi*np.array(L)) / (ESUN[bandNum - 1]*cos_theta*dr)
    
    return rho


def alfa_toa(a_toa, n, rho):

    omega_lambda = (0.293, 0.274, 0.233, 0.157, 0.033, 0, 0.011)
    a_toa = np.array(a_toa) + omega_lambda[n-1]*np.array(rho)
    return a_toa


def alfa(a_toa, z):

    tau_sw = 0.75 + 2*z*10**(-5)
    a_path_rad = 0.03
    a = ( np.array(a_toa) - a_path_rad) / ( tau_sw**2 )
    return a


landsat_dir_path = raw_input('Insira o caminho da pasta com as imagens Landsat 5:\n')
os.chdir(landsat_dir_path)
alt_est = input('Altitude da estacao:\n')

landsat_dir_name = os.path.basename(landsat_dir_path)
try:
    doy = read_doy(landsat_dir_name)
    top_left_x = float(read_top_left(landsat_dir_name)[0])
    top_left_y = float(read_top_left(landsat_dir_name)[1])
    print "metadata (1/2) loaded"
except:
    print "failed do load _ANG.txt metadata"
try:
    sol_elev_angle = read_sol_elev_angle(landsat_dir_name)
    print "metadata (2/2) loaded"
except:
    print "failed do load _MTL.txt metadata"

landsat_bands = [None]

for i in range(1,8):
    bandDict = get_landsat_bands(landsat_dir_path, i)
    landsat_bands.append(bandDict)

try:
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_filename = "ALBEDO.TIF"
    output_dataset = gtiff_driver.Create( output_filename, 8021, 7061, 1, gdal.GDT_Byte )
    print "output layer created"
except:
    print "failed to create output layer"

    
output_dataset.SetProjection('UTM')
output_dataset.SetGeoTransform( [ top_left_x, 30, 0, top_left_y, 0, -30 ] )
output_band = output_dataset.GetRasterBand(1)
output_data = output_band.ReadAsArray()
albedo_toa = output_data

bands_range = (1, 2, 3, 4, 5, 7)
for i in bands_range:
    try:
        input_dataset = gdal.Open(landsat_bands[i]['fileName'])
        input_band = input_dataset.GetRasterBand(1)
        input_data = input_band.ReadAsArray()
        print "landsat band " + str(i) + " loaded"
    except: 
        print "landsat band " + str(i) + " failed to load"

    try:
        radiance = spectral_radiance(i, input_data)
        print "spectral radiance for landsat band " + str(i) + " calculated"
    except:
        print "failed to calculate spectral radiance for landsat band " + str(i)
    try:
        ro = reflectivity(i, doy, sol_elev_angle, radiance)
        print "reflectivity for landsat band " + str(i) + " calculated"
    except:
        print "failed to calculate reflectivity for landsat band " + str(i)
    try:
        albedo_toa = alfa_toa(albedo_toa, i, ro)
        print "albedo at the top of the atmosphere for landsat band " + str(i) + " calculated"
    except:
        print "failed to calculate albedo at the top of the atmosphere for landsat band " + str(i)
    
albedo = alfa(albedo_toa, alt_est)
    
try :
    output_band.WriteArray(albedo*100)
    output_dataset.FlushCache()
    print "output layer written"
except:
    print "failed to write to output layer"
    
