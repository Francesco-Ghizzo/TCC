## Spectral Radiance (L) landsat 5


from qgis.core import *
from PyQt4.QtGui import QInputDialog
import os
from osgeo import gdal


def get_landsat_dir():

    landsat_dir = QInputDialog.getText(None, '',
                                       'Insira o caminho da pasta com as imagens Landsat 5:\n')[0]
    return landsat_dir

def get_landsat_band(dirPath, bandNum):
    
    bandStr = str(bandNum)
    imageName = os.path.basename(dirPath) + "_B" + bandStr + ".TIF"
    imagePath = dirPath + "/" + imageName
    imageDict = {'fileName': imageName, 'fullPath': imagePath}
    return imageDict    

def spectral_radiance(bandNum, DN):
    
    LMIN = (-1.765,  -3.576,  -1.502,  -1.763,  -0.411,  1.238,  -0.137)
    LMAX = (178.941, 379.055, 255.695, 242,303, 30.178,  15.600, 13.156)

    L = ((LMAX[bandNum-1] - LMIN[bandNum-1])/255)*(DN) + LMIN[bandNum-1]
    return L


landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

landsat_bands = [None]
for i in range(1, 8):
    bandDict = get_landsat_band(landsat_dir_path, i)
    landsat_bands.append(bandDict)

for i in range(1, 8):
    input_dataset = gdal.Open(landsat_bands[i]['fileName'])
    if input_dataset is None:
        print "layer " + str(i) + " failed to load"
    else:
        print "layer " + str(i) + " loaded"
    input_band = input_dataset.GetRasterBand(1)
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_filename = "Spectral Radiance_B" + str(i) + ".TIF"
    output_dataset = gtiff_driver.Create(output_filename, input_band.XSize,
                                         input_band.YSize, 1, input_band.DataType)
    output_dataset.SetProjection(input_dataset.GetProjection())
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    if output_dataset is None:
        print "failed to create output layer " + str(i)
    else:
        print "output layer " + str(i) + " created"
    
    input_data = input_band.ReadAsArray()
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(spectral_radiance(i, input_data))
#   if  ?
#        print "failed to write to output layer " + str(i)
#    else:
#        print "output layer " + str(i) + " written"
    
    output_dataset.FlushCache()
