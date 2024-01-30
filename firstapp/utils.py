import smtplib
import os
from dotenv import load_dotenv
from geopy.distance import geodesic
from .models import GPS

load_dotenv()
class Util:
    @staticmethod
    def send_email(data):
        gmail_user = os.environ.get('EMAIL_USER')
        gmail_password = os.environ.get('EMAIL_PASS')

        sent_from = gmail_user
        to = [data['to_email']]
        subject = data['subject']
        body = data['body']

        email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

        try:
          # print("sent-from-", sent_from)
          smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
          smtp_server.ehlo()
          smtp_server.login(gmail_user, gmail_password)
          smtp_server.sendmail(sent_from, to, email_text)
          smtp_server.close()
          print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong….", ex)
            

def is_within_geofence(latitude, longitude):
  gpsInstance = GPS.objects.first()
  geofenceLatitude = float(gpsInstance.latitude)
  geofenceLongitude = float(gpsInstance.longitude)
  geofence_radius = float(gpsInstance.area)

  return (float(latitude) - geofenceLatitude)**2 + (float(longitude)-geofenceLongitude)**2 <= geofence_radius**2
