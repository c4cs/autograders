c4cs-autograders
------------------

An assortment of scripts to help manage autograding of assignments.

### Dependencies
Probably a lot of them... Sorry.

### Grading assignments
e.g. for the unit testing homework, this script will clone + grade and write to
a `results.json` which can then be picked up by other scripts.

```bash
$ ./grade.py submissions.csv
```

### Emailing grades to students

You'll need an `email.cfg` file, which just contains host, user, and password on
one line each. You can use `smtp.mail.umich.edu`, your uniqname, and Kerberos
password.

First, write the emails:

```bash
$ ./emailer.py write results.json
```

Then give them a look. If you want to do a test send you can prune the directory
and rename a student's uniqname to yours. When you're ready:

```bash
$ ./emailer.py send
```


### Sending grades to Canvas
Generates a Gradescope-style csv.

```bash
$ ./to_canvas.py unit-testing/results.json ~/repos/c4cs-w17-grades/hw/Homework_10_Scores.csv
```

### Creating a new autograder
The `autograder.py` script contains a collection of classes.

- `Autograder` takes in a list of `TestCase`s and submissions which then
  individually get passed to `TestCase.test` by way of the `TestRunner`.
- `TestCase` returns a `TestCaseResult`.
