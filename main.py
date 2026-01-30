import streamlit as st
import csv
from io import StringIO
from datetime import datetime


def main(date_str: str, csv_text: bytes) -> bytes:
    f = StringIO(uploaded_bytes.decode("utf-8-sig"), newline="")

    reader_for_count = csv.reader(csv_text)
    rows = list(reader_for_count)
    f.seek(0)
    count = len(rows)

    # Now iterate like your second pass
    reader_rows = rows  # reuse

    out = StringIO()

    # Preserve your exact header output style
    out.write("\ufeff")  # BOM
    out.write(f"{date_str}, '', '', ''\n")
    out.write("'Company', 'Gross', 'Net', 'Corp'")  # NOTE: no newline in your original

    # iteration vars
    current_check_no = False
    current_company = ""
    sum_gross = 0.0
    sum_net = 0.0
    current_corp = ""

    # summary vars
    is_finished = False
    net_totals = {}

    # processing
    for line_num, row in enumerate(reader_rows, start=1):
        # mimic: if reader.line_num == 1: continue
        if line_num == 1:
            continue

        # mimic: if reader.line_num == count: is_finished = True
        if line_num == count:
            is_finished = True

        # Guard against short/blank rows (prevents index errors)
        if not row or len(row) <= 11:
            continue

        check_no = row[0]

        if check_no == current_check_no:
            sum_gross += float(row[10].replace("$", ""))
            sum_net += float(row[11].replace("$", ""))
        else:
            if current_check_no:
                out.write(f"{current_company}, {sum_gross}, {sum_net}, {current_corp}\n")
                net_totals[current_corp] = net_totals.get(current_corp, 0) + sum_net

            current_check_no = check_no
            current_corp = row[1]
            current_company = row[3]
            sum_gross = float(row[10].replace("$", ""))
            sum_net = float(row[11].replace("$", ""))

            if is_finished:
                out.write(f"{current_company}, {sum_gross}, {sum_net}, {current_corp}\n")
                net_totals[current_corp] = net_totals.get(current_corp, 0) + float(sum_net)

        if is_finished:
            for k, v in net_totals.items():
                out.write(f"'', '', {v}, {k}\n")

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