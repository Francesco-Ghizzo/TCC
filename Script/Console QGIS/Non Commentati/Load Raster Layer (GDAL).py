from qgis.core import *
from PyQt4.QtGui import QInputDialog
import os
from osgeo import gdal


def get_landsat_dir():

    landsat_dir = QInputDialog.getText(None, '', 'Insira o caminho da pasta com as imagens Landsat:\n')[0]                                      
    return landsat_dir


def get_landsat_bands(dirPath, bandNum):
    
    bandStr = str(bandNum)
    imageName = os.path.basename(dirPath) + "_B" + bandStr + ".TIF"
    imagePath = dirPath + "/" + imageName
    imageDict = {'fileName': imageName, 'fullPath': imagePath}
    return imageDict


def load_raster(landsat_images, bandNum):

    input_dataset = gdal.Open(landsat_images[bandNum]['fileName'])
    if input_dataset is None:
        print "layer " + str(bandNum) + " failed to load"
    else:
        print "layer " + str(bandNum) + " loaded"
    input_band = input_dataset.GetRasterBand(1)
    input_data = input_band.ReadAsArray()
    return input_data


landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

landsat_bands = [None]
for i in range(1, 6):
    bandDict = get_landsat_bands(landsat_dir_path, i)
    landsat_bands.append(bandDict)
    
for i in range(1, 6):
    input_array = load_raster(landsat_bands, i)

