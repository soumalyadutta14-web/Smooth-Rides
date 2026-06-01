import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import random
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Smart Cab Booking", layout="wide")

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🚖 Smart Cab Booking System")
st.markdown("Book your cab quickly and easily")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio(
    "Go To",
    [
        "Book Cab",
        "Driver Database",
        "City Database",
        "Fare Details"
    ]
)

# -------------------------------------------------
# CITY DATABASE
# -------------------------------------------------
city_data = {
    "Kolkata": (22.5726, 88.3639),
    "Durgapur": (23.5204, 87.3119),
    "Asansol": (23.6739, 86.9524),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Patna": (25.5941, 85.1376)
}

# -------------------------------------------------
# DRIVER DATABASE
# -------------------------------------------------
driver_data = pd.DataFrame([
    {
        "Driver Name": "Rahul Sharma",
        "Car": "Swift Dzire",
        "Cab Number": "WB 40 A 1122",
        "Rating": 4.7
    },
    {
        "Driver Name": "Amit Das",
        "Car": "Hyundai Aura",
        "Cab Number": "WB 38 C 7721",
        "Rating": 4.5
    },
    {
        "Driver Name": "Rohan Singh",
        "Car": "Honda Amaze",
        "Cab Number": "DL 01 X 2211",
        "Rating": 4.8
    },
    {
        "Driver Name": "Arjun Roy",
        "Car": "Maruti Ertiga",
        "Cab Number": "WB 44 D 9981",
        "Rating": 4.6
    }
])

# -------------------------------------------------
# FARE SETTINGS
# -------------------------------------------------
BASE_FARE = 50
PER_KM_RATE = 14
GST_PERCENT = 5

# -------------------------------------------------
# CITY DATABASE PAGE
# -------------------------------------------------
if menu == "City Database":

    st.header("🌍 City Database")

    city_df = pd.DataFrame([
        {
            "City": city,
            "Latitude": coords[0],
            "Longitude": coords[1]
        }
        for city, coords in city_data.items()
    ])

    st.dataframe(city_df, use_container_width=True)

# -------------------------------------------------
# DRIVER DATABASE PAGE
# -------------------------------------------------
elif menu == "Driver Database":

    st.header("👨‍✈️ Driver Database")

    st.dataframe(driver_data, use_container_width=True)

# -------------------------------------------------
# FARE DETAILS PAGE
# -------------------------------------------------
elif menu == "Fare Details":

    st.header("💰 Fare Details")

    st.write(f"Base Fare: ₹{BASE_FARE}")
    st.write(f"Per KM Rate: ₹{PER_KM_RATE}")
    st.write(f"GST: {GST_PERCENT}%")

# -------------------------------------------------
# BOOK CAB PAGE
# -------------------------------------------------
elif menu == "Book Cab":

    st.header("🚕 Book Your Cab")

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Enter Customer Name")
        mobile = st.text_input("Enter Mobile Number")
        pickup_city = st.selectbox(
            "Select Pickup City",
            list(city_data.keys())
        )

    with col2:
        booking_date = st.date_input("Booking Date")
        pickup_time = st.time_input("Pickup Time")
        drop_city = st.selectbox(
            "Select Drop City",
            list(city_data.keys())
        )

    cab_type = st.selectbox(
        "Select Cab Type",
        ["Mini", "Sedan", "SUV"]
    )

    # -------------------------------------------------
    # CAB MULTIPLIER
    # -------------------------------------------------
    multiplier = 1

    if cab_type == "Mini":
        multiplier = 1
    elif cab_type == "Sedan":
        multiplier = 1.3
    elif cab_type == "SUV":
        multiplier = 1.7

    # -------------------------------------------------
    # BOOK BUTTON
    # -------------------------------------------------
    if st.button("Book Cab"):

        if customer_name == "" or mobile == "":
            st.error("Please fill all details")

        elif pickup_city == drop_city:
            st.warning("Pickup and Drop city cannot be same")

        else:

            # ---------------------------------------------
            # DISTANCE CALCULATION
            # ---------------------------------------------
            pickup_coords = city_data[pickup_city]
            drop_coords = city_data[drop_city]

            distance = geodesic(
                pickup_coords,
                drop_coords
            ).km

            distance = round(distance, 2)

            # ---------------------------------------------
            # FARE CALCULATION
            # ---------------------------------------------
            basic_fare = BASE_FARE + (distance * PER_KM_RATE)
            cab_fare = basic_fare * multiplier
            gst_amount = (cab_fare * GST_PERCENT) / 100
            total_fare = cab_fare + gst_amount

            total_fare = round(total_fare, 2)
            gst_amount = round(gst_amount, 2)

            # ---------------------------------------------
            # DRIVER ASSIGNMENT
            # ---------------------------------------------
            assigned_driver = driver_data.sample(1).iloc[0]

            booking_id = random.randint(10000, 99999)

            # ---------------------------------------------
            # SUCCESS MESSAGE
            # ---------------------------------------------
            st.success("Cab Booked Successfully ✅")

            # ---------------------------------------------
            # BOOKING DETAILS
            # ---------------------------------------------
            st.subheader("📋 Booking Details")

            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:
                st.info(f"Booking ID: {booking_id}")
                st.info(f"Customer: {customer_name}")
                st.info(f"Mobile: {mobile}")
                st.info(f"Cab Type: {cab_type}")

            with detail_col2:
                st.info(f"Pickup: {pickup_city}")
                st.info(f"Drop: {drop_city}")
                st.info(f"Distance: {distance} KM")
                st.info(f"Date: {booking_date}")

            # ---------------------------------------------
            # DRIVER DETAILS
            # ---------------------------------------------
            st.subheader("👨‍✈️ Driver Assigned")

            driver_col1, driver_col2 = st.columns(2)

            with driver_col1:
                st.success(
                    f"Driver Name: {assigned_driver['Driver Name']}"
                )
                st.success(
                    f"Car: {assigned_driver['Car']}"
                )

            with driver_col2:
                st.success(
                    f"Cab Number: {assigned_driver['Cab Number']}"
                )
                st.success(
                    f"Rating: ⭐ {assigned_driver['Rating']}"
                )

            # ---------------------------------------------
            # INVOICE
            # ---------------------------------------------
            st.subheader("🧾 Fare Invoice")

            invoice_df = pd.DataFrame([
                ["Base Fare", f"₹ {BASE_FARE}"],
                ["Distance Charge", f"₹ {round(distance * PER_KM_RATE, 2)}"],
                ["Cab Type Multiplier", f"x {multiplier}"],
                ["GST", f"₹ {gst_amount}"],
                ["Total Fare", f"₹ {total_fare}"]
            ], columns=["Description", "Amount"])

            st.table(invoice_df)

            # ---------------------------------------------
            # FINAL MESSAGE
            # ---------------------------------------------
            st.balloons()

            st.markdown("---")
            st.write(
                f"Booking generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            )

