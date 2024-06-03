import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt

def run_model_chain(datafile, latitude, longitude, tz, altitude, module, inverter,
                    temp_model, modules_per_string, strings_per_inverter,
                    surface_tilt, surface_azimuth, location_name):
    location = Location(latitude=latitude, longitude=longitude, tz=tz, altitude=altitude, name=location_name)
    temperature_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][temp_model]
    system = PVSystem(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        module_parameters=module,
        inverter_parameters=inverter,
        temperature_model_parameters=temperature_parameters,
        modules_per_string=modules_per_string,
        strings_per_inverter=strings_per_inverter
    )

    # Get the correct file path from the FileStorage object
    datafile_path = datafile.filename

    # Rest of the function with correct indentation
    try:
        poa_data = pd.read_csv(datafile_path, index_col=0, parse_dates=True)

        # Data Validation (Optional but Recommended)
        required_columns = ["poa_global", "temp_air", "wind_speed"]  # Replace with your actual required columns
        missing_columns = [col for col in required_columns if col not in poa_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in the CSV file: {', '.join(missing_columns)}")

        # Ensure index is datetime
        if not isinstance(poa_data.index, pd.DatetimeIndex):
            raise ValueError("The index column should be a datetime.")

        model_chain = ModelChain(system, location)
        model_chain.run_model_from_poa(poa_data)
        print("I got here")  # This indicates successful model run

        # Optionally save the plot
        fig = model_chain.results.ac.plot(figsize=(16, 9))
        plt.savefig('ac_power_output.png')

    except pd.errors.EmptyDataError:
        return "Error: The uploaded CSV file is empty or has no headers."
    except pd.errors.ParserError:
        return "Error: The uploaded CSV file could not be parsed correctly. Please check the format, delimiter, and data types."
    except ValueError as e:
        return f"Error: {e}"  # Pass the specific ValueError message
    except Exception as e:
        return f"An unexpected error occurred: {e}"
