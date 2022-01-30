import csv
import re
from rich import print

with open("sample_data.csv", "r", encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

headers = rows[0]
rows.pop(0)

with open("email_template.txt", "r") as f:
    template_data = f.read()

user = input("Would you like to pass a RegEx filter or an example (r/e)")
if user == "r":
    filter = input(
        "Default filter is for: __[x]__. If you want to change it, enter a new filter."
    )
    filter = "(\_+\s*\_*\[*.*?\]*\_+\s*\_*)" if filter == "" else filter
    filter = re.compile(filter)
if user == "e":
    example = input('Enter an example: "__[x]__"')

m = re.findall(filter, template_data)
if len(m) == 0:
    print("incorrect filter given")

for i in range(len(rows)):
    substituted_email = template_data
    for match in m:
        label = re.search(r"[a-zA-Z\s]+", match).group(0)
        label = label.strip()

        if label not in headers:
            lowered_headers = list(map(lambda x: x.lower(), headers))
            if label.lower() in lowered_headers:
                replace = input(
                    'Should "{}" be replaced with "{}"? (y/n)'.format(
                        label, headers[lowered_headers.index(label.lower())]
                    )
                )
                if replace == "y":
                    substituted_email = substituted_email.replace(
                        match, rows[i][lowered_headers.index(label.lower())]
                    )
        else:
            substituted_email = substituted_email.replace(
                match, rows[i][headers.index(label)]
            )