from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired

class RetrieveForm(FlaskForm):
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    output = StringField('Output File', validators=[DataRequired()])
    submit = SubmitField('Retrieve Data')

class ModelForm(FlaskForm):
    datafile = FileField('Data File', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    tz = StringField('Timezone', validators=[DataRequired()])
    altitude = IntegerField('Altitude', validators=[DataRequired()])

    module_database = SelectField('Module Database', choices=[
        ('SandiaMod', 'Sandia Module Database'),
        ('CECMod', 'CEC Module Database'),
        # Add other databases as needed
    ], default='SandiaMod')  # Default to SandiaMod
    inverter_database = SelectField('Inverter Database', choices=[
        ('CECInverter', 'CEC Inverter Database'),
        # Add other databases as needed
    ], default='CECInverter')
    # module_source = SelectField('Module Source', choices=[('SandiaMod', 'Sandia'), ('CECMod', 'CEC')], validators=[DataRequired()])
    # inverter_source = SelectField('Inverter Source', choices=[('CECInverter', 'CEC'), ('ADRInverter', 'ADR')], validators=[DataRequired()])

    module = SelectField('Module', choices=[])
    inverter = SelectField('Inverter', choices=[])
    temp_model = SelectField('Temperature Model', choices=[
        ('open_rack_glass_glass', 'Open Rack Glass-Glass'),
        ('roof_mount_glass_glass', 'Roof Mount Glass-Glass'),
        ('open_rack_glass_polymer', 'Open Rack Glass-Polymer'),
        ('insulated_back_glass_polymer', 'Insulated Back Glass-Polymer')
    ], validators=[DataRequired()])
    modules_per_string = IntegerField('Modules per String', validators=[DataRequired()])
    strings_per_inverter = IntegerField('Strings per Inverter', validators=[DataRequired()])
    surface_tilt = IntegerField('Surface Tilt', validators=[DataRequired()])
    surface_azimuth = IntegerField('Surface Azimuth', default=180, validators=[DataRequired()])
    location_name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Run Model')
