from posixpath import split
import requests
from datetime import datetime
import time
import smtplib

MY_EMAIL = "___YOUR_EMAIL_HERE____"
MY_PASSWORD = "___YOUR_PASSWORD_HERE___"
MY_SMTP = "__YOUR_SMTP_ADDRESS_HERE___"
MY_LAT = 53.260280
MY_LONG = 7.927060


def is_iss_overhead():
    # ISS (International Space Station) position
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # if position is within +5 or -5 degrees of the iss position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        # it's in the range
        return True


def is_night():
    # www.latlong.net/ - find sunrise and sunset in given location
    parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # return the hour
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # print(sunrise)  # 2022-01-17T08:02:35+00:00
    # print(sunrise.split("T"))  # ['2022-01-17', '08:02:35+00:00']
    # print(sunrise.split("T")[1].split(":")[0])  # 08

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        # it's dark
        return True


while True:
    # run every 60 seconds
    time.sleep(60)
    if is_iss_overhead() and is_night():
        print("Subject:Look Up👆\n\nThe ISS is above you in the sky.")
        # # send an email notification
        # connection = smtplib.SMTP(MY_SMTP)
        # connection.starttls()
        # connection.login(MY_EMAIL, MY_PASSWORD)
        # connection.sendmail(
        #     from_addr=MY_EMAIL,
        #     to_addrs=MY_EMAIL,
        #     msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        # )
    else:
        print("No Space Station to see on the sky :(")
