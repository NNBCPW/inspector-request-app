
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 🔧 MANUAL ITEM ADDITIONS HERE (Optional) ---
custom_items_config = {
    "TRUCK MODEL YEAR": ["2018", "2019", "2020", "2021", "2022", "2023"],
    "JACKET SIZE": ["SM", "MED", "LARGE", "XL", "XXL"],
    "COOLING TOWEL": ["HAVE", "NEED"]
}


# Sample item data (will be replaced by real lists)
list1_items = [
    "SMART LEVEL", "6' LEVEL", "MEASURING WHEEL", "1\" % GUAGE", "HAMMER CLAW / SLEDGE"
]

list2_items = [
    "PENS/HIGHLIGHTERS/PENCILS", "TABLETS SMALL / LARGE", "STICKY NOTES / PAGE TABS",
    "GLOVE SIZE", "VEST SIZE"
]

size_options = ["HAVE", "NEED", "SMALL", "MED", "LARGE", "XL", "XXL"]

st.title("Inspector Request Form")

# --- User Info ---
with st.sidebar:
    name = st.text_input("Your Name")
    date = st.date_input("Date", value=datetime.today())
    notes = st.text_area("Additional Notes")

st.header("Request Items")

# --- List 1 ---
st.subheader("List 1 Items")
list1_selections = {}
for item in list1_items:
    choice = st.selectbox(f"{item}", options=size_options, key=f"list1_{item}")
    list1_selections[item] = choice

# --- List 2 ---
st.subheader("List 2 Items")
list2_selections = {}
for item in list2_items:
    choice = st.selectbox(f"{item}", options=size_options, key=f"list2_{item}")
    list2_selections[item] = choice


# --- Manual Items (Optional) ---
st.subheader("Additional Manual Items")
manual_selections = {}
for item, options in custom_items_config.items():
    choice = st.selectbox(f"{item}", options=options, key=f"manual_{item}")
    manual_selections[item] = choice

# --- Custom Items ---
st.subheader("Custom Items")
custom_items = []
for i in range(1, 4):
    custom = st.text_input(f"Custom Item {i}", key=f"custom_{i}")
    if custom:
        custom_items.append(custom)

# --- Generate PDF ---
def generate_pdf(name, date, notes, list1, list2, customs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Inspector Request Receipt", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date.strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="List 1 Items Needed:", ln=True)
    pdf.set_font("Arial", size=12)
    for item, val in list1.items():
        if val.upper() != "HAVE":
            pdf.cell(200, 10, txt=f"- {item}: {val}", ln=True)

    pdf.ln(3)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="List 2 Items Needed:", ln=True)
    pdf.set_font("Arial", size=12)
    for item, val in list2.items():
        if val.upper() != "HAVE":
            pdf.cell(200, 10, txt=f"- {item}: {val}", ln=True)


    pdf.ln(3)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Additional Manual Items:", ln=True)
    pdf.set_font("Arial", size=12)
    for item, val in manual_selections.items():
        if val.upper() != "HAVE":
            pdf.cell(200, 10, txt=f"- {item}: {val}", ln=True)


    if customs:
        pdf.ln(3)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Custom Items:", ln=True)
        pdf.set_font("Arial", size=12)
        for c in customs:
            pdf.cell(200, 10, txt=f"- {c}", ln=True)

    if notes:
        pdf.ln(3)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Notes:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=notes)

    return pdf

# --- Save Button ---
if st.button("📄 Download PDF Receipt"):
    pdf = generate_pdf(name, date, notes, list1_selections, list2_selections, custom_items)
    pdf_output = "inspector_request.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        st.download_button("Download PDF", f, file_name=pdf_output)
