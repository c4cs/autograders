#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
from to_canvas import score_to_final
import json
import sys
import os
import sh

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

###### CHANGE ME
ASSIGNMENT_NAME = 'Homework 10'
TOTAL_POSSIBLE = 4.
REGRADE_DATE = 'April 7'
AUTOGRADER_LINK = "http://google.com"

USAGE='Usage: ./emailer.py [write|send] [results.json]'
if len(sys.argv) < 2:
    print(USAGE)
    exit()

with open('email.cfg') as e:
    SMTP_HOST = e.readline().strip()
    SMTP_USER = e.readline().strip()
    SMTP_PASS = e.readline().strip()
    
sm = None

def send_email(uniqname, body):
    SUBJECT = '[c4cs] {} Graded'.format(ASSIGNMENT_NAME)
    FROM = 'c4cs-staff@umich.edu'
    TO = uniqname + '@umich.edu'
    CC = ['mterwil@umich.edu',]
    encoding = 'html'

    print('Sending {}'.format(TO))

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg['CC'] = ','.join(CC)
    msg.attach(MIMEText(body, encoding))

    global sm
    if sm is None:
        sm = smtplib.SMTP_SSL(host=SMTP_HOST)
        sm.login(SMTP_USER, SMTP_PASS)

        send_to = [TO,] + CC
        sm.sendmail(FROM, send_to, msg.as_string())

loc = '/tmp/c4cs-autograder-emails/{}'.format(ASSIGNMENT_NAME.lower().replace(' ', '_'))

if sys.argv[1] == 'write':
    with open(sys.argv[2]) as f:
        data = json.loads(f.read())

    env = Environment(loader=FileSystemLoader('email_templates'))
    template = env.get_template('hw.html')
    sh.rm('-Rf', loc)
    sh.mkdir('-p', loc)
    with sh.pushd(loc):
        for uniq, submission in data.items():
            with open(uniq, 'w') as f:
                f.write(template.render(
                    uniq=uniq,
                    assignment_name=ASSIGNMENT_NAME,
                    total_possible=TOTAL_POSSIBLE,
                    regrade_date=REGRADE_DATE,
                    autograder_link=AUTOGRADER_LINK,
                    raw_score=submission['score'],
                    final_score=score_to_final(submission['score']),
                    testcases=submission['test_case_results'],
                ))
elif sys.argv[1] == 'send':
    with sh.pushd(loc):
        for uniq in os.listdir():
            with open(uniq) as f:
                send_email(uniq, f.read())
else:
    print(USAGE)
    exit()
