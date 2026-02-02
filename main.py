import csv
import streamlit as st
import io
from datetime import datetime

def main(date_str: str, upload_bytes: bytes):
    f = io.TextIOWrapper(io.BytesIO(upload_bytes), encoding="utf-8", newline="")

    count_reader = csv.reader(f)
    count = sum(1 for row in count_reader)
    f.seek(0)
    reader = csv.reader(f)

    out_bytes = io.BytesIO()
    out = io.TextIOWrapper(out_bytes, encoding="utf-8", newline="")

    out.write(f'\ufeff"{date_str}",,,\n')
    out.write("Company,Gross,Net,Corp\n")

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


            out.write(f'"{current_company}","${current_gross:,.2f}","${current_net:,.2f}","{current_corp}"\n')
            net_totals[current_corp] = net_totals.get(current_corp, 0) + current_net

        print(row)

    for k, v in net_totals.items():
        out.write(f',,"${format(round(v, 2), ',')}", {k}\n')

    out.flush()
    return out_bytes.getvalue()

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