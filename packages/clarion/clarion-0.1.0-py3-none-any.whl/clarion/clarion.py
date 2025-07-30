import io
import pandas as pd
import boto3

def load_from_s3(access_key = "admin", secret_key = "password", endpoint_url = "http://127.0.0.1:9000", data_key = None):
    # access_key = "admin"
    # secret_key = "password"
    # endpoint_url = "http://127.0.0.1:9000"

    # --- NEED TO HANDLE EXCEPTION ----
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key = secret_key, 
        endpoint_url = endpoint_url
    )

    # response = s3.list_buckets()
    # for bucket in response['Buckets']:
    #     print(bucket['Name'])

    response = s3.get_object(Bucket = 'autocleanse-data', Key = data_key)
    df = pd.read_csv(io.StringIO(response['Body'].read().decode('utf-8')))

    return df