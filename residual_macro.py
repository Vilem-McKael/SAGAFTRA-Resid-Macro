import csv

def macro(date, residual_data_filepath, new_filename):

    with open(residual_data_filepath, 'r') as f:
        count_reader = csv.reader(f)
        count = sum(1 for row in count_reader)
        f.seek(0)
        reader = csv.reader(f)

        new_file = open(f'results/{new_filename}', 'w')
        new_file.write(f'\ufeff"{date}",,,\n')
        new_file.write("Company,Gross,Net,Corp\n")

        # corp changer dict
        corp_name_changer_dict = {
            "E M L PRODS": "EML",
            "LEHBOD INC": "LBI",
            "Edie Lehmann Boddicker": "LehBod"
        }

        # summary vars
        processed_check_identifiers = []
        net_totals = {}

        # processing
        for row in reader:
            print(reader.line_num)

            if reader.line_num == 1:
                print('here')
                continue

            if reader.line_num == count:
                print("finished: line_num:", reader.line_num, " count: ", count)
                is_finished = True

            print(row[8])
            check_no = row[8]
            current_company = row[3]
            unique_check_identifier = f"{check_no}-{current_company}"

            if unique_check_identifier in processed_check_identifiers:
                print('check already processed, continuing')
                continue
            else:
                print('new check')

                processed_check_identifiers.append(unique_check_identifier)
                current_corp = corp_name_changer_dict[row[1]]


                print('gross: ', row[10], 'net: ', row[11])
                current_gross = float(row[10].replace('$', ''))
                current_net = float(row[11].replace('$', ''))


                new_file.write(f'"{current_company}","${current_gross:,.2f}","${current_net:,.2f}","{current_corp}"\n')
                net_totals[current_corp] = net_totals.get(current_corp, 0) + current_net

            print(row)

        for k, v in net_totals.items():
            new_file.write(f',,"${format(round(v, 2), ',')}", {k}\n')

macro('Jan 27 2026', 'data/residuals1-27-26.csv', '1-27-26 Residuals.csv')