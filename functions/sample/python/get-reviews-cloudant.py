import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("_jmHxOs2-RLKmlfJ2JjQRzEzZ1mnl5bm3SS15Zv66N6d")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://39c5ae9d-7f45-4c94-bb02-22a7ce000df0-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
                db='reviews',
                selector={'dealership': int(dict['id'])},
            ).get_result()

    try:
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
            }
        return result
    except:
        return {
            'statusCode': 404,
            'message': 'Something went wrong'
            }
