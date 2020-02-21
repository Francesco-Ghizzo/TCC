## Albedo (alfa) landsat 5


import os
import linecache
import math
import re
from osgeo import gdal
import numpy as np




def get_landsat_bands(nameBase, bandNum):
    
    bandStr = str(bandNum)
    imageName = nameBase + "_sr_band" + bandStr + ".tif"
    return imageName   


def read_top_left(basename):
    
    metadata_filename = basename + "_ANG.txt"
    metadata = open(metadata_filename, "r")
    UL_line = linecache.getline(metadata_filename, 21)
    return re.findall(r'[-+]?\d*\.\d+|\d+', UL_line)


def alfa(a, n, DN):

    omega_lambda = (0.293, 0.274, 0.233, 0.157, 0.033, 0, 0.011)
    rho = np.array(DN)*0.0001
    a = np.array(a) + omega_lambda[n-1]*np.array(rho)
    return a


landsat_dir_path = raw_input('Insira o caminho da pasta com as imagens Landsat 5:\n')
os.chdir(landsat_dir_path)
baseName = raw_input('Insira o basename:\n')

try:
    top_left_x = float(read_top_left(baseName)[0])
    top_left_y = float(read_top_left(baseName)[1])
    print "metadata (1/2) loaded"
except:
    print "failed do load _ANG.txt metadata"
    
landsat_bands = [None]

for i in range(1,8):
    bandName = get_landsat_bands(baseName, i)
    landsat_bands.append(bandName)

try:
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_filename = "ALBEDO.TIF"
    output_dataset = gtiff_driver.Create( output_filename, 7801,
                                         6891, 1, gdal.GDT_Byte )
    print "output layer created"
except:
    print "failed to create output layer"

    
output_dataset.SetProjection('UTM')
output_dataset.SetGeoTransform( [ top_left_x, 30, 0, top_left_y, 0, -30 ] )
output_band = output_dataset.GetRasterBand(1)
output_data = output_band.ReadAsArray()
albedo = output_data

bands_range = (1, 2, 3, 4, 5, 7)
for i in bands_range:
    try:
        input_dataset = gdal.Open(landsat_bands[i])
        input_band = input_dataset.GetRasterBand(1)
        input_data = input_band.ReadAsArray()
        print "landsat band " + str(i) + " loaded"
    except: 
        print "landsat band " + str(i) + " failed to load"

    try:
        albedo = alfa(albedo, i, input_data)
        print "albedo for landsat band " + str(i) + " calculated"
    except:
        print "failed to calculate albedo for landsat band " + str(i)
    
    
try :
    output_band.WriteArray(albedo*100)
    output_dataset.FlushCache()
    print "output layer written"
except:
    print "failed to write to output layer"
    
