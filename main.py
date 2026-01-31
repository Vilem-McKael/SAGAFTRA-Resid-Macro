import streamlit as st
import csv
from io import StringIO
from datetime import datetime


def main(date_str: str, csv_text: bytes) -> bytes:
    f = StringIO(csv_text.decode("utf-8-sig"), newline="")

    count_reader = csv.reader(f)
    count = sum(1 for row in count_reader)
    f.seek(0)
    reader = csv.reader(f)

    out = StringIO()
    writer = csv.writer(out)  # Create a CSV writer

    # Write BOM manually, then use writer for CSV rows
    out.write("\ufeff")
    writer.writerow([date_str, '', '', ''])
    writer.writerow(['Company', 'Gross', 'Net', 'Corp'])

    # iteration vars
    current_check_no = False
    current_company = ""
    sum_gross = 0.0
    sum_net = 0.0
    current_corp = ""

    # summary vars
    net_totals = {}

    # processing
    for row in reader:
        print(reader.line_num)

        if reader.line_num == 1:
            print('here')
            continue

        print(row[0])
        check_no = row[0]

        if check_no == current_check_no:
            print('adding sums')
            sum_gross += float(row[10].replace('$', ''))
            sum_net += float(row[11].replace('$', ''))
        else:
            print('new check')
            if current_check_no:
                writer.writerow([current_company, sum_gross, sum_net, current_corp])
                net_totals[current_corp] = net_totals.get(current_corp, 0) + sum_net

            current_check_no = check_no
            current_corp = row[1]
            current_company = row[3]
            print('gross: ', row[10], 'net: ', row[11])
            sum_gross = float(row[10].replace('$', ''))
            sum_net = float(row[11].replace('$', ''))

        print(row)

    # Write the last check's data
    if current_check_no:
        writer.writerow([current_company, sum_gross, sum_net, current_corp])
        net_totals[current_corp] = net_totals.get(current_corp, 0) + sum_net

    # Write summary totals
    for k, v in net_totals.items():
        writer.writerow(['', '', v, k])

    return out.getvalue().encode("utf-8")

# ---------------- Streamlit UI ----------------

st.title("SAG-AFTRA Residual Macro")

date_string = st.text_input("Date (first line)", datetime.today().strftime('%Y-%m-%d'))
uploaded = st.file_uploader("Upload residuals CSV", type=["csv"])

# Optional: let the user choose the download file name
download_name = "Residuals" + datetime.today().strftime('%Y-%m-%d')

if uploaded is not None:
    # Use utf-8-sig to gracefully handle BOM if your input CSV has one
    uploaded_bytes = uploaded.getvalue()  # from st.file_uploader

    if st.button("Run"):
        output_bytes = main(date_string, uploaded_bytes)

        st.download_button(
            label="Download modified CSV",
            data=output_bytes,
            file_name=f"{download_name}.csv",
            mime="text/csv",
        )