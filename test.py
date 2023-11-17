import json
import urllib3


url = "https://complexprogrammer.uz"
http = urllib3.PoolManager()
r = http.request('GET', url)
htmlSource = r.data
print(htmlSource)