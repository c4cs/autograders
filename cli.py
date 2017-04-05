#!/usr/bin/env python3

import click
import csv
import json
import os
from termcolor import cprint

def init(ag_in):
    global ag
    ag = ag_in

@click.group(chain=True)
def cli():
    pass

@click.command()
@click.option('--rerun', is_flag=True, default=False)
def grade(rerun):
    '''Run the autograder'''
    global ag
    cprint('Grading...', 'green')
    ag.clone(rerun)
    ag.grade()

@click.command()
@click.option('--file', default='results.json', show_default=True)
def load(file):
    '''Load JSON results from the autograder'''
    global ag
    file = os.path.abspath(os.path.expanduser(file))
    cprint('Loading {}...'.format(file), 'green')
    ag.load_results(json.loads(open(file).read()))

@click.command()
@click.option('--outfile', default='scores.csv', show_default=True)
def to_canvas(outfile):
    '''Write canvas-friendly grades'''
    global ag
    outfile = os.path.expanduser(outfile)
    cprint('Writing {} scores to {}...'.format(len(ag.get_grades()), os.path.abspath(outfile)), 'green')
    with open(outfile, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=['Email', 'Total Score'])
        writer.writeheader()
        for uniq, score in ag.get_grades().items():
            writer.writerow({
                'Email': uniq,
                'Total Score': score,
            })

@click.command()
def write_emails():
    '''Generate autograder emails but do not send'''
    pass

@click.command()
def send_emails():
    '''Send pre-generated autograder emails'''
    pass

cli.add_command(grade)
cli.add_command(to_canvas)
cli.add_command(load)
cli.add_command(write_emails)
cli.add_command(send_emails)
