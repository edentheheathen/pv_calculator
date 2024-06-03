from flask import Flask, render_template, redirect, url_for, request, jsonify
from forms import RetrieveForm, ModelForm
from retrieve import retrieve_pvgis_data
from model_chain import run_model_chain
import pvlib
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    form = RetrieveForm()
    if form.validate_on_submit():
        latitude = form.latitude.data
        longitude = form.longitude.data
        year = form.year.data
        output = form.output.data  # Get the output file name from the form
        retrieve_pvgis_data(latitude, longitude, year, output)
        return redirect(url_for('index'))
    return render_template('retrieve.html', form=form)

def populate_form_choices(form):
    module_database = form.module_database.data
    inverter_database = form.inverter_database.data

    try:
        sandia_modules = pvlib.pvsystem.retrieve_sam(module_database)
        cec_inverters = pvlib.pvsystem.retrieve_sam(inverter_database)
    except pvlib.pvsystem.SamDownloadError as e:
        print(f"Error retrieving SAM data: {e}")
        return  # Don't populate choices if there's an error

    module_names = list(sandia_modules.keys())
    inverter_names = list(cec_inverters.keys())
    module_choices = [(model, model) for model in module_names]
    inverter_choices = [(inverter, inverter) for inverter in inverter_names]

    form.module.choices = module_choices
    form.inverter.choices = inverter_choices


@app.route('/model', methods=['GET', 'POST'])
def model():
    form = ModelForm()
    populate_form_choices(form)
    if form.validate_on_submit():
        datafile = form.datafile.data
        print (datafile)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], datafile.filename)
        datafile.save(filepath)
        latitude = form.latitude.data
        longitude = form.longitude.data
        tz = form.tz.data
        altitude = form.altitude.data
        temp_model = form.temp_model.data
        module_database = form.module_database.data
        inverter_database = form.inverter_database.data
        module = form.module.data
        inverter = form.inverter.data
        modules_per_string = form.modules_per_string.data
        strings_per_inverter = form.strings_per_inverter.data
        surface_tilt = form.surface_tilt.data
        surface_azimuth = form.surface_azimuth.data
        location_name = form.location_name.data

        try:
            sandia_modules = pvlib.pvsystem.retrieve_sam(module_database)
            cec_inverters = pvlib.pvsystem.retrieve_sam(inverter_database)
            module = sandia_modules[form.module.data]
            inverter = cec_inverters[form.inverter.data]
            run_model_chain(datafile, latitude, 
                        longitude, tz, altitude, 
                        module, 
                        inverter, 
                        temp_model, modules_per_string, 
                        strings_per_inverter, surface_tilt, 
                        surface_azimuth, location_name)
            return redirect(url_for('index'))
        except (KeyError, FileNotFoundError) as e:
            # Handle both KeyError (invalid module/inverter) and SamDownloadError
            return render_template('model.html', form=form, error=str(e))
    else:
        populate_form_choices(form)  # Populate choices only on initial GET request
    return render_template('model.html', form=form)

    

if __name__ == '__main__':
    app.run(debug=True)
