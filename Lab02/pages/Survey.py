# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# Folder that holds data.csv (one level up from this pages folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data.csv")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What's your favorite track event? (100, 200, 400, 800, 1600, 3200)")
    value_input = st.text_input("How many hours of sleep do you get each night?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category = category_input.strip().lower().replace(",", "").replace(" ", "")
        value = value_input.strip()

        if category == "" or value == "":
            st.error("Please fill in both boxes.")
        else:
            try:
                value = float(value)
            except ValueError:
                st.error("The value must be a number, like 7 or 7.5.")
            else:
                # Make sure the file ends with a new line before adding a row
                needs_newline = False
                if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
                    with open(CSV_FILE, "rb") as f:
                        f.seek(-1, os.SEEK_END)
                        needs_newline = f.read(1) != b"\n"

                # Append the new row to data.csv
                with open(CSV_FILE, "a") as f:
                    if needs_newline:
                        f.write("\n")
                    f.write(f"{category},{value}\n")

                st.success("Your data has been submitted!")
                st.write(f"You entered: **Category:** {category}, **Value:** {value}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(CSV_FILE)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
