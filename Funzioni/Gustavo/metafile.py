#!/usr/bin/env python

import math


__all__ = ['Metafile']


class Metafile(object):
    def __init__(self, filename):
        self._sun_elevation_angle = math.radians(...)
        self._day_of_year = ...
        self._spectral_radiance = ...

    @property
    def sun_elevation_angle(self):
        return self._sun_elevation_angle

    @property
    def day_of_year(self):
        return self._day_of_year

    @property
    def spectral_radiance(self):
        return self._spectral_radiance
