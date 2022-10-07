# Github Cli Tools

Container for python scripts that use the github cli to facilitate custom
workflows or tasks.

Only has a single script at present.

- `estimates_csv.py`

## Installation

Install github cli.

https://cli.github.com/

Run the python script from shell whilst in the relevant project folder, or add
the folder for this repo to PATH.

## Issue Estimates

`estimates_csv.py`

Looks for estimates in github issue body (description in first comment), in the
form (emoji used for disambiguation):

```
⏱️ Estimate:
```

Converts days to hours, accepts ranges for both.

Summarises the estimates and outputs a CSV.

Suggested uses:

- quotes
- invoices
- records
- client emails.

### Examples

```
⏱️ Estimate: 2.5 hrs
⏱️ Estimate: 0.5 - 20 hours
⏱️ Estimate: 1 day (if a fair wind blows)
⏱️ Estimate: 3-4 days
```
