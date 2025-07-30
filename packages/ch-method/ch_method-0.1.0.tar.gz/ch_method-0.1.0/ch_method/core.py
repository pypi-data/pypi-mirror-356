# core.py

import numpy as np
from datetime import datetime
from typing import Tuple

from nrlmsise00 import msise_model

from .constants import G, ME, RE, R_GAS, NA, M_AIR, H_SCALE
from .helpers import find_index, compute_background_noise

def Parameters(
    Photoncounts: np.ndarray,
    Altitude: np.ndarray,
    Initial_alt: float,
    refer_alt: float,
    seed_alt: float,
    location: Tuple[float, float],
    Time: datetime
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    This function utilizes Photoncounts from Reyleigh lidar to derive the temperature and density profiles of the middle atmosphere.
    The primary method is based on the approach proposed by Hauchecorne and Chanin (1980)[1]. 
    [1] Hauchecorne, A., & Chanin, M. L. (1980). Density and temperature profiles obtained by lidar between 35 and 70 km. Geophysical Research Letters, 7(8), 565-568. https://doi.org/10.1029/GL007i008p00565
    
    Parameters:
    Photoncounts (numpy.ndarray): Array of photon count data from the lidar.
    Altitude (numpy.ndarray): Array of altitude values in km corresponding to the photon counts.
    Initial_alt (float): The initial altitude in km for the analysis.
    refer_alt (float): Reference altitude used for density retrieval.
    seed_alt (float): Seed altitude for the temperature retrieval.
    location (tuple): Tuple containing latitude in degrees north and longitude in degrees east (lat, lon) for the NRLMSISE-00 atmospheric model.
    Time (datetime.datetime): Date and time as a 'datetime.datetime' to be used for the NRLMSISE-00 atmospheric model.

    Returns:
    tuple: A tuple containing:
        - temperature (numpy.ndarray): Derived temperature profile in the middle atmosphere [K].
        - density (numpy.ndarray): Derived density profile [kg/m^3].
        - derived_altitude (numpy.ndarray): Altitude values in the derived range [km].
        - relative_density_error (numpy.ndarray): Relative error values for density.
        - absolute_density_error (numpy.ndarray): Absolute error values for density [kg/m^3].
        - absolute_temperature_error (numpy.ndarray): Absolute error values for temperature [K].

    """
    # Input validation
    if Photoncounts.size == 0 or Altitude.size == 0:
        raise ValueError("Photoncounts and Altitude must be non-empty arrays.")
    if Photoncounts.shape != Altitude.shape:
        raise ValueError("Photoncounts and Altitude must have the same shape.")
    if not isinstance(Time, datetime):
        raise TypeError("Time must be a datetime.datetime object.")
    if not (isinstance(location, tuple) and len(location) == 2):
        raise ValueError("Location must be a (lat, lon) tuple.")
    
 # Background noise
    back_noise = compute_background_noise(Photoncounts, Altitude)

    # Reference index and values
    idx_down = find_index(Altitude, Initial_alt)
    idx_up = find_index(Altitude, seed_alt)
    idx_ref = find_index(Altitude, refer_alt)
    ph_ref = Photoncounts[idx_ref]

    # Reference density using NRLMSISE-00
    output1 = msise_model(Time, refer_alt, location[0], location[1], 140, 140, 10)
    reference_density = np.sum(output1[0]) * M_AIR / NA * 1e6

    # Altitude slice
    idx0 = min(idx_down, idx_up)
    idx1 = max(idx_down, idx_up) + 1
    slice_range = slice(idx0, idx1)

    # Density profile retrieval
    alt_squared = np.square(Altitude)
    
    density = reference_density * (
        (Photoncounts - back_noise) / (ph_ref - back_noise)
        * alt_squared / refer_alt**2
    )

    Density = density[slice_range]
    # Gravitational acceleration
    Gravity = G * ME / np.square(RE + Altitude * 1e3)
    delta_z = (Altitude[2] - Altitude[1]) * 1e3  # in meters

    # Reference temperature using NRLMSISE-00
    output2 = msise_model(Time, seed_alt, location[0], location[1], 140, 140, 10)
    reference_temperature = output2[1][1]

    # Temperature profile
    T1 = np.full_like(Photoncounts, np.nan)
    for i in range(idx_up, idx_down - 1, -1):
        slice_i = slice(i, idx_up)
        sum_term = np.nansum(density[slice_i] * Gravity[slice_i])
        T1[i] = (reference_temperature * density[idx_up] +
                  (M_AIR / R_GAS) * delta_z * sum_term) / density[i]

    temperature = T1[slice_range]

    # Error estimation
    ph0 = Photoncounts[slice_range]
    rel_density_err = np.sqrt(ph0) / (ph0 - back_noise)
    abs_density_err = Density * rel_density_err  

    abs_temp_err = np.sqrt(
        (temperature * rel_density_err)**2 +
        (reference_temperature * np.sqrt(ph0[-1]) / (ph0[-1] - back_noise)
         * np.exp(-(refer_alt - Altitude[slice_range]) / H_SCALE))**2
    )

    return temperature, Density, Altitude[slice_range], rel_density_err, abs_density_err, abs_temp_err
