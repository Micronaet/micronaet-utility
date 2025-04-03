"""
    Creazione dell'identificatore app completata.

    ---------------------------------------------------------------------------
    1.Setup APP:
    ---------------------------------------------------------------------------
    Sito: https://panchemicalsitaly.sharepoint.com/sites/IT/_layouts/15/appregnew.aspx

    ID client: e31f9c0f-5a52-4ae3-85bc-c175045396bc
    Segreto client: L+3eec8y95HDt1MIO+/9Oo7d/QmLiFvaGkqoHepXeM4=
    Titolo: PythonAPI
    Dominio app: localhost
    URI reindirizzamento: https://localhost


    Note: https://learn.microsoft.com/it-it/sharepoint/dev/sp-add-ins/retirement-announcement-for-azure-acs

    ---------------------------------------------------------------------------
    2. Autorizzo APP:
    ---------------------------------------------------------------------------
    https://panchemicalsitaly.sharepoint.com/sites/IT/_layouts/15/appinv.aspx

    Usare:
    <AppPermissionRequests AllowAppOnlyPolicy="true">
        <AppPermissionRequest Scope="http://sharepoint/content/sitecollection/web" Right="FullControl" />
    </AppPermissionRequests>

    ---------------------------------------------------------------------------
    3. Recupero ID Tenant:
    ---------------------------------------------------------------------------
    Sito: https://login.microsoftonline.com/panchemicalsitaly.onmicrosoft.com/.well-known/openid-configuration

    {
        "token_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/oauth2/token",
        "token_endpoint_auth_methods_supported": [
            "client_secret_post",
            "private_key_jwt",
            "client_secret_basic"
            ],
        "jwks_uri": "https://login.microsoftonline.com/common/discovery/keys",
        "response_modes_supported": [
            "query",
            "fragment",
            "form_post",
            ],
        "subject_types_supported":[
            "pairwise"
            ],
        "id_token_signing_alg_values_supported": [
            "RS256"
            ],
        "response_types_supported": [
            "code",
            "id_token",
            "code id_token",
            "token id_token",
            "token"
            ],
        "scopes_supported": [
            "openid"
            ],
        "issuer": "https://sts.windows.net/d6a7ff30-4398-46ab-9a8c-821db007295f/",
        "microsoft_multi_refresh_token": true,
        "authorization_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/oauth2/authorize",
        "device_authorization_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/oauth2/devicecode",
        "http_logout_supported": true,
        "frontchannel_logout_supported": true,
        "end_session_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/oauth2/logout",
        "claims_supported": [
            "sub",
            "iss",
            "cloud_instance_name",
            "cloud_instance_host_name",
            "cloud_graph_host_name",
            "msgraph_host",
            "aud",
            "exp",
            "iat",
            "auth_time",
            "acr",
            "amr",
            "nonce",
            "email",
            "given_name",
            "family_name",
            "nickname"
            ],
        "check_session_iframe": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/oauth2/checksession",
        "userinfo_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/openid/userinfo",
        "kerberos_endpoint": "https://login.microsoftonline.com/d6a7ff30-4398-46ab-9a8c-821db007295f/kerberos",
        "tenant_region_scope": "EU",
        "cloud_instance_name": "microsoftonline.com",
        "cloud_graph_host_name": "graph.windows.net",
        "msgraph_host": "graph.microsoft.com",
        "rbac_url": "https://pas.windows.net"
        }
"""

import requests
import json


site = 'IT'
client_id = 'e31f9c0f-5a52-4ae3-85bc-c175045396bc'  # App ID
client_secret = 'L+3eec8y95HDt1MIO+/9Oo7d/QmLiFvaGkqoHepXeM4='
# tenant = 'PanChemicalsItaly'
tenant = 'panchemicalsitaly'
tenant_id = 'd6a7ff30-4398-46ab-9a8c-821db007295f'

client_id = client_id + '@' + tenant_id

data = {
    'grant_type': 'client_credentials',
    # 'resource': '%s/%s.sharepoint.com@%s' % (tenant_id, tenant, tenant_id),
    'resource': '00000003-0000-0ff1-ce00-000000000000/%s.sharepoint.com@%s' % (
        tenant, tenant_id),
    'client_id': client_id,
    'client_secret': client_secret,
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

url = 'https://accounts.accesscontrol.windows.net/%s/tokens/OAuth/2' % \
      tenant_id
reply = requests.post(url, data=data, headers=headers)
# print(reply.text)
json_data = json.loads(reply.text)

# print(json_data)

headers = {
    'Authorization': "Bearer " + json_data['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose'
}

# url = "https://%s.sharepoint.com/sites/IT/_api/web/lists/
# getbytitle('Customers')/items" % tenant
# reply = requests.get(url, headers=headers)
# import pdb; pdb.set_trace()

# url = 'https://%s.sharepoint.com/_api/search/query?query_parameter=value
# &amp;query_parameter=value' % tenant
url = 'https://%s.sharepoint.com/sites/IT/_api/search/query?querytext=' \
      '\'sharepoint\'' % tenant
reply = requests.get(url, headers=headers)
print(reply.text)
import pdb; pdb.set_trace()


