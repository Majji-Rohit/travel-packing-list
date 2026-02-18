import streamlit as st
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Smart Travel Packing List", page_icon="🧳")
st.title("🧳 Smart Travel Packing List Generator")

# ---------------- FUNCTION ----------------
def generate_packing_list(days, weather, trip_type, travel_type, gender):

    essentials = [
        "Passport / ID",
        "Travel Tickets",
        "Wallet",
        "Emergency Contacts",
        "Phone",
        "Phone Charger",
        "Power Bank",
        "Toothbrush",
        "Toothpaste",
        "Medications",
        "First-Aid Kit"
    ]

    # Travel type logic
    if travel_type == "International":
        essentials.append("Visa Documents")
        essentials.append("Currency Exchange")

    # Weather logic
    weather_items = {
        "Cold": ["Jacket", "Gloves", "Thermal Wear", "Woolen Socks"],
        "Hot": ["T-Shirts", "Shorts", "Sunglasses", "Cap", "Sunscreen"],
        "Rainy": ["Raincoat", "Umbrella", "Waterproof Shoes"]
    }

    # Trip type logic
    trip_items = {
        "Business": ["Formal Shirt", "Formal Shoes", "Laptop", "Notebook"],
        "Vacation": ["Camera", "Headphones", "Snacks"],
        "Adventure": ["Hiking Boots", "Energy Bars", "Torch"]
    }

    # Gender specific items
    gender_items = {
        "Male": ["Shaving Kit"],
        "Female": ["Makeup Kit", "Hair Accessories"]
    }

    # Per-day clothing
    per_day = [
        f"Underwear x {days}",
        f"Socks x {days}",
        f"Tops x {days}",
        f"Pants x {days}"
    ]

    full_list = (
        essentials
        + weather_items[weather]
        + trip_items[trip_type]
        + gender_items[gender]
        + per_day
    )

    return full_list


# ---------------- FORM ----------------
with st.form("trip_form"):
    destination = st.text_input("Destination")
    days = st.number_input("Trip Duration (Days)", 1, 60, 5)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    travel_type = st.selectbox("Travel Type", ["Domestic", "International"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    submitted = st.form_submit_button("Generate Packing List")


# ---------------- DISPLAY ----------------
if submitted:

    if destination.strip() == "":
        st.warning("Please enter destination.")
    else:
        st.success(f"Packing list for {destination}")

        items = generate_packing_list(days, weather, trip_type, travel_type, gender)

        select_all = st.checkbox("Select All", value=True)

        selected_items = []

        for i, item in enumerate(items):
            checked = st.checkbox(item, value=select_all, key=f"item_{i}")
            if checked:
                selected_items.append(item)

        st.markdown(f"### Total Selected Items: {len(selected_items)}")

        # --------- PDF DOWNLOAD ---------
        def create_pdf(items_list):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Travel Packing List", ln=True)
            pdf.ln(5)

            for item in items_list:
                pdf.cell(200, 8, txt=f"- {item}", ln=True)

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(temp_file.name)
            return temp_file.name

        if selected_items:
            pdf_path = create_pdf(selected_items)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name="packing_list.pdf",
                    mime="application/pdf"
                )
