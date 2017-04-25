import requests
url = 'http://localhost:5000/'
resp = requests.post(url=url+'/observeTransition')
print(resp.status_code)