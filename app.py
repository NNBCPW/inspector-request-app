
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- Custom Dropdowns for Specific Items ---
custom_dropdown_map = {
    "GLOVE SIZE": ['HAVE', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    "VEST SIZE": ['HAVE', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    "JACKET SIZE": ['HAVE', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    "SMART LEVEL BATT TYPE": ['HAVE', 'AA', 'AAA', '9V'],
    "TRUCK MODEL YEAR": ['HAVE', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028'],
    "CABLES NEEDED": ['HAVE', 'USB C to USB C', 'USB A to USB C', 'USB C to Lightning', 'USB A to Lightning']
}

# --- Final Cleaned Lists ---
list1_items = ['SMART LEVEL', "6' LEVEL", 'MEASURING WHEEL', '1" % GUAGE', 'HAMMER CLAW / SLEDGE', 'MEASURING TAPE', 'THEMOMETER', 'BLANK', 'RUBBER BOOTS', "6' FOLDING RULE", 'HARD HAT SUN VISOR', 'TYPE CUSTOM HERE', 'TAPE MEASURE', 'SAFETY BELT', 'HARD HAT', 'GLOVES 2 TYPES', 'SAFETY GLASSES', 'STRING LINE', 'CHAINING PINS', 'PAINT WAND', 'CLEANING SPRAY TOWELS', 'SMART LEVEL BATTERIES', 'SUNGLASSES', 'HIGH VIS WINTER JACKET/COAT', 'HIGH VIS / REFLECTIVE RAIN SUIT', 'HIGH VIS JACKET', 'SHOVELS', '12" ENGINEERING SCALE', 'BROOM', 'LOGITECH BLUETOOTH MOUSE']
list2_items = ['PENS/HIGHLIGHTERS/PENICLS', 'TABLETS SMALL / LARGE', 'STICKY NOTES /  PAGE TABS', 'PAPER CLIPS / BINDER CLIPS', 'BINDER / FOLDERS / PAGE DIVIDERS', 'GRADES BOOKLET', 'EAR PLUGS / EAR PROTECTION', 'BUG SPRAY', 'WHITE OUT', 'SHEET PROTECTORS', 'GATORADE POWDER', 'GOJO HAND CLEANER', 'APPLE IPHONE CHARGER / CABLE', 'COOLING TOWEL', 'Type Custom Here', 'RUNNING BOARDS', 'HEADACHE RACK', 'TOOL BOX', 'LIGHTBAR /CONTROL BOX', 'TRUCK MODEL YEAR?', 'GLOVE SIZE', 'VEST SIZE', 'JACKET SIZE', 'SMART LEVEL BATT TYPE', 'TRUCK MODEL YEAR', 'CABLES NEEDED']
default_dropdown = ['HAVE', 'NEED']

st.title("Inspector Request Form")

# --- Moved Name/Date/Notes into main body for mobile compatibility ---
name = st.text_input("Your Name")
date = st.date_input("Date", value=datetime.today())
notes = st.text_area("Additional Notes")

st.header("Request Items")

# --- List 1 ---
st.subheader("List 1 Items")
list1_selections = {}
for item in list1_items:
    choice = st.selectbox(f"{item}", options=default_dropdown, key=f"list1_{item}")
    list1_selections[item] = choice

# --- List 2 ---
st.subheader("List 2 Items")
list2_selections = {}
for item in list2_items:
    options = custom_dropdown_map.get(item.upper(), default_dropdown)
    choice = st.selectbox(f"{item}", options=options, key=f"list2_{item}")
    list2_selections[item] = choice

# --- Custom Items ---
st.subheader("Custom Items")
custom_items = []
for i in range(1, 4):
    custom = st.text_input(f"Custom Item {i}", key=f"custom_{i}")
    if custom:
        custom_items.append(custom)

# --- PDF Generator ---
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
        if val.upper() == "NEED":
            pdf.cell(200, 10, txt=f"- {item}", ln=True)

    pdf.ln(3)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="List 2 Items Needed:", ln=True)
    pdf.set_font("Arial", size=12)
    for item, val in list2.items():
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

# --- Download Button ---
pdf = generate_pdf(name, date, notes, list1_selections, list2_selections, custom_items)
pdf_bytes = pdf.output(dest='S').encode('latin-1')

file_name = f"{Inspector.lower().replace(' ', '_')}.request.{date.strftime('%Y-%m-%d')}.pdf"
st.download_button("📄 Download and Save PDF Receipt", data=pdf_bytes, file_name=file_name, mime="application/pdf")
