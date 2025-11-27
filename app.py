import streamlit as st
import json
import os
from datetime import date, datetime
import os
import openai
from dotenv import load_dotenv
import pdb
import logging
from utils import categorize_and_make_timeline, save_milestone, show_milestones, add_timeline_styles, render_timeline, save_timeline, show_timeline_from_db

st.set_page_config(page_title="Savir Stories", layout="wide")
#testing GIt 
#styling section, needs to be moved once we go into production
st.markdown("""
<style>
    body {
    background-color: #FFFFFF;
    }
    /* Reduce excessive padding at top */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 900px;  /* makes your app look more like a sleek web app */
    }

    /* Modern card look */
    .app-card {
        background-color: #FFFFFF;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 1.2rem;
    }

    /* Better buttons */
    .stButton>button {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        border: none;
    }

    /* Cleaner upload widget spacing */
    .uploadedFile {
        border-radius: 10px !important;
    }

</style>
""", unsafe_allow_html=True)

# Streamlit page setup
st.title("Savir Stories")
st.caption("Capture and visualize Savir's milestones with photos and AI-generated timelines.")
st.divider()
st.subheader("Add a new milestone")

# Form inputs
milestone_date = datetime.now().strftime("%Y%m%d_%H%M%S")
photo = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])
# Save button
if st.button("Save Photo(s)"):
    if photo is None:
        st.error("Please upload a photo before saving the milestone.")
    else:
        save_milestone(milestone_date, photo)
        st.success("🎉 Milestone saved successfully!")

st.divider()
st.subheader("Timeline actions")
# Save timeline and milestones
if st.button("Save timeline"):
    save_timeline()
    st.success("🎉 Timeline saved successfully!")

# Display existing milestones
if st.button("Show Milestones"):
    st.title("🍼 Savir Stories: Milestone Timeline")
    milestones = []
    milestones = show_milestones()
    if milestones: 
        add_timeline_styles()
        milestones.sort(key=lambda x: x["date"])
        render_timeline(milestones)
    else:
        st.write("No milestones logged yet. Start by adding one above!")
    # Footer

if st.button("Generate Categorized Timeline"):
    st.title("🍼 Savir Stories: Categorized Milestone Timeline")
    milestones = []
    milestones = show_timeline_from_db()
    if milestones:
        categorized_timeline = show_timeline_from_db()
        print(f"Categorized Timeline: {categorized_timeline}")
        st.markdown(categorized_timeline, unsafe_allow_html=True)
    else:
        st.write("No milestones logged yet. Start by adding one above!")
    # Footer