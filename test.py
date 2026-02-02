import csv
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



main('Jan 30 2026', 'data/residuals1-30-26.csv', '1-30-26 Residuals.csv')