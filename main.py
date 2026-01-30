import streamlit as st
import csv
from io import StringIO
from typing import Dict, List, Optional


def money_to_float(x: str) -> float:
    """Convert things like '$1,234.56' or '($12.00)' to float."""
    if x is None:
        return 0.0
    s = str(x).strip()
    if not s:
        return 0.0

    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1]

    s = s.replace("$", "").replace(",", "").strip()
    try:
        val = float(s)
    except ValueError:
        val = 0.0

    return -val if negative else val


def transform_csv(date_str: str, input_csv_text: str) -> bytes:
    """
    Takes input CSV text, returns output CSV bytes (utf-8 with BOM) for download.
    """
    # Read input rows
    reader = csv.reader(StringIO(input_csv_text))
    rows = list(reader)

    if not rows:
        # Empty file
        out = "\ufeff" + f"{date_str},,,\n" + "Company,Gross,Net,Corp\n"
        return out.encode("utf-8")

    # Skip header row (your original code skipped line 1)
    data_rows = rows[1:] if len(rows) > 1 else []

    # Prepare output in memory
    out_buf = StringIO()
    out_buf.write("\ufeff")  # Excel-friendly BOM
    writer = csv.writer(out_buf, lineterminator="\n")

    writer.writerow([date_str, "", "", ""])
    writer.writerow(["Company", "Gross", "Net", "Corp"])

    current_check_no: Optional[str] = None
    current_company = ""
    current_corp = ""
    sum_gross = 0.0
    sum_net = 0.0

    net_totals: Dict[str, float] = {}

    def flush_group():
        nonlocal sum_gross, sum_net, current_company, current_corp
        if current_check_no is None:
            return
        writer.writerow([current_company, f"{sum_gross:.2f}", f"{sum_net:.2f}", current_corp])
        net_totals[current_corp] = net_totals.get(current_corp, 0.0) + sum_net

    for row in data_rows:
        if not row:
            continue

        # Defensive: make sure indexes exist
        # You use row[0], row[1], row[3], row[10], row[11]
        if len(row) <= 11:
            continue

        check_no = row[0].strip()

        gross = money_to_float(row[10])
        net = money_to_float(row[11])

        if current_check_no is None:
            # first group
            current_check_no = check_no
            current_corp = row[1].strip()
            current_company = row[3].strip()
            sum_gross = gross
            sum_net = net
            continue

        if check_no == current_check_no:
            sum_gross += gross
            sum_net += net
        else:
            # new check_no => write previous group, start new group
            flush_group()
            current_check_no = check_no
            current_corp = row[1].strip()
            current_company = row[3].strip()
            sum_gross = gross
            sum_net = net

    # Flush last group
    flush_group()

    # Summary rows (your original wrote: '', '', {v}, {k}
    for corp, total_net in net_totals.items():
        writer.writerow(["", "", f"{total_net:.2f}", corp])

    return out_buf.getvalue().encode("utf-8")


# ---------------- Streamlit UI ----------------

st.title("CSV Macro")

date_str = st.text_input("Date", "Jul 10 2025")
uploaded = st.file_uploader("Upload residuals CSV", type=["csv"])

if uploaded is not None:
    # Read bytes -> text
    input_text = uploaded.getvalue().decode("utf-8-sig", errors="replace")

    if st.button("Run"):
        output_bytes = transform_csv(date_str, input_text)

        st.download_button(
            label="Download result CSV",
            data=output_bytes,
            file_name="result.csv",
            mime="text/csv",
        )
