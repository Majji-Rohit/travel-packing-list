
import streamlit as st

def generate_packing_list(destination, days, weather, trip_type):
    essentials = [
        "🪪 Passport/ID", "📱 Phone & Charger", "💳 Wallet", "🪥 Toothbrush", 
        "🧴 Shampoo", "🧴 Sunscreen", "🧼 Deodorant", "🪞 Comb", "🔋 Power Bank"
    ]

    clothing = []
    if weather == "Cold":
        clothing += ["🧤 Gloves", "🧥 Jacket", "🧦 Woolen Socks", "🧣 Thermal Wear"]
    elif weather == "Hot":
        clothing += ["🧢 Cap", "😎 Sunglasses", "👕 T-Shirts", "🩳 Shorts"]
    elif weather == "Rainy":
        clothing += ["☔ Umbrella", "🧥 Raincoat", "🥾 Waterproof Shoes"]

    gear = []
    if trip_type == "Business":
        gear += ["👔 Formal Shirt", "💼 Laptop", "📝 Notepad", "🪪 Business Cards"]
    elif trip_type == "Vacation":
        gear += ["📷 Camera", "🎧 Headphones", "📖 Book/Kindle", "🍪 Snacks"]
    elif trip_type == "Adventure":
        gear += ["🥾 Hiking Boots", "🩹 First-Aid Kit", "🚰 Water Bottle", "🔦 Torch", "🍫 Energy Bars"]

    daily_items = ["👚 Underwear", "🧦 Socks", "👕 Tops", "👖 Pants"]
    per_day = [f"{item} x {days}" for item in daily_items]

    full_list = essentials + clothing + gear + per_day
    unique_list = list(set(full_list))  # Remove duplicates
    return essentials, clothing, gear, per_day, unique_list

st.set_page_config(page_title="Travel Packing List Generator", page_icon="🧳")
st.title("🧳 Travel Packing List Generator")
st.markdown("Plan smarter, pack lighter. Enter your trip details below:")

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g. Manali, Paris")
    days = st.number_input("Trip Duration (in Days)", min_value=1, max_value=60, value=5)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    submitted = st.form_submit_button("Generate Packing List")

if submitted:
    st.success(f"Packing list for {destination} ({days} days, {weather} weather, {trip_type} trip):")

    essentials, clothing, gear, per_day, _ = generate_packing_list(destination, days, weather, trip_type)

    st.markdown("### 🧰 Essentials")
    for item in essentials:
        st.checkbox(item, value=False)

    st.markdown("### 👕 Clothing & Gear")
    for item in clothing:
        st.checkbox(item, value=False)

    if gear:
        st.markdown(f"### 🎒 {trip_type} Gear")
        for item in gear:
            st.checkbox(item, value=False)

    st.markdown("### 📆 Per-Day Clothing")
    for item in per_day:
        st.checkbox(item, value=False)

    st.markdown("---")
    st.info("💡 Tip: Roll your clothes to save space and avoid wrinkles.")
