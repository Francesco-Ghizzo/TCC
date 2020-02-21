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

# Peco o caminho da pasta com as imagens landsat e me movo dentro dela:
landsat_dir_path = get_landsat_dir()
os.chdir(landsat_dir_path)

# Crio uma lista de diciona'rios com o nome e o caminho completo de cada imagem landsat.
# O primeiro lugar na lista e' vazio; os outros (n) sao ocupados pela n-sima banda landsat
landsat_bands = [None]
for i in range(1, 6):
    bandDict = get_landsat_band(landsat_dir_path, i)
    landsat_bands.append(bandDict)

for i in range(1, 6):

# Abro a i-esima imagem com gdal e crio o objeto input_dataset:
    input_dataset = gdal.Open(landsat_bands[i]['fileName'])
# Retorno um erro em caso de falha:
    if input_dataset is None:
        print "layer " + str(i) + " failed to load"
    else:
        print "layer " + str(i) + " loaded"
# Crio o objeto input_band abrindo o input_dataset como raster:
    input_band = input_dataset.GetRasterBand(1)
# Crio um objeto output_dataset com as mesmas caracteristicas da imagem de entrada input_band
# e a mesma projecao de input_dataset:
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_filename = "Spectral Radiance_B" + str(i) + ".TIF"
    output_dataset = gtiff_driver.Create(output_filename, input_band.XSize,
                                         input_band.YSize, 1, input_band.DataType)
    output_dataset.SetProjection(input_dataset.GetProjection())
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
# Retorno uma mensagem de erro se output_dataset nao foi criado:
    if output_dataset is None:
        print "failed to create output layer " + str(i)
    else:
        print "output layer " + str(i) + " created"
# Uso o metodo ReadAsArray para ler o objeto input_data como uma matriz de valores inteiros de 0 a 255 (8 bits):
# (ou seja, os valores digitais dos pixels)
    input_data = input_band.ReadAsArray()
# Crio um objeto output_band, abrindo a imagem output_dataset como raster:
    output_band = output_dataset.GetRasterBand(1)
    
# Uso o metodo WriteArray para escrever, ponto a ponto, o resultado da funcao spectral_radiance,
# tendo como valores de entrada os valores digitais dos pixels:
    output_band.WriteArray(spectral_radiance(i, input_data))
# ? Nao sei como retornar um erro se o metodo WriteArray falhar. Sera que e' retornada alguma mensagem de erro?
# Talvez:
#   check_err =  output_band.WriteArray(spectral_radiance(i, input_data))
#   if  check_err == valor retornado quando da zebra
#        print "failed to write to output layer " + str(i)
#    else:
#        print "output layer " + str(i) + " written"

# Por fim, limpo a cache:
    output_dataset.FlushCache()
