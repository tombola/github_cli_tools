import csv
import json
import re
import subprocess
from collections import UserList
from decimal import Decimal
import sys

HOURS_PER_DAY = 6
HOURLY_RATE = 50
CURRENCY = "£"

label_params = []
sys.argv.pop(0)
if len(sys.argv):
    for label in sys.argv:
        label_params.append("--label")
        label_params.append(label)

# Variables to output into csv rows
COLUMNS = [
    "issue_number",
    "url",
    "title",
    "estimate_num",
    "estimate_range",
    "averaged_estimate"
]

output = subprocess.run(
    [
        "gh",
        "issue",
        "list",
        "--state", "open",
        *label_params,
        # "--label", "some label",
        "--json", "number,title,state,url,labels,body"
    ],
    capture_output=True
)

if output.returncode != 0:
    print("Couldn't get github issues.")
    print("Try running `gh issue list` yourself and see if the github cli can authenticate.")
    quit()

issues = json.loads(output.stdout)
total_hours = 0
total_cost = 0

class ReadableRange(UserList):
    """
    Change the string representation of the list used to represent a range estimate.
    """
    def __str__(self):
        if len(self.data):
            return f"{self.data[0]} - {self.data[1]}"
        return ""


def estimate_in_hours(estimate, unit):
    """
    Normalise estimate to hours rather than days.
    """
    estimate = Decimal(estimate)
    if unit == "HOURS":
        return estimate
    return estimate * HOURS_PER_DAY


with open('issue_estimates.csv', mode='w') as estimates_csv:
    estimate_writer = csv.writer(
        estimates_csv,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    estimate_writer.writerow(COLUMNS)
    print("\nIssue Estimates\n")

    for issue in issues:
        issue_number = issue["number"]
        url = issue["url"]
        title = issue["title"]
        estimate_match = re.search(
            "^⏱️ Estimate: ([0-9\- \. ]*)([A-Za-z ]*)",
            issue["body"]
        )
        if not estimate_match:
            continue

        estimate_num = estimate_match.group(1).replace(" ", "")
        estimate_str = estimate_match.group(2).lower()
        averaged_estimate = None

        estimate_range = ReadableRange()
        unit = "HOURS"

        if estimate_str.find("day") > -1:
            unit ="DAYS"

        if estimate_num.find("-") > -1:
            estimate_range = ReadableRange(
                [estimate_in_hours(str(e), unit) for e in estimate_num.split("-")]
            )
            averaged_estimate = (estimate_range[0] + estimate_range[1]) / 2
            estimate_num = None
            message = f"{url} - {averaged_estimate} "
            "(average) ({estimate_num} {estimate_str})"
        else:
            estimate_num = estimate_in_hours(estimate_num, unit)
            averaged_estimate = estimate_num
            message = f"{url} - {estimate_num} hours "
            "({estimate_num} {estimate_str})"

        column_values = [globals()[c] for c in COLUMNS]

        estimate_writer.writerow(column_values)
        total_hours += averaged_estimate
        total_cost += averaged_estimate * HOURLY_RATE
        print(message)

print("\nTotals\n")

print(f"{total_hours} hours")
print(f"{CURRENCY}{total_cost}")