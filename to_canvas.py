#!/usr/bin/env python3

import json
import csv
import sys
import canvasgrader

def score_to_final(score):
    if score > 2.:
        return 4.
    if score > .25:
        return 2.
    return 0.

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./to_canvas.py results.json outfile.csv')
        exit()

    with open(sys.argv[1]) as f:
        data = json.loads(f.read())

    with open(sys.argv[2], 'w') as csvf:
        # Gradescope style csv
        writer = csv.DictWriter(csvf, fieldnames=['Email', 'Total Score'])
        writer.writeheader()
        for uniq, submission in data.items():
            writer.writerow({
                'Email': uniq,
                'Total Score': submission['score']
            })
