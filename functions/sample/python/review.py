import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(params):
    authenticator = IAMAuthenticator("_jmHxOs2-RLKmlfJ2JjQRzEzZ1mnl5bm3SS15Zv66N6d")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://39c5ae9d-7f45-4c94-bb02-22a7ce000df0-bluemix.cloudantnosqldb.appdomain.cloud")

    # Specify the database name
    db_name = 'reviews'

    if 'dealerId' in params:
        dealer_id = params['dealerId']
        selector = {'dealership': {'$eq': int(dealer_id)}}
        response = service.post_find(db=db_name, selector=selector).get_result()
        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response}
        }
        return result
    elif 'review' in params:
        review = params['review']
        new_review = {
            'id': int(review['id']),
            'name': review['name'],
            'dealership': int(review['dealership']),
            'review': review['review'],
            'purchase': review['purchase'],
            'another': review['another'],
            'purchase_date': review['purchase_date'],
            'car_make': review['car_make'],
            'car_model': review['car_model'],
            'car_year': int(review['car_year'])
        }
        try:
            response = service.post_document(
                db=db_name,
                document=new_review
            ).get_result()
            result = {
                'statusCode': 200,
                'body': {
                    'message': 'Review posted successfully',
                    'data': response
                }
            }
            return result
        except:
            result = {
                'statusCode': 500,
                'message': 'Failed to post review'
            }
            return result
    else:
        result = {
            'statusCode': 400,
            'message': 'Bad Request'
        }
        return result
