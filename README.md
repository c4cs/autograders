c4cs-autograders
------------------

An assortment of scripts to help manage autograding of assignments.

### Working with the CLI

1. Grab the `grade.py` from an existing assignment
1. Implement `get_test_cases_and_submissions`, which must return 
    `test_cases` and `submissions`. This gets injected into the cli.
1. `grade.py` is the entrypoint for `cli.py`. In your directory, call
   `grade.py --help` for more usage information.

#### Common tasks:

```bash
# grade everything in a given submissions file
# will clone but throw away the grades
$ ./grade.py grade -s ~/Downloads/c4cs-rpn-repos.csv 

# you really want to chain commands:
$ ./grade.py grade -s ~/Downloads/c4cs-rpn-repos.csv write_results

# now to load those results back up:
$ ./grade.py load_results print_stats

# and each command and subcommand has help
$ ./grade.py load_results --help

# write emails but don't send
$ ./grade.py load_results write_emails \
    --assignment-name="Homework 10" \
    --total-points=4 \
    --regrade-date="April 7" \
    --autograder-link="https://google.com" \
    --dest="/tmp/hw10_emails"

# send the emails
$ ./grade.py send_emails
    --loc="/tmp/hw10_emails"
    --subject="[c4cs] HW10 Graded"
    --smtp-username="mterwil"
    --cc="mterwil@umich.edu"
```

### Creating a new autograder
The `autograder.py` script contains a collection of classes.

- `Autograder` takes in a list of `TestCase`s and submissions which then
  individually get passed to `TestCase.test` by way of the `TestRunner`.
- `TestCase` returns a `TestCaseResult`.

### Dependencies
Probably a lot of them... Sorry.

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
