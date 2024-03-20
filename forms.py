from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class FeedbackForm(FlaskForm):
    feedback= StringField('Feedback')
    submit= SubmitField('Submit')
    
