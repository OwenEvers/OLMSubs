#  Copyright (c) 2023. Bro Video Software.
# to use this you must have 2 step verification on google
# SET UP AN APP PASSWORD on Google:
# store your email address (from address) and the generated APP Password
# in a txt file called EmailSettings.txt in the root folder of this app
# My EmailSettings.txt IS NOT INCLUDED WITH THIS GIT:

# FORMAT OF EmailSettings.txt IS:
# line 1 yourfromEmail@google.com
# line2 your APP Password like '**** **** **** ****'
# replace the * with your char! and no ' marks
import smtplib


def configureEmail():
    savedEmail = ""
    savedPW = ""
    toEmail = ""
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # settings for Google with port number
        smtp.ehlo()  # handshake
        smtp.starttls()  # secure
        smtp.ehlo()  # handshake

        smtp.login(savedEmail, savedPW)  # log in to account

        subject = "test email"
        body = "This is the body text"
        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(savedEmail, toEmail, msg)
