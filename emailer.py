#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import json
import sys
import os
import sh

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

###### CHANGE ME
# ASSIGNMENT_NAME = 'Homework 10'
# TOTAL_POSSIBLE = 4.
# REGRADE_DATE = 'April 7'
# AUTOGRADER_LINK = 'https://github.com/c4cs/autograders/blob/master/unit-testing/test_cases.py'

# with open('email.cfg') as e:
#     SMTP_HOST = e.readline().strip()
#     SMTP_USER = e.readline().strip()
#     SMTP_PASS = e.readline().strip()
    
sm = None

# def send_email(uniqname, body):
#     SUBJECT = '[c4cs] {} Graded'.format(ASSIGNMENT_NAME)
#     FROM = 'c4cs-staff@umich.edu'
#     TO = uniqname + '@umich.edu'
#     CC = ['mterwil@umich.edu',]
#     encoding = 'html'

#     print('Sending {}'.format(TO))

#     msg = MIMEMultipart()
#     msg['Subject'] = SUBJECT
#     msg['From'] = FROM
#     msg['To'] = TO
#     msg['CC'] = ','.join(CC)
#     msg.attach(MIMEText(body, encoding))

#     global sm
#     if sm is None:
#         sm = smtplib.SMTP_SSL(host=SMTP_HOST)
#         sm.login(SMTP_USER, SMTP_PASS)

#     send_to = [TO,] + CC
#     sm.sendmail(FROM, send_to, msg.as_string())

loc = '/tmp/c4cs-autograder-emails/{}'.format(ASSIGNMENT_NAME.lower().replace(' ', '_'))

def write_emails(assignment_name, total_points, regrade_date, autograder_link, dest):
    env = Environment(loader=FileSystemLoader('email_templates'))
    template = env.get_template('hw.html')
    sh.rm('-Rf', loc)
    sh.mkdir('-p', loc)
    with sh.pushd(loc):
        for uniq, submission in data.items():
            with open(uniq, 'w') as f:
                f.write(template.render(
                    uniq=uniq,
                    assignment_name=assignment_name,
                    total_possible=total_points,
                    regrade_date=regrade_date,
                    autograder_link=autograder_link,
                    raw_score=submission['score'],
                    final_score=score_to_final(submission['score']),
                    testcases=submission['test_case_results'],
                ))

# elif sys.argv[1] == 'send':
#     with sh.pushd(loc):
#         for uniq in os.listdir():
#             with open(uniq) as f:
#                 send_email(uniq, f.read())
# else:
#     print(USAGE)
#     exit()
