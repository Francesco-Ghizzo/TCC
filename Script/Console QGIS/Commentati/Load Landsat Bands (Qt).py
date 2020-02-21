from qgis.core import *


# Apro una finestra di input e chiedo il cammino della cartella

def get_landsat_dir():

    from PyQt4.QtGui import QInputDialog
    landsat_dir = QInputDialog.getText(None, '', 'Insira o caminho da pasta com as imagens Landsat:\n')[0]
    return landsat_dir


# Genero il nome del file dell’n-sima banda a partire dal cammino della cartella

def get_landsat_band(dirPath, bandNum):

    import os
    bandName = os.path.basename(dirPath) + "_B" + bandNum + ".TIF"
    bandPath = dirPath + "/" + bandName        
    return bandPath


# Carico la banda come raster a partire dal cammino del file

def load_raster(filePath):

    from PyQt4.QtCore import QFileInfo
    fileInfo = QFileInfo(filePath)
    fileName = fileInfo.baseName()
    raster_layer = QgsRasterLayer(filePath, fileName)
    if not raster_layer.isValid():
        print "Layer failed to load!"
    else:
        QgsMapLayerRegistry.instance().addMapLayer(raster_layer)
        print "Layer loaded succesfully"
    return


# Esempio: carico tutte le bande landsat da 1 a 7:

landsat_dir_path = get_landsat_dir()
for band in range(1, 8):
    bandStr = str(band)
    load_raster(get_landsat_band(landsat_dir_path, bandStr))

	
#! Il metodo .basename e' applicato due volte: linea 16 e linea 26 (bandName e fileName hanno lo stesso valore).
#! Soluzione: -> far ritornare un dizionario?
#! 
#! Importare moduli e/o librerie dentro una funzione: e’ sbagliato? Poco efficiente? Poco elegante?
#! Meglio importare tutto all’inizio del codice?
