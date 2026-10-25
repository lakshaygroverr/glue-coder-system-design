# demo1_request.py - you are the client. Send a real request and read the response.
import time
import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&current=temperature_2m,wind_speed_10m"

start = time.time()
response = requests.get(url)
ms = (time.time() - start) * 1000

print("REQUEST")
print("  Method:", response.request.method)
print("  URL:   ", url)
print()
print("RESPONSE")
print("  Status code:", response.status_code)
print("  Took:", round(ms), "ms")
print("  Content-Type:", response.headers.get("Content-Type"))
print()
if response.ok:
    data = response.json()
    print("BODY (the actual data)")
    print("  Toronto temperature right now:", data["current"]["temperature_2m"], "°C")
    print("  Wind speed:", data["current"]["wind_speed_10m"], "km/h")

print()
print("Now let's ask for a page that doesn't exist:")
bad = requests.get("https://api.open-meteo.com/v1/this-does-not-exist")
print("  Status code:", bad.status_code)
