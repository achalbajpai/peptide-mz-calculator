"""
Documentation page for the application.

This module provides comprehensive documentation and guides for users.
"""

import streamlit as st
from src.common.common import page_setup
from pathlib import Path

page_setup(page="docs")

st.title("📚 Documentation")

cols = st.columns(2)

pages = [
    "User Guide",
    "What's New",
    "Feature Overview",
]

page = cols[0].selectbox(
    "**Content**",
    pages,
)

#############################################################################################
# User Guide
#############################################################################################

if page == pages[0]:
    with open(Path("docs", "user_guide.md"), "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(content) 

#############################################################################################
# What's New
#############################################################################################

if page == pages[1]:
    with open(Path("docs", "new.md"), "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(content) 

#############################################################################################
# Feature Overview
#############################################################################################

if page == pages[2]:
    with open(Path("docs", "feature_overview.md"), "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(content)