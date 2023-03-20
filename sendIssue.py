#  Copyright (c) 2023. Bro Video Software.
# to use this you must have 2 step verification on google
# SET UP AN APP PASSWORD on Google:
# store your email address (from address) and the generated APP Password
# in a txt file called EmailSettings.txt in the root folder of this app
# My EmailSettings.txt IS NOT INCLUDED WITH THIS GIT:

# FORMAT OF EmailSettings.txt IS:
# line 1 yourfromEmail@google.com
# line 2 your APP Password like '**** **** **** ****'
# line 3 NEEDED BUT KEEP BLANK
# replace the * with your char! and no ' marks

import smtplib
from email.message import EmailMessage
import os

def configureEmail(subscriber, toEmail):       # pass in subscriber (name) and Email
    #subscriber = ""                            # set a test To NAME
    #toEmail = ""                               # can set this to send a test, to your self
    savedEmail, savedPW = getEmailSettings()    # from EmailSettings.txt

    msg = EmailMessage()
    msg['Subject'] = "Email sent by O.L.M. Issue Delivery System"
    msg['From'] = savedEmail
    msg['To'] = toEmail
    msg.set_content(f"Hello {subscriber}.\n This message has been sent to you because you are listed as\n"
                    "being subscribed to receive Outer Limits Magazine.\n"
                    "The latest issue is ATTACHED to this message as a pdf file.\n"
                    "For the latest on everything OLM or to contact us visit olm-mag.co.uk\n"
                    "DO NOT REPLY TO THIS MESSAGE, THIS EMAIL ACCOUNT IS NOT MONITORED\n"
                    "End...")

#    files = ['YOURFILENAME']                 # file or files to send: FULL PATH
#    for file in files:
#        with open(file, 'rb') as f:    # PROBLEM! FILE SIZE HAS TO BE LESS THAN 25GB
#            file_data = f.read()       # TO WORK
#            file_name = f.name
#        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # settings for Google with port number

        smtp.login(savedEmail, savedPW)  # log in to account

        smtp.send_message(msg)


def getEmailSettings():
    emailData = []
    file = open('EmailSettings.txt', 'r')
    f = file.readlines()
    for line in f:
        emailData.append(line[:-1])  # use [:-1] to loose the \n newline
    savedEmail = emailData[0]
    savedPW = emailData[1]
    return savedEmail, savedPW

testTo = 'sending to name'              # edit this
testEmail = 'email your sending to'     # edit this
configureEmail(testTo, testEmail)
