#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os
import sh

def write_emails(data, assignment_name, total_points, regrade_date, autograder_link, dest, ceil_func):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) + '/email_templates'))
    template = env.get_template('c4cs.html')
    sh.mkdir('-p', dest)
    with sh.pushd(dest):
        for uniq, submission in data.items():
            with open(uniq, 'w') as f:
                f.write(template.render(
                    uniq=uniq,
                    assignment_name=assignment_name,
                    total_possible=total_points,
                    regrade_date=regrade_date,
                    autograder_link=autograder_link,
                    raw_score=submission['score'],
                    final_score=ceil_func(submission['score']),
                    testcases=submission['test_case_results'],
                ))
