import requests
from datetime import datetime
import config
import smtplib
import threading

MY_LAT = config.MY_LAT
MY_LONG = config.MY_LONG
GMAIL = config.GMAIL
GMAIL_PW = config.GMAIL_PW
YAHOO = config.YAHOO


# compare iss location with my location
def iss_is_close_by():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5)


# compare sunrise and sunset with current time
def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour
    return (current_hour >= sunset) or (current_hour <= sunrise)


is_dark = is_dark()
iss_is_close_by = iss_is_close_by()


def send_email():
    threading.Timer(60.0, send_email).start()
    if iss_is_close_by and is_dark:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=GMAIL_PW)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=YAHOO,
                msg='Subject: Look Up!\n\nThe ISS is near by!!'
            )
    else:
        print('ISS is not here')


send_email()
