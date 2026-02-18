import streamlit as st


def generate_packing_list(destination, days, weather, trip_type):
    essentials = [
        "Passport/ID",
        "Phone & Charger",
        "Wallet",
        "Toothbrush",
        "Shampoo",
        "Sunscreen",
        "Deodorant",
        "Comb",
        "Power Bank"
    ]

    clothing = []
    if weather == "Cold":
        clothing.extend(["Gloves", "Jacket", "Woolen Socks", "Thermal Wear"])
    elif weather == "Hot":
        clothing.extend(["Cap", "Sunglasses", "T-Shirts", "Shorts"])
    elif weather == "Rainy":
        clothing.extend(["Umbrella", "Raincoat", "Waterproof Shoes"])

    gear = []
    if trip_type == "Business":
        gear.extend(["Formal Shirt", "Laptop", "Notepad", "Business Cards"])
    elif trip_type == "Vacation":
        gear.extend(["Camera", "Headphones", "Book/Kindle", "Snacks"])
    elif trip_type == "Adventure":
        gear.extend([
            "Hiking Boots",
            "First-Aid Kit",
            "Water Bottle",
            "Torch",
            "Energy Bars"
        ])

    daily_items = ["Underwear", "Socks", "Tops", "Pants"]
    per_day = [f"{item} x {days}" for item in daily_items]

    return essentials, clothing, gear, per_day


# ------------------ Streamlit UI ------------------

st.set_page_config(
    page_title="Travel Packing List",
    page_icon="🧳",
    layout="centered"
)

st.title("Travel Packing List Generator")
st.write("Generate a customized packing checklist based on your trip details.")

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g., Manali, Paris")
    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=60, value=5)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    submitted = st.form_submit_button("Generate Packing List")

if submitted:
    st.success(f"Packing list for {destination} ({days} days)")

    essentials, clothing, gear, per_day = generate_packing_list(
        destination, days, weather, trip_type
    )

    st.subheader("Essentials")
    for item in essentials:
        st.checkbox(item)

    if clothing:
        st.subheader("Clothing")
        for item in clothing:
            st.checkbox(item)

    if gear:
        st.subheader(f"{trip_type} Gear")
        for item in gear:
            st.checkbox(item)

    st.subheader("Per-Day Items")
    for item in per_day:
        st.checkbox(item)

    st.divider()
    st.info("Tip: Roll clothes to save space and avoid wrinkles.")
