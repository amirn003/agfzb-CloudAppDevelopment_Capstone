import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'apikey' in kwargs.keys():
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]

            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            #print(dealer_doc["full_name"])
            #print(dealer_obj)
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    dealerId = int(dealerId)
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            if dealer_doc["id"] == dealerId:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                #print(dealer_doc["full_name"])
                #print(dealer_obj)
                results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, dealerId, **kwargs):
    results = []
    dealerId = int(dealerId)
    # Call get_request with a URL parameter
    #json_result = get_request(url, dealerId=dealerId)
    json_result = get_request(url)
    #print(json_result)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["data"]["docs"]
        # For each review object
        for review_doc in reviews:
            # Get its content in `doc` object
            #print(review_doc)
            # Create a DealerReview object with values in `doc` object
            #  name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
            # need to double the sentences or Error: not enough text for language id
            review_to_be_analyzed = review_doc["review"] + " " + review_doc["review"]
            #print(review_to_be_analyzed)
            sentiment = analyze_review_sentiments(review_to_be_analyzed)
            #print(sentiment)

            review_obj = DealerReview(name=review_doc["name"], purchase=review_doc["purchase"], review=review_doc["review"],
                                purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"], car_model=review_doc["car_model"],
                                car_year=review_doc["car_year"], sentiment=sentiment, id=review_doc["id"])
            #print(review_doc["full_name"])
            #print(review_obj)
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative

    authenticator = IAMAuthenticator('CLD2r3ZUb1czL2pLy8G5H4NKqnBBtrThQpSuk9_UT2bo')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url('https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/e7d4955a-6db7-4151-a4ef-ef90813294ba')


    response = natural_language_understanding.analyze(
    text=text,
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()

    result = json.dumps(response, indent=2)
    json_result = json.loads(result)
    sentiment = json_result['keywords'][0]['sentiment']['label']
    return sentiment
