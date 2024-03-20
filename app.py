from flask import Flask, render_template
from forms import FeedbackForm

app= Flask(__name__)
app. config['SECRET_KEY']= "Ruchita"


@app.route('/', methods=['GET', 'POST'])
def home():
    return "Hi welcome"

@app.route('/feedback')
def feedback():
    form=FeedbackForm()
    return render_template('feedback.html', form=form)
