"""
Main page for the Peptide M/Z Calculator App.
"""

from pathlib import Path
import streamlit as st

from src.common.common import page_setup, v_space

page_setup(page="main")

# Hero section
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">👋 Welcome to the Peptide M/Z Calculator</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
        Accurate mass-to-charge ratio calculations for proteomics research
    </p>
</div>
""", unsafe_allow_html=True)

# Logo Section  
col1, col2, col3 = st.columns([1, 1.5, 0.5])
with col2:
    st.image("assets/openms_transparent_bg_logo.svg", width=400)

# About section 
st.markdown("""
<div style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
            color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
    <h2 style="margin-top: 0; text-align: center;">📖 About This Calculator</h2>
    <p style="font-size: 1.1rem; text-align: center; margin-bottom: 0;">
        This peptide m/z calculator is designed for researchers and scientists working in 
        <strong>proteomics</strong> and <strong>mass spectrometry</strong>. 
        It provides accurate mass-to-charge ratio calculations for peptides using the powerful 
        <strong>pyOpenMS</strong> library, ensuring reliable results for your research workflows.
    </p>
</div>
""", unsafe_allow_html=True)

# Quickstart links  
st.page_link(
    "content/calculator.py",
    label="🧮 Start calculating Peptide m/z ratios",
    use_container_width=True
)

st.page_link(
    "content/docs.py",
    label="📚 Read the documentation", 
    use_container_width=True
)

st.page_link(
    "content/visualization.py",
    label="📊 Visualize your data",
    use_container_width=True
)
