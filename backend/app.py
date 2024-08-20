from flask import Flask, request, jsonify
import netCDF4 as nc
import numpy as np
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the NetCDF file
dataset = nc.Dataset('../data/x.nc')

# Extract latitude, longitude, and elevation data from the NetCDF file
latitudes = dataset.variables['lat'][:]
longitudes = dataset.variables['lon'][:]
elevations = dataset.variables['elevation'][:]

@app.route('/data', methods=['GET'])
def get_data():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))

        # Find the closest index in the latitude and longitude arrays
        lat_idx = np.abs(latitudes - lat).argmin()
        lon_idx = np.abs(longitudes - lon).argmin()

        # Retrieve the corresponding elevation value
        elevation = elevations[lat_idx, lon_idx]

        return jsonify({
            'latitude': lat,
            'longitude': lon,
            'elevation': float(elevation)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Please click on a region with data available (Indian Ocean region).'
        }), 400


if __name__ == '__main__':
    app.run(debug=True)
