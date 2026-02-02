import csv
import streamlit as st
import pandas as pd
from io import StringIO

def main(date, residual_data_filepath, new_filename):

    with open(residual_data_filepath, 'r') as f:
        count_reader = csv.reader(f)
        count = sum(1 for row in count_reader)
        f.seek(0)
        reader = csv.reader(f)

        new_file = open(f'results/{new_filename}.csv', 'w')
        new_file.write(f"\ufeff{date}, '', '', ''\n")
        new_file.write("'Company', 'Gross', 'Net', 'Corp'")

        # iteration vars
        current_check_no = False
        current_company = ""
        sum_gross = 0
        sum_net = 0
        current_corp = ""

        # summary vars
        is_finished = False
        net_totals = {}

        # processing
        for row in reader:
            print(reader.line_num)

            if reader.line_num == 1:
                print('here')
                continue

            if reader.line_num == count:
                is_finished = True

            print(row[0])
            check_no = row[0]

            if check_no == current_check_no:
                print('adding sums')
                sum_gross += float(row[10].replace('$', ''))
                sum_net += float(row[11].replace('$', ''))
            else:
                print('new check')
                if current_check_no:
                    new_file.write(f"{current_company}, {sum_gross}, {sum_net}, {current_corp}\n")
                    net_totals[current_corp] = net_totals.get(current_corp, 0) + sum_net

                current_check_no = check_no
                current_corp = row[1]
                current_company = row[3]
                print('gross: ', row[10], 'net: ', row[11])
                sum_gross = float(row[10].replace('$', ''))
                sum_net = float(row[11].replace('$', ''))

                if is_finished:
                    new_file.write(f"{current_company}, {sum_gross}, {sum_net}, {current_corp}\n")
                    net_totals[current_corp] = net_totals.get(current_corp, 0) + float(sum_net)

            if is_finished:
                for k, v in net_totals.items():
                    new_file.write(f"'', '', {v}, {k}\n")

                # if i == count:
                #     new_file.write(f"{current_company}, {sum_gross}, {sum_net}, {current_corp}\n")
                #     net_totals[current_corp] = net_totals.get(current_corp, 0) + sum_net
                #
                #     new_file.write

            print(row)



main('Jul 10 2025', 'data/residuals1-30-26.csv', 'result3')
# Current CSV Format:
# ['SAG-AFTRA ID', 'Payee Name', 'Payee Type', 'Company', 'Payroll House', 'Production/Episode Title', 'Check Status', 'Check Status Date', 'Check #', 'Check Date', 'Gross Amount', 'Net Amount', 'Received Date', 'Donated', 'Prod Title Gross Amt']
# ['10043657', 'E M L PRODS', 'ORGANIZATION', 'Nickelodeon', 'GEP Talent Services, LLC - SDDD (1494)', 'Rugrats / Rugrats Chanukah, A', 'Queued for Post', '7/1/25', '60565650', '6/16/25', '$17.13', '$17.13', '6/17/25', 'No', '$0.35']
# ['10043657', 'E M L PRODS', 'ORGANIZATION', 'Nickelodeon', 'GEP Talent Services, LLC - SDDD (1494)', 'Rugrats / Rugrats Chanukah, A', 'Queued for Post', '7/1/25', '60565650', '6/16/25', '$17.13', '$17.13', '6/17/25', 'No', '$14.47']
# ['10043657', 'E M L PRODS', 'ORGANIZATION', 'Nickelodeon', 'GEP Talent Services, LLC - SDDD (1494)', 'Rugrats / Rugrats Chanukah, A', 'Queued for Post', '7/1/25', '60565650', '6/16/25', '$17.13', '$17.13', '6/17/25', 'No', '$1.19']

# NEEDED:
# Col 0: Check # - GROUP BY
# Col 1: Payee Org
# Col 3: Company
# Col 10: Gross
# Col 11: Net

# Desired CSV Format:
# ['\ufeff"Tuesday July 1', ' 2025"', '', '', '']
# ['Company', 'Gross', 'Net', 'Corp']
# ['Nickelodeon', '$17.13 ', '$17.13 ', 'EML']
# ['Paramount Pictures Corporation', '$351.44 ', '$351.44 ', 'EML']
# ['Paramount Pictures Corporation', '$55.37 ', '$55.37 ', 'LBI']
# ['Paramount Pictures Corporation', '$94.62 ', '$94.62 ', 'LBI']
# ['Paramount Pictures Corporation', '$13.91 ', '$13.91 ', 'EML']
# ['Warner Bros. Pictures Inc.', '$63.20 ', '$63.20 ', 'EML']
# ['Warner Bros. Pictures Inc.', '$1,263.12 ', '$1,263.12 ', 'LBI']
# ['Metro-Goldwyn-Mayer Pictures Inc.', '$13.05 ', '$13.05 ', 'EML']
# ['Universal City Studios LLC', '$6,223.55 ', '$6,223.55 ', 'LBI']
# ['Universal City Studios LLC', '$41.58 ', '$41.58 ', 'EML']
# ['Universal City Studios LLC', '$3,254.83 ', '$3,254.83 ', 'EML']
# ['Walt Disney Pictures', '$993.98 ', '$993.98 ', 'EML']
# ['Walt Disney Pictures', '$25.09 ', '$15.69 ', 'LehBod']
# ['Walt Disney Pictures', '$3,464.00 ', '$3,464.00 ', 'LBI']
# ['Warner Bros. Pictures Inc.', '$222.05 ', '$222.05 ', 'EML']
# ['Warner Bros. Pictures Inc.', '$275.06 ', '$275.06 ', 'LBI']
# ['Warner Bros. Pictures Inc.', '$18.82 ', '$15.93 ', 'LehBod']
# ['Warner Bros. Pictures Inc.', '$279.51 ', '$279.51 ', 'EML']
# ['Warner Bros. Pictures Inc.', '$98.74 ', '$98.74 ', 'LBI']
# ['', '', '$5,250.68 ', 'EML']
# ['', '', '$11,474.46 ', 'LBI']
# ['', '', '$31.62 ', 'LehBod']