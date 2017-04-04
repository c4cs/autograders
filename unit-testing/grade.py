#!/usr/bin/env python3

import csv
import json
import sys

sys.path.append('..')

import autograder
from test_cases import *

if len(sys.argv) < 2:
    print('Usage: ./grade.py submissions.csv [rerun]')
    exit()

if len(sys.argv) > 2 and sys.argv[2].lower() == 'rerun':
    rerun = True
else:
    rerun = False

uniq_to_repo = {}
with open(sys.argv[1]) as csvf:
    for row in csv.DictReader(csvf):
        uniq = row['Email Address'].split('@')[0]
        repo = row['Give the link to your github repository']
        uniq_to_repo[uniq] = repo

test_cases = [
    TestTravis(),
    TestExponentiationGood(),
    TestExponentiationBad(),
    TestExponentiationImpl(),
]

def gen_submissions():
    for uniq, repo in uniq_to_repo.items():
        yield uniq, (repo, '/tmp/c4cs-rpn/{}'.format(uniq))

submissions = {
    uniq: submission for uniq, submission in gen_submissions()
}

ag = autograder.Autograder(test_cases, submissions)

ag.clone(rerun)

ag.grade()

with open('results.json', 'w') as f:
    f.write(ag.to_json())

ag.print_stats()
