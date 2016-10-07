#!/usr/bin/python

import smtplib

sender = 'matthew.l.allen@gmail.com'
receivers = ['kc3eys@gmail.com']
username = 'matthew.l.allen'
password = 'i@ms1mple'

message = """From: BBB <BBB@localhost>
To: KC3EYS <kc3eys@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.ehlo()
   smtpObj.starttls()
   smtpObj.login(username,password)
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except:
   print "Error: unable to send email"
