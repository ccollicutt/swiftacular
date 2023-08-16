import requests
from swiftclient import client


i = 1
user, password, auth_url = "achilles", "CHANGEME", "http://192.168.100.50:5000/v3/auth/tokens"
continer_name, obejct_name, object_data, object_ttl =  f'test-container-{1}', f'obj_number_{1}', "A"*1, 60*60

def get_connection_info(user, password, auth_url):
    resp = requests.post(auth_url, headers={'Content-Type':'application/json'},json ={ "auth": {"identity": {"methods": ["password"],"password": {"user": {"name": user,"domain": { "id": "default" },"password": password}}}}})
    token = resp.headers["X-Subject-Token"]
    endpoint = [endpoint for endpoint in [catalog_endpoints for catalog_endpoints in  resp.json()['token']['catalog'] if catalog_endpoints['type'] == "object-store"][0]['endpoints'] if endpoint['interface'] =='public'][0]['url']
    return token, endpoint 

def main():
    token, endpoint = get_connection_info(user, password, auth_url)
    client.put_container(endpoint, token, continer_name, headers={'X-Storage-Policy': "Policy-0"})
    return_id = client.put_object(endpoint, token, continer_name, obejct_name, object_data, headers={'X-Delete-After': object_ttl })
    print(f"The retuen id for the object is {return_id}")


main()
