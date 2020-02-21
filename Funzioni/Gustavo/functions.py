#!/usr/bin/env python

import math


__all__ = ['reflectivity', 'relative_earth_sun_distance']


def reflectivity(L, esun, theta, dr):
    rho = (math.pi * L) / (esun * math.sin(theta) * dr)
    return rho


def relative_earth_sun_distance(day_of_year):
    dr = 1 + 0.033 * math.cos(get_day_angle(day_of_year))
    return dr


def get_day_angle(day_of_year):
    return math.radians(360 * day_of_year / 365.0)
