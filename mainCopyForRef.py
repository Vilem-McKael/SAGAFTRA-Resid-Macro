import csv

with open('data/residuals.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

with open('data/7.1.25 Residuals.csv', 'r') as f2:
    reader2 = csv.reader(f2)
    for row in reader2:
        print(row)