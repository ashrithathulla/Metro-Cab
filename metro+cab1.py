import streamlit as st
import qrcode
from io import BytesIO
import uuid


# ---------------- QR GENERATION FUNCTION ----------------
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

s# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="METRO TICKET BOOKING", layout="centered")
st.title(" Metro Ticket Booking System")

stations = ["Ameerpet", "Miyapur", "LB Nagar", "KPHP", "JNTU"]

# ---------------- USER INPUTS ----------------
name = st.text_input("Passenger Name")
source = st.selectbox("From Station", stations)
destination = st.selectbox("To Station", stations)
tickets = st.number_input("Tickets", min_value=1, value=1)

# Cab Requirement
st.subheader("Do you need a Cab?")
cab_required = st.radio("", ["NO", "YES"], horizontal=True)

drop_location = ""
cab_charge = 0

if cab_required == "YES":
    drop_location = st.text_input("Enter Drop Location")
    cab_charge = 100 if cab_required == "YES" else 0


# ---------------- PRICE CALCULATION ----------------
ticket_price = 30
metro_amount = tickets * ticket_price
total_amount = metro_amount + cab_charge

st.info(f" Total Amount: {total_amount}")

# ---------------- BOOK BUTTON ----------------
if st.button("Book"):
    if name.strip() == "":
        st.error("Please enter passenger name")
    elif source == destination:
        st.error("From and To stations cannot be same")
    elif cab_required == "YES" and drop_location.strip() == "":
        st.error("Please enter drop location")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {tickets}\n"
            f"Cab: {cab_required}\n"
            f"Drop: {drop_location if cab_required == 'YES' else 'N/A'}\n"
            f"Total Amount:{total_amount}"
        )

        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")

        st.success("Booking Successful!")

        # ---------------- DETAILS OUTPUT ----------------
        st.subheader(" Ticket Details")
        st.write(f"*Booking ID:* {booking_id}")
        st.write(f"*Passenger:* {name}")
        st.write(f"*Route:* {source}{destination}")
        st.write(f"*Tickets:* {tickets}")

        if cab_required == "YES":
            st.write("*Cab Booked*")
            st.write(f"*Drop Location:* {drop_location}")
        else:
            st.write("*Metro Ticket Only*")

        st.write(f"*Total Paid:* {total_amount}")

        st.image(buf.getvalue(),width=250)

