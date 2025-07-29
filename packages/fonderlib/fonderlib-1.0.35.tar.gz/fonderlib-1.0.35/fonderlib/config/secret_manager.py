import json

import boto3
from botocore.exceptions import ClientError


class SecretManager:
    def __init__(self):
        secret_name = "credentials_spreadsheets_postgresql"
        region_name = "us-west-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        self.secret = json.loads(get_secret_value_response["SecretString"])

    def get_secret_spreadsheets(self):
        return self.secret["spreadsheets_secret"]

    def get_secret_postgres_db(self):
        return self.secret["db_secret"]
