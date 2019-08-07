import boto3

PARAMETER_STORE_REGION_NAME = 'us-east-1'

ssm = boto3.client('ssm', region_name=PARAMETER_STORE_REGION_NAME)

def get_parameter(name, with_decryption=False):
    resp = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
    return resp['Parameter']['Value']
