"""
    pip install Office365-REST-Python-Client
    Alternative:
    pip install git+https://github.com/vgrem/Office365-REST-Python-Client.git

"""

from . import ModelName

client_credentials = ClientCredential('{client_id}','{client_secret}')
ctx = ClientContext('{url}').with_credentials(client_credentials)
