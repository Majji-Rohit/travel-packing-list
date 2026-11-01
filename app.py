
import streamlit as st
from fpdf import FPDF

st.set_page_config(
    page_title="Travel Packing List Generator",
    page_icon="🧳",
    layout="centered"
)


# ---------------------------
# Packing Recommendation Logic
# ---------------------------

def generate_packing_list(days, weather, trip_type, destination):

    essentials = [
        "Passport / ID", "Travel Tickets", "Wallet",
        "Phone", "Phone Charger", "Charging Cable",
        "Power Bank", "Earphones", "Toothbrush",
        "Toothpaste", "Shampoo", "Soap", "Deodorant",
        "Comb", "Sunscreen", "Medications",
        "Hand Sanitizer", "Wet Wipes",
        "Reusable Water Bottle", "Travel Adapter",
        "Small First Aid Kit"
    ]

    clothing = ["Comfortable Shoes"]

    if weather == "Cold":
        clothing += [
            "Jacket", "Sweater", "Gloves",
            "Woolen Socks", "Thermals"
        ]
    elif weather == "Hot":
        clothing += [
            "T-Shirts", "Shorts", "Cap", "Sunglasses"
        ]
    elif weather == "Rainy":
        clothing += [
            "Raincoat", "Umbrella", "Waterproof Shoes"
        ]

    gear = []

    if trip_type == "Business":
        gear += [
            "Formal Shirt", "Laptop",
            "Notepad", "Business Documents"
        ]
    elif trip_type == "Vacation":
        gear += [
            "Camera", "Headphones", "Book", "Snacks"
        ]
    elif trip_type == "Adventure":
        gear += [
            "Hiking Boots", "Backpack",
            "First Aid Kit", "Torch",
            "Water Bottle", "Energy Bars"
        ]

    # Destination-based recommendations

    place = destination.strip().lower()

    if "goa" in place:
        gear += ["Swimwear", "Beach Towel", "Flip-Flops"]
    elif "manali" in place or "shimla" in place:
        gear += ["Thermal Wear", "Gloves", "Winter Cap"]
    elif "tirupati" in place:
        gear += ["Comfortable Walking Shoes", "Modest Clothing"]
    elif "hyderabad" in place:
        gear += ["Comfortable Casual Clothing"]

    # Daily clothing quantities

    per_day = [
        f"Underwear x {days}",
        f"Socks x {days}",
        f"Tops x {days}",
        f"Pants x {days}"
    ]

    return essentials, clothing, gear, per_day


# ---------------------------
# PDF Generation
# ---------------------------

def generate_pdf(destination, days, sections, checked_state):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "Travel Packing Checklist", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Destination: {destination}", ln=True)
    pdf.cell(0, 8, f"Duration: {days} days", ln=True)

    for section_name, items in sections.items():

        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, section_name, ln=True)

        pdf.set_font("Arial", "", 11)

        for index, item in enumerate(items):

            item_key = f"{section_name}_{index}"

            if checked_state[item_key]:
                pdf.cell(0, 8, f"[X] {item}", ln=True)

    return bytes(pdf.output(dest="S").encode("latin-1"))


# ---------------------------
# Application Interface
# ---------------------------

st.title("🧳 Travel Packing List Generator")

st.write(
    "Generate a personalized packing checklist "
    "based on your destination, weather and trip type."
)

st.divider()

st.subheader("Enter Your Trip Details")

with st.form("trip_form"):

    destination = st.text_input(
        "Destination",
        placeholder="Example: Goa, Manali, Tirupati"
    )

    days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=60,
        value=5
    )

    weather = st.selectbox(
        "Weather",
        ["Hot", "Cold", "Rainy"]
    )

    trip_type = st.selectbox(
        "Trip Type",
        ["Vacation", "Business", "Adventure"]
    )

    submitted = st.form_submit_button(
        "Generate Packing List",
        use_container_width=True
    )


# ---------------------------
# Generate Packing List
# ---------------------------

if submitted:

    if not destination.strip():
        st.warning("Please enter your destination.")

    else:

        essentials, clothing, gear, per_day = generate_packing_list(
            days, weather, trip_type, destination
        )

        st.session_state.generated = True
        st.session_state.destination = destination.strip()
        st.session_state.days = days

        st.session_state.sections = {
            "Essentials": essentials,
            "Clothing": clothing,
            "Trip Gear": gear,
            "Daily Clothing": per_day
        }

        st.session_state.checked_state = {}

        for section_name, items in st.session_state.sections.items():

            for index, item in enumerate(items):

                item_key = f"{section_name}_{index}"
                st.session_state.checked_state[item_key] = True


# ---------------------------
# Display Packing Checklist
# ---------------------------

if st.session_state.get("generated", False):

    st.divider()

    st.success(
        f"Packing list generated for {st.session_state.destination}!"
    )

    st.subheader("Your Packing Checklist")

    total_items = sum(
        len(items)
        for items in st.session_state.sections.values()
    )

    for section_name, items in st.session_state.sections.items():

        with st.expander(section_name, expanded=True):

            for index, item in enumerate(items):

                item_key = f"{section_name}_{index}"

                st.session_state.checked_state[item_key] = st.checkbox(
                    item,
                    value=st.session_state.checked_state[item_key],
                    key=item_key
                )

    # Packing progress

    completed_items = sum(
        st.session_state.checked_state.values()
    )

    progress = completed_items / total_items if total_items else 0

    st.divider()
    st.subheader("Packing Progress")

    st.progress(progress)

    st.write(
        f"Completed: {completed_items}/{total_items} items "
        f"({progress * 100:.0f}%)"
    )

    st.write(f"Remaining: {total_items - completed_items} items")

    # Downloads

    st.divider()
    st.subheader("Download Your Packing List")

    col1, col2 = st.columns(2)

    text_content = (
        f"Travel Packing List\n"
        f"Destination: {st.session_state.destination}\n"
        f"Duration: {st.session_state.days} days\n\n"
    )

    for section_name, items in st.session_state.sections.items():

        text_content += f"\n{section_name}\n"
        text_content += "-" * 30 + "\n"

        for index, item in enumerate(items):

            item_key = f"{section_name}_{index}"

            if st.session_state.checked_state[item_key]:
                text_content += f"- {item}\n"

    if any(st.session_state.checked_state.values()):

        with col1:
            st.download_button(
                "Download TXT",
                data=text_content,
                file_name="travel_packing_list.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:
            pdf_data = generate_pdf(
                st.session_state.destination,
                st.session_state.days,
                st.session_state.sections,
                st.session_state.checked_state
            )

            st.download_button(
                "Download PDF",
                data=pdf_data,
                file_name="travel_packing_list.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    else:
        st.info("Select at least one item to download your packing list.")
