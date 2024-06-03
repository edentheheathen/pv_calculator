import pvlib
import pandas as pd

def retrieve_pvgis_data(latitude, longitude, year, output_file):
    poa_data, meta, input = pvlib.iotools.get_pvgis_hourly(
        latitude=latitude,
        longitude=longitude,
        start=year,
        end=year,
        raddatabase="PVGIS-SARAH2",
        components=True,
        surface_tilt=45,
        surface_azimuth=0,
        outputformat='json',
        usehorizon=True,
        pvcalculation=False,
        trackingtype=0,
        url='https://re.jrc.ec.europa.eu/api/v5_2/',
        map_variables=True,
        timeout=30
    )

    poa_data["poa_diffuse"] = poa_data['poa_sky_diffuse'] + poa_data["poa_ground_diffuse"]
    poa_data["poa_global"] = poa_data["poa_diffuse"] + poa_data["poa_direct"]

    
    poa_data.to_csv(output_file)
    print(f"Data saved to {output_file}")
