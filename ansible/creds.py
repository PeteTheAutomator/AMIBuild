import os
import sys
import requests
import json

if 'AWS_CONTAINER_CREDENTIALS_RELATIVE_URI' not in os.environ.keys():
    print("Environment variable AWS_CONTAINER_CREDENTIALS_RELATIVE_URI is not set - aborting...")
    sys.exit(1)

creds_url="http://169.254.170.2" + os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

r = requests.get(creds_url)
d = json.loads(r._content)

creds = "aws_access_key: " + d['AccessKeyId'] + '\n'
creds += "aws_secret_key: " + d['SecretAccessKey'] + '\n'
creds += "security_token: " + d['Token']

with open('creds.yml', 'w') as fh:
    fh.write(creds)

fh.close()


if 'SSH_PRIV_KEY' in os.environ.keys():
    with open('key.pem', 'w') as fh:
        fh.write(os.environ['SSH_PRIV_KEY'])

    fh.close()
    os.chmod('key.pem', 0600)
