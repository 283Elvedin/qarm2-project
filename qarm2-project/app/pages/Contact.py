import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from layout import set_page_config, render_header

set_page_config("Vedoinvest – Contact")
render_header(active_page="Contact")

st.title("Contact Vedoinvest")

st.markdown(
    """
If you have any **questions, comments or suggestions** about the platform
or the investment methodology, you can leave a message below.

This contact form is a **demo** – it does not send real emails, but it shows
how a client-facing page could look.
"""
)

st.subheader("Your details")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
with col2:
    email = st.text_input("Email (optional)")

topic = st.selectbox(
    "Request type",
    [
        "Question about the platform",
        "Question about the methodology",
        "Feedback on the user interface",
        "Other",
    ],
)

message = st.text_area("Message", height=200)

if st.button("Submit message"):
    if len(message.strip()) == 0:
        st.error("Please write a short message before submitting.")
    else:
        st.success(
            "Thank you for your message! "
            "This is a demonstration interface, so no real email is sent, "
            "but your feedback is very much appreciated."
        )

st.caption(
    "Data entered here is not stored permanently – it only lives in your local session for demonstration purposes."
)
