
import streamlit as st
from fpdf import FPDF
from datetime import datetime
import smtplib
from email.message import EmailMessage

# --- Items ---
list1_items = [
    "SMART LEVEL", "6' LEVEL", "MEASURING WHEEL", "1\" % GUAGE", "HAMMER CLAW / SLEDGE"
]

list2_items = [
    "TOOL BOX", "LIGHTBAR /CONTROL BOX", "TRUCK MODEL YEAR", "CABLES NEEDED"
]

st.set_page_config(page_title="Inspector Request", layout="centered")
st.title("Inspector Request Form")

name = st.text_input("Your Name")
date = st.date_input("Date", value=datetime.today())

# --- Button Pair Function ---
def toggle_buttons(item_key):
    if f"{item_key}_selection" not in st.session_state:
        st.session_state[f"{item_key}_selection"] = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ HAVE" if st.session_state[f"{item_key}_selection"] == "HAVE" else "HAVE", key=f"{item_key}_have"):
            st.session_state[f"{item_key}_selection"] = "HAVE"
    with col2:
        if st.button("✅ NEED" if st.session_state[f"{item_key}_selection"] == "NEED" else "NEED", key=f"{item_key}_need"):
            st.session_state[f"{item_key}_selection"] = "NEED"

    return st.session_state[f"{item_key}_selection"]

# --- List 1 ---
st.subheader("List 1 Items")
list1_selections = {}
for item in list1_items:
    st.markdown(f"**{item}**")
    list1_selections[item] = toggle_buttons(item.replace(" ", "_").lower())

# --- List 2 ---
st.subheader("List 2 Items")
list2_selections = {}
for item in list2_items:
    st.markdown(f"**{item}**")
    list2_selections[item] = toggle_buttons(item.replace(" ", "_").lower())

# --- Custom Items ---
st.subheader("Custom Items")
custom_items = []
for i in range(1, 4):
    val = st.text_input(f"Custom Item {i}")
    if val:
        custom_items.append(val)

# --- Notes and Email ---
st.subheader("Additional Notes")
notes = st.text_area("Type any extra notes here")
cc_email = st.text_input("Optional: CC another email")

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
        if val == "NEED":
            pdf.cell(200, 10, txt=f"- {item}", ln=True)

    pdf.ln(3)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="List 2 Items Needed:", ln=True)
    pdf.set_font("Arial", size=12)
    for item, val in list2.items():
        if val == "NEED":
            pdf.cell(200, 10, txt=f"- {item}", ln=True)

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

# --- Submit & Email ---
if st.button("📧 Submit and Email PDF"):
    pdf = generate_pdf(name, date, notes, list1_selections, list2_selections, custom_items)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    filename = f"{name.lower().replace(' ', '_')}.request.{date.strftime('%Y-%m-%d')}.pdf"

    msg = EmailMessage()
    msg["Subject"] = f"{name}.{date.strftime('%d.%m.%Y')}.suppliesrequestreceipt"
    msg["From"] = "nickbexarinspector@gmail.com"
    recipients = ["nicholas.nabholz@bexar.org"]
    if cc_email:
        recipients.append(cc_email.strip())
    msg["To"] = ", ".join(recipients)
    msg.set_content("Attached is the Inspector Request Form PDF.")
    msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename=filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("nickbexarinspector@gmail.com", "szwg fmcv moih jufh")
            smtp.send_message(msg)
        st.success(f"PDF emailed to: {', '.join(recipients)}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
