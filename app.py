import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Travel Packing List Generator",
    page_icon="🧳",
    layout="centered"
)

# Title
st.title("🧳 Travel Packing List Generator")
st.markdown("Plan smarter, pack lighter. Generate a customized packing checklist based on your trip details.")

# Function to generate packing list
def generate_packing_list(destination, days, weather, trip_type):

    essentials = [
        "🪪 Passport / ID",
        "📱 Phone & Charger",
        "💳 Wallet",
        "🪥 Toothbrush",
        "🧴 Toiletries",
        "🧼 Deodorant",
        "🔋 Power Bank"
    ]

    clothing = []

    if weather == "Cold":
        clothing.extend([
            "🧥 Jacket",
            "🧣 Thermal Wear",
            "🧦 Woolen Socks",
            "🧤 Gloves"
        ])

    elif weather == "Hot":
        clothing.extend([
            "👕 T-Shirts",
            "🩳 Shorts",
            "🧢 Cap",
            "😎 Sunglasses"
        ])

    elif weather == "Rainy":
        clothing.extend([
            "☔ Umbrella",
            "🧥 Raincoat",
            "🥾 Waterproof Shoes"
        ])

    gear = []

    if trip_type == "Business":
        gear.extend([
            "👔 Formal Wear",
            "💼 Laptop",
            "📝 Notepad",
            "🪪 Business Cards"
        ])

    elif trip_type == "Vacation":
        gear.extend([
            "📷 Camera",
            "🎧 Headphones",
            "📖 Book / Kindle",
            "🍪 Snacks"
        ])

    elif trip_type == "Adventure":
        gear.extend([
            "🥾 Hiking Boots",
            "🩹 First-Aid Kit",
            "🚰 Water Bottle",
            "🔦 Torch",
            "🍫 Energy Bars"
        ])

    daily_items = [
        f"👕 Tops x {days}",
        f"👖 Bottoms x {days}",
        f"🧦 Socks x {days}",
        f"👚 Innerwear x {days}"
    ]

    return essentials, clothing, gear, daily_items


# Form
with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g. Manali, Paris")
    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=60, value=3)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])

    submitted = st.form_submit_button("Generate Packing List")

# When user submits
if submitted:

    if destination.strip() == "":
        st.error("Please enter a destination.")
    else:
        st.success(f"Packing list for {destination} ({days} days | {weather} | {trip_type})")

        essentials, clothing, gear, daily_items = generate_packing_list(
            destination, days, weather, trip_type
        )

        st.markdown("### 🧰 Essentials")
        for item in essentials:
            st.checkbox(item)

        st.markdown("### 👕 Clothing")
        for item in clothing:
            st.checkbox(item)

        if gear:
            st.markdown(f"### 🎒 {trip_type} Gear")
            for item in gear:
                st.checkbox(item)

        st.markdown("### 📅 Per-Day Clothing")
        for item in daily_items:
            st.checkbox(item)

        st.markdown("---")

        # Download feature
        full_list = essentials + clothing + gear + daily_items
        text_output = "\n".join(full_list)

        st.download_button(
            label="📄 Download Packing List",
            data=text_output,
            file_name=f"{destination}_packing_list.txt",
            mime="text/plain"
        )

        st.info("💡 Tip: Roll clothes to save space and reduce wrinkles.")
