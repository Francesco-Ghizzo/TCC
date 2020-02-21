from qgis.core import *
from PyQt4.QtGui import QInputDialog
import os
from osgeo import gdal


# Abro uma janela de input e peco o caminho da pasta com as imagens landsat

def get_landsat_dir():

    landsat_dir = QInputDialog.getText(None, '', 'Insira o caminho da pasta com as imagens Landsat:\n')[0]
    return landsat_dir


# Descubro o nome do file da i-esima banda a partir do caminho da pasta
# Retorno um diciona'rio com o nome do file da imagem tif (fileName) e o caminho completo do file (fullPath)

def get_landsat_bands(dirPath, bandNum):
    
    bandStr = str(bandNum)
    imageName = os.path.basename(dirPath) + "_B" + bandStr + ".TIF"
    imagePath = dirPath + "/" + imageName
    imageDict = {'fileName': imageName, 'fullPath': imagePath}
    return imageDict


# Carrego a i-esima banda como raster e a retorno como uma matriz nume'rica a partir de uma lista de diciona'rios.
# A primeira entrada de cada diciona'rio e' o nome da imagem e a segunda e' o caminho completo
 
def load_raster(landsat_images, bandNum):

    input_dataset = gdal.Open(landsat_images[bandNum]['fileName'])
    if input_dataset is None:
        print "layer " + str(bandNum) + " failed to load"
    else:
        print "layer " + str(bandNum) + " loaded"
    input_band = input_dataset.GetRasterBand(1)
    input_data = input_band.ReadAsArray()
    return input_data


# Peco o caminho da pasta com as imagens landsat e me movo dentro dela:

landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

# Crio uma lista de diciona'rios com o nome e o caminho completo de cada imagem landsat.
# O primeiro lugar na lista e' vazio; os outros (n) sao ocupados pela n-sima banda landsat

landsat_bands = [None]
for i in range(1, 6):
    bandDict = get_landsat_bands(landsat_dir_path, i)
    landsat_bands.append(bandDict)

# Carrego os rasters como matrizes nume'ricas sobre as quais vou poder fazer os ca'lculos de algebra de mapas

for i in range(1, 6):
    input_array = load_raster(landsat_bands, i)
