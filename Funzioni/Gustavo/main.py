#!/usr/bin/env python

import functions
from metafile import Metafile


ESUN = (1969.0, 1840.0, 1551.0, 1044.0, 225.7, 1.0, 82.07)


def main():
    metafile_path = ...
    metafile = Metafile(metafile_path)

    sun_elevation_angle = metafile.sun_elevation_angle
    day_of_year = metafile.day_of_year
    spectral_radiance = metafile.spectral_radiance
    dr = functions.relative_earth_sun_distance(day_of_year)

    for esun in ESUN:
        refl = functions.reflectivity(L=spectral_radiance,
                                      esun=esun,
                                      theta=sun_elevation_angle,
                                      dr=dr)
        print(refl)


if __name__ == '__main__':
    main()
