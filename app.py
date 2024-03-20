from flask import Flask, render_template, request
from forms import FeedbackForm

import requests
import os 
import uuid 
import json 
from dotenv import load_dotenv 
load_dotenv() 

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app= Flask(__name__)
app. config['SECRET_KEY']= "Ruchita"


@app.route('/', methods=['GET', 'POST'])
def home():
    return "Hi welcome to Sentiment Analysis portal!"

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form=FeedbackForm()
    return render_template('feedback.html', form=form)


@app.route('/feedback_post', methods=['POST'])
def feedback_post():
    feedb=request.form.get('feedback')
    # Load the values from .env 
    language_key = os.environ.get('KEY')
    language_endpoint = os.environ.get('ENDPOINT')
    location = os.environ['LOCATION'] 

    # Authenticate the client using your key and endpoint 
    def authenticate_client():
        ta_credential = AzureKeyCredential(language_key)
        text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
        return text_analytics_client

    #create and authenticate the client
    client = authenticate_client()
    
    #feedback received is in string and inout to text analytics has to be a document so convert it to one as follows:
    documents=[
        {"id":"1","language":"en", "text":feedb}
    ]

    #Analyze the sentiment
    result= client.analyze_sentiment(documents, show_opinion_mining=True)
    senti=[r for r in result if not r.is_error]
    print("Let's visualize the sentiment of each of these documents")
    for idx, doc in enumerate(senti):
        print(f"Document text: {documents[idx]}")
        print(f"Overall sentiment: {doc.sentiment}")
    
    return render_template('result.html', sentiment=[doc.sentiment for idx, doc in enumerate(senti)])


