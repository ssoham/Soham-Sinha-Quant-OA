import csv 
import re

with open('sample_data.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

headers = rows[0]

with open('email_template.txt', 'r', encoding='utf-8') as f:
    template_data = f.read()

m = re.findall(r'(\_+\s*\_*\[.*?\]\_+\s*\_*)', template_data)
print(m)