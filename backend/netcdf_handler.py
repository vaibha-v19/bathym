import netCDF4 as nc
import numpy as np

def get_data_from_netcdf(lat, lon):
    dataset = nc.Dataset('./data/x.nc', 'r')
    lats = dataset.variables['lat'][:]
    lons = dataset.variables['lon'][:]
    elevation = dataset.variables['elevation'][:]

    # Find the closest indices for the given latitude and longitude
    lat_idx = find_closest_index(lats, lat)
    lon_idx = find_closest_index(lons, lon)

    if lat_idx != -1 and lon_idx != -1:
        elevation_value = elevation[lat_idx, lon_idx]
        return {
            "latitude": lats[lat_idx],
            "longitude": lons[lon_idx],
            "elevation": elevation_value
        }
    else:
        return None

def find_closest_index(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx if np.abs(array[idx] - value) < 1 else -1
