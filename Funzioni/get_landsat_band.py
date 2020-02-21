#Opzione uno: ritorna soltanto il cammino completo del file

def get_landsat_band(dirPath, bandNum):

        import os

        bandName = os.path.basename(dirPath) + "_B" + bandNum + ".TIF"
        bandPath = dirPath + "/" + bandName
        
        return bandPath
        
#Opzione due: ritorna sia il cammino sia il nome del file, come dizionario:

def get_landsat_band(dirPath, bandNum):

        import os

        bandName = os.path.basename(dirPath) + "_B" + bandNum + ".TIF"
        bandPath = dirPath + "/" + bandName
        
        return {'fileName': bandName, 'filePath': bandPath}
