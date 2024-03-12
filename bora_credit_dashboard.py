import streamlit as st
import pandas as pd
from multipage import MultiPage
from apps import bora_merchant_demographics

st.set_page_config( layout="wide",initial_sidebar_state="expanded")

# Define your contact email address
contact_email = "ck@boracredit.org"
red_markdown = "#F03E35"

# Load allowed emails and passwords from csv file
allowed_emails_df = pd.read_csv("allowed_emails.csv")

red_markdown = "#F03E35"



# Initialize session state
if "login_status_sample" not in st.session_state:
    st.session_state.login_status_sample = False


# Landing page
st.sidebar.title("Select Dashboard")
selected_dashboard = st.sidebar.radio("options", ["Sample Description"],
                                     label_visibility='collapsed')


# Add a contact support link at the bottom of the sidebar (visible even before login)
with st.sidebar:
    st.markdown(
        f'<a class="custom-link" href="mailto:{contact_email}?subject=Dashboard Issue&body=Please describe the issue you\'re facing." target="_blank" style="color: #1a73e8; font-size: 16px; font-style: italic;">Contact Support</a>',
        unsafe_allow_html=True,
    )

# Login form based on the selected dashboard

# Show the selected dashboard
# Show the selected dashboard
if selected_dashboard == "Sample Description":
    with st.sidebar.form("Login_Form"):
        email_input = st.text_input("Email", key="email_input",help=None)
        password_input = st.text_input("Enter Password", type="password", key="password_input")
        login_button = st.form_submit_button("Login")
        if login_button:
            # Check if entered email is in the allowed list
            if email_input in allowed_emails_df['email'].tolist():
                # Check if entered password matches the corresponding password in the allowed list
                if allowed_emails_df.loc[
                        allowed_emails_df['email'] == email_input, 'password'].values[0]:
                    st.session_state.login_status_sample = True
                else:
                    st.markdown(
                        f'<p style="color:{red_markdown}; font-size: 14px; font-style: italic;">The password you entered is incorrect</p>',
                        unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<p style="color:{red_markdown}; font-size: 14px; font-style: italic;">Visit <a href="https://boracredit.org/" target="_blank">bora credit</a> to signup</p>',
                    unsafe_allow_html=True)


# Check login status and show the selected dashboard
if st.session_state.login_status_sample and selected_dashboard == "Sample Description":
    bora_merchant_demographics.app()


    
    
     