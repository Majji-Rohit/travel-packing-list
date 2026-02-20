import streamlit as st

st.set_page_config(page_title="Travel Packing List Generator", page_icon="🧳")

# ---------------------------
# Packing Logic Function
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

    return essentials + clothing + gear + per_day


# ---------------------------
# UI
# ---------------------------
st.title("🧳 Travel Packing List Generator")
st.write("Fill the details and generate your customized list.")

with st.form("trip_form"):
    destination = st.text_input("Destination")
    days = st.number_input("Number of Days", min_value=1, max_value=60, value=5)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    submitted = st.form_submit_button("Generate Packing List")


# ---------------------------
# Display Packing List
# ---------------------------
if submitted:

    if destination.strip() == "":
        st.warning("Please enter destination.")
    else:
        st.success(f"Packing list for {destination}")

        packing_items = generate_packing_list(days, weather, trip_type)

        # Initialize session state
        if "packing_list" not in st.session_state:
            st.session_state.packing_list = packing_items

        if "checked_state" not in st.session_state:
            st.session_state.checked_state = {
                item: True for item in packing_items
            }

        # SELECT ALL
        select_all = st.checkbox("Select All", value=True)

        if select_all:
            for item in st.session_state.checked_state:
                st.session_state.checked_state[item] = True
        else:
            for item in st.session_state.checked_state:
                st.session_state.checked_state[item] = False

        st.write("### Your Packing List")

        # Display checkboxes
        for item in st.session_state.packing_list:
            st.session_state.checked_state[item] = st.checkbox(
                item,
                value=st.session_state.checked_state[item],
                key=item
            )

        # Collect selected items
        selected_items = [
            item
            for item, checked in st.session_state.checked_state.items()
            if checked
        ]

        st.write(f"Total Selected Items: {len(selected_items)}")

        # Download selected items only
        if selected_items:
            file_content = "\n".join(selected_items)

            st.download_button(
                label="Download",
                data=file_content,
                file_name="packing_list.txt",
                mime="text/plain"
            )
