import csv
from re import template
from tabnanny import check
import regex as re

with open('sample_data.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

headers = rows[0]
rows.pop(0)

with open('email_template.txt', 'r', encoding='utf-8') as f:
    template_data = f.read()

user = input("Would you like to pass a RegEx filter or an example (r/e)")
if user == "r":
    filter = input(
        "Default filter is for: __[x]__ (including space checks). If you want to change it, enter a new filter."
    )
    filter = "(\_+\s*\_*\[*.*?\]*\_+\s*\_*)" if filter == "" else filter
    filter = re.compile(filter)
if user == "e":
    print("")

m = re.findall(filter, template_data)
if len(m) == 0:
    print("incorrect filter given")

ops, ends = set(), set()
if len(m) > 0:
    opening_1 = re.search(r".+?(?=[a-zA-Z]\s*)", m[0]).group()
    closing_1 = re.search(r".+?(?=[a-zA-Z]\s*)", m[0][::-1]).group()[::-1]
print(closing_1)

for i in range(len(m)):
    ops.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i]).group())
    ends.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i][::-1]).group()[::-1])

if len(ops) != 1 or len(ends) != 1:
    print("multiple patterns were detected")
    print("The regex initially passed was: " + filter.pattern)
    for i in range(len(ends)):
        is_replaced = input("should {} be considered as correct? (y/n)".format(list(ends)[i]))
        if is_replaced == "y":
            string = list(ends)[i]
            ends.remove(string)
            template_data = template_data.replace(string, ends[0])


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

# print(m)
print(substituted_email)