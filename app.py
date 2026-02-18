import streamlit as st

# -----------------------------
# Function to Generate Packing List
# -----------------------------
def generate_packing_list(days, weather, trip_type):

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
        clothing += ["🧥 Jacket", "🧤 Gloves", "🧦 Woolen Socks"]
    elif weather == "Hot":
        clothing += ["👕 T-Shirts", "🩳 Shorts", "🧢 Cap"]
    elif weather == "Rainy":
        clothing += ["☔ Umbrella", "🧥 Raincoat", "🥾 Waterproof Shoes"]

    gear = []
    if trip_type == "Business":
        gear += ["💼 Laptop", "👔 Formal Wear"]
    elif trip_type == "Vacation":
        gear += ["📷 Camera", "🎧 Headphones"]
    elif trip_type == "Adventure":
        gear += ["🥾 Hiking Boots", "🩹 First Aid Kit"]

    daily_items = [f"👕 Clothes x {days}", f"🧦 Socks x {days}"]

    return essentials + clothing + gear + daily_items


# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Travel Packing List Generator", page_icon="🧳")
st.title("🧳 Travel Packing List Generator")
st.markdown("Generate and customize your travel packing checklist.")

# -----------------------------
# Input Form
# -----------------------------
with st.form("trip_form"):
    destination = st.text_input("Destination")
    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=60, value=3)
    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])
    trip_type = st.selectbox("Trip Type", ["Vacation", "Business", "Adventure"])
    submitted = st.form_submit_button("Generate Packing List")

# -----------------------------
# Generate List
# -----------------------------
if submitted:

    if destination.strip() == "":
        st.error("Please enter a destination.")
    else:
        st.success(f"Packing list for {destination}")

        items = generate_packing_list(days, weather, trip_type)

        # Select All Option (default True)
        select_all = st.checkbox("✅ Select All Items", value=True)

        selected_items = []

        st.markdown("### 📦 Your Packing Items")

        for i, item in enumerate(items):
            checked = st.checkbox(item, value=select_all, key=f"item_{i}")
            if checked:
                selected_items.append(item)

        # -----------------------------
        # Download Button
        # -----------------------------
        if selected_items:
            download_text = "\n".join(selected_items)

            st.download_button(
                label="📥 Download Selected Items",
                data=download_text,
                file_name="packing_list.txt",
                mime="text/plain"
            )
        else:
            st.warning("No items selected to download.")

        st.markdown("---")
        st.info("Tip: Select only items you actually own or want to carry.")
