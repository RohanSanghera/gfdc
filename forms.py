from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class GFDCInputs(FlaskForm):

   dev = FloatField('Mean Deviation: ', validators = [DataRequired()])
   central_point_1 = FloatField('Global Plot Central Decibel Values:', validators = [DataRequired()])
   central_point_2 = FloatField(' ', validators = [DataRequired()])
   central_point_3 = FloatField('Central Point 3', validators = [DataRequired()])
   central_point_4 = FloatField('Central Point 4', validators = [DataRequired()])
   
   submit = SubmitField('Run Analysis')

class UploadForm(FlaskForm):
   image_data = TextAreaField('Paste your image here')
   submit_input = SubmitField('Submit')


