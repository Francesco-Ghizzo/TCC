## Spectral Radiance (L) landsat 7

from qgis.core import *
from PyQt4.QtGui import QInputDialog
import os
import linecache
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


def read_gain(basename):

    metadata_filename = basename + "_MTL.txt"
    gain_list = [None]
    
    for i in range(0, 5):
        gain_line = linecache.getline(metadata_filename, 160 + i)
        gain_line = gain_line.replace("    GAIN_BAND_", "")
        gain_line = gain_line.replace(str(i+1) + " = \"", "")
        gain_line = gain_line.replace("\"\n", "")
        gain_list.append(gain_line)
        
    return gain_list


def spectral_radiance(Gain, bandNum, DN):
    
    LMIN = {'L': (-6.20, -6.40, -5.00, - 5.10, -1.00, 0.00, -0.35, -0.47),
            'H': (-6.20, -6.40, -5.00, - 5.10, -1.00, 3.20, -0.35, -4.7)}
    LMAX = {'L': (293.70, 300.90, 234.40, 241.10, 47.57, 17.04, 16.54, 243.10),
            'H': (191.60, 196.50, 152.90, 157.40, 31.06, 12.65, 10.80, 158.30)}
    
    L = ((LMAX[Gain[bandNum]][bandNum-1] - LMIN[Gain[bandNum]][bandNum-1])/255)*(DN) + LMIN[Gain[bandNum]][bandNum-1]
    return L



landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

landsat_dir_name = os.path.basename(landsat_dir_path)
gain = read_gain(landsat_dir_name)
if gain is "" or None:
    print "failed do load metadata"
else:
    print "metadata loaded"

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
    output_band.WriteArray(spectral_radiance(gain, i, input_data))
#   if  ?
#        print "failed to write to output layer " + str(i)
#    else:
#        print "output layer " + str(i) + " written"
    
    output_dataset.FlushCache()
