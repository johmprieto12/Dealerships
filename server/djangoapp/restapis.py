# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Generic GET request to Cloud Functions backend.
    Example:
        get_request("dealership", state="CA")
    """
    url = f"{backend_url}/{endpoint}"

    try:
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("❌ Error in GET request:", e)
        return {}

# Add code for get requests to back end

def analyze_review_sentiments(text):
    """
    Sends text to the sentiment analyzer service.
    Example:
        analyze_review_sentiments("The car is amazing")
    """
    request_url = sentiment_analyzer_url + "analyze/" + text

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("❌ Error analyzing sentiment:", e)
        return {}

# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

def post_review(data_dict):
    """
    Sends a POST request to the backend to submit a review.
    Example:
        post_review({ "name": "John", "review": "Great!" })
    """
    url = f"{backend_url}/review"

    try:
        response = requests.post(url, json=data_dict)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("❌ Error posting review:", e)
        return {}
