## Reflectivity (ro) landsat 5


from qgis.core import *
from PyQt4.QtGui import QInputDialog
import os
import linecache
import math
from osgeo import gdal


def get_landsat_dir():

    landsat_dir = QInputDialog.getText(None, '',
                                       'Insira o caminho da pasta com as imagens Landsat 5:\n')[0]
    return landsat_dir


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
    doyLine = doyLine.replace("  EPHEMERIS_EPOCH_DAY = ", "")
    doyLine = doyLine.replace("\n", "")
    DOY = int(doyLine)

    return DOY


def read_sol_elev_angle(basename):

    metadata_filename = basename + "_MTL.txt"
    metadata = open(metadata_filename, "r")
    betaLine = linecache.getline(metadata_filename, 67)
    betaLine = betaLine.replace("    SUN_ELEVATION = ", "")
    betaLine = betaLine.replace("\n", "")
    beta = float(betaLine)
    return beta

def spectral_radiance(bandNum, DN):
    
    LMIN = (-1.765,  -3.576,  -1.502,  -1.763,  -0.411,  1.238,  -0.137)
    LMAX = (178.941, 379.055, 255.695, 242,303, 30.178,  15.600, 13.156)

    L = ((LMAX[bandNum-1] - LMIN[bandNum-1]) / 255) * DN + LMIN[bandNum-1]
    return L


def reflectivity(bandNum, DOY, beta, L):

    ESUN = ( 1957.0, 1829.0, 1557.0, 1047.0, 219.3, 1.0, 74.52 )

    theta = ((math.pi/2) - math.radians(beta))
    cos_theta = math.cos(theta)

    dr = 1 + 0.033*(math.cos(DOY*2*math.pi/365))

    rho = (math.pi*L) / (ESUN[bandNum - 1]*cos_theta*dr)
    
    return rho


landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

landsat_dir_name = os.path.basename(landsat_dir_path)
doy = read_doy(landsat_dir_name)
if doy is None:
    print "failed do load _ANG.txt metadata"
else:
    print "metadata (1/2) loaded"
sol_elev_angle = read_sol_elev_angle(landsat_dir_name)
if sol_elev_angle is None:
    print "failed do load _MTL.txt metadata"
else:
    print "metadata (2/2) loaded"

landsat_bands = [None]
for i in range(1, 6):
    bandDict = get_landsat_bands(landsat_dir_path, i)
    landsat_bands.append(bandDict)

for i in range(1, 6):
    input_dataset = gdal.Open(landsat_bands[i]['fileName'])
    if input_dataset is None:
        print "layer " + str(i) + " failed to load"
    else:
        print "layer " + str(i) + " loaded"
    input_band = input_dataset.GetRasterBand(1)
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_filename = "Reflectivity_B" + str(i) + ".TIF"
    output_dataset = gtiff_driver.Create(output_filename, input_band.XSize,
                                         input_band.YSize, 1, input_band.DataType)
    if output_dataset is None:
        print "failed to create output layer " + str(i)
    else:
        print "output layer " + str(i) + " created"
    input_data = input_band.ReadAsArray()
    output_dataset.SetProjection(input_dataset.GetProjection())
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    radiance = spectral_radiance(i, input_data)
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(reflectivity(i, doy, sol_elev_angle, radiance))
#   if  ?
#        print "failed to write to output layer " + str(i)
#    else:
#        print "output layer " + str(i) + " written"
    
    output_dataset.FlushCache()
