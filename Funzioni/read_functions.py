## read_doy


import linecache

def read_doy(basename):

    #abro o .txt
    metadata_filename = basename + "_ANG.txt"
    metadata = open(metadata_filename, "r")

    #leio a linha com a data de acquisicao dos dados
    doyLine = linecache.getline(metadata_filename, 28)

    #puxo o dia do ano (Day Of Year) e converto em inteiro:
    doyLine = doyLine.replace("  EPHEMERIS_EPOCH_DAY = ", "")
    doyLine = doyLine.replace("\n", "")
    DOY = int(doyLine)

    return DOY



## read_sol_elev-angle


import linecache

def read_sol_elev_angle(basename):

    metadata_filename = basename + "_MTL.txt"
    metadata = open(metadata_filename, "r")
    betaLine = linecache.getline(metadata_filename, 67)
    betaLine = betaLine.replace("    SUN_ELEVATION = ", "")
    betaLine = betaLine.replace("\n", "")
    beta = float(betaLine)
    return beta



## read_gain

# Um jeito (bom, ruim?) e' retornar uma lista:

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

#Exemplo:
#>>>gain = read_gain(landsat_dir_path)
#>>>gain
#[None, 'H', 'H', 'H', 'H', 'H']

# Outro jeito (melhor, pior?) e' retornar somente um valor:

def read_gain(basename, n):

    metadata_filename = basename + "_MTL.txt"
    gain_line = linecache.getline(metadata_filename, 160 + n)
    gain_line = gain_line.replace("    GAIN_BAND_", "")
    gain_line = gain_line.replace(str(i+1) + " = \"", "")
    gain_line = gain_line.replace("\"\n", "")

    return gain_line

#Exemplo:
#gain = [None]
#for i in range(0, 5):
#    gain.append(read_gain(landsat_dir_name, i))
