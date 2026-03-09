import streamlit as st

st.set_page_config(page_title="Travel Packing List Generator", page_icon="🧳")

# ---------------------------
# Packing Logic
# ---------------------------
def generate_packing_list(days, weather, trip_type):

    essentials = [
        "Passport / ID",
        "Wallet",
        "Phone",
        "Phone Charger",
        "Power Bank",
        "Toothbrush",
        "Toothpaste",
        "Shampoo",
        "Soap",
        "Deodorant",
        "Comb",
        "Sunscreen",
        "Medications",
        "Travel Tickets"
    ]

    clothing = []
    if weather == "Cold":
        clothing += ["Jacket", "Sweater", "Gloves", "Woolen Socks", "Thermals"]
    elif weather == "Hot":
        clothing += ["T-Shirts", "Shorts", "Cap", "Sunglasses"]
    elif weather == "Rainy":
        clothing += ["Raincoat", "Umbrella", "Waterproof Shoes"]

    gear = []
    if trip_type == "Business":
        gear += ["Formal Shirt", "Laptop", "Notepad", "Business Documents"]
    elif trip_type == "Vacation":
        gear += ["Camera", "Headphones", "Book", "Snacks"]
    elif trip_type == "Adventure":
        gear += ["Hiking Boots", "First Aid Kit", "Torch", "Water Bottle"]

    per_day = [
        f"Underwear x {days}",
        f"Socks x {days}",
        f"Tops x {days}",
        f"Pants x {days}"
    ]

    return essentials, clothing, gear, per_day


# ---------------------------
# UI
# ---------------------------
st.title("🧳 Travel Packing List Generator")
st.write("Enter your trip details to generate a personalized packing checklist.")

with st.form("trip_form"):
    destination = st.text_input("Destination")
    days = st.number_input("Number of Days", min_value=1, max_value=60, value=5)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    submitted = st.form_submit_button("Generate Packing List")


# ---------------------------
# Generate Packing List
# ---------------------------
if submitted:

    if destination.strip() == "":
        st.warning("Please enter destination.")
    else:

        st.session_state.generated = True
        st.session_state.destination = destination

        essentials, clothing, gear, per_day = generate_packing_list(days, weather, trip_type)

        st.session_state.sections = {
            "Essentials": essentials,
            "Clothing": clothing,
            "Trip Gear": gear,
            "Daily Clothing": per_day
        }

        st.session_state.checked_state = {}

        for section in st.session_state.sections.values():
            for item in section:
                st.session_state.checked_state[item] = True

        st.session_state.select_all = True


# ---------------------------
# Select All Toggle
# ---------------------------
def toggle_select_all():
    for item in st.session_state.checked_state:
        st.session_state.checked_state[item] = st.session_state.select_all


# ---------------------------
# Display Packing List
# ---------------------------
if "generated" in st.session_state:

    st.success(f"Packing list for {st.session_state.destination}")

    st.checkbox(
        "Select All",
        key="select_all",
        on_change=toggle_select_all
    )

    st.write("## Packing Checklist")

    for section_name, items in st.session_state.sections.items():

        if items:
            st.subheader(section_name)

            for item in items:

                st.session_state.checked_state[item] = st.checkbox(
                    item,
                    value=st.session_state.checked_state[item],
                    key=item
                )

    selected_items = [
        item for item, checked in st.session_state.checked_state.items() if checked
    ]

    st.write(f"Total Selected Items: {len(selected_items)}")

    if selected_items:

        numbered_items = "\n".join(
            [f"{i+1}. {item}" for i, item in enumerate(selected_items)]
        )

        file_content = f"""Packing List
-----------------------

{numbered_items}
"""

        st.download_button(
            label="Download Packing List",
            data=file_content,
            file_name="packing_list.txt",
            mime="text/plain"
        )
