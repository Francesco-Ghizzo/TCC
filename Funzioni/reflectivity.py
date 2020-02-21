## rho: Reflectivity (ratio of the reflected radiation flux to the incident radiation flux)
## DOY: Day Of Year (sequential day of the year)
## beta: sun elevation angle
## theta: solar incidence angle (= 90 - beta)
## dr: inversed squared relative earth sun distance
## ( dr = 1/(d_es^2), where d_es is the relative distance between the earth and the sun )



## landsat 5:

def reflectivity(bandNum, DOY, beta, L):

    ESUN = ( 1957.0, 1829.0, 1557.0, 1047.0, 219.3, 1.0, 74.52 )
    
# Calculo o cosseno de theta:

    theta = ((math.pi/2) - math.radians(beta))
    cos_theta = math.cos(theta)

# Calculo a distancia relativa Terra Sol:

    dr = 1 + 0.033*(math.cos(DOY*2*math.pi/365))

# Calculo a reflectividade:

    rho = (math.pi*L) / (ESUN[bandNum - 1]*cos_theta*dr)
    
    return rho



## landsat 7:

def reflectivity(bandNum, DOY, beta, L):

    ESUN = ( 1969.0, 1840.0, 1551.0, 1044.0, 225.7, 1.0, 82.07 )
    
# Calculo o cosseno de theta:

    theta = ((math.pi/2) - math.radians(beta))
    cos_theta = math.cos(theta)

# Calculo a distancia relativa Terra Sol:

    dr = 1 + 0.033*(math.cos(DOY*2*math.pi/365))

# Calculo a reflectividade:

    rho = (math.pi*L) / (ESUN[bandNum - 1]*cos_theta*dr)
    
    return rho
