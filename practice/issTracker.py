import requests

data = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_postion = data.json()["iss_position"]
latitude = iss_postion["latitude"]
longitude = iss_postion["longitude"]
current_location = (latitude, longitude)

print(current_location)
