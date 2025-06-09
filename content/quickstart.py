"""
Main page for the Peptide M/Z Calculator App.
"""

from pathlib import Path
import streamlit as st
# import pyopenms as poms # No longer needed here, handled by backend

from src.common.common import page_setup, v_space
# Import backend functions
from src.peptide_calculator import (
    validate_peptide_sequence, 
    apply_modification, 
    calculate_peptide_mz, 
    get_supported_modifications
)

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

st.markdown("""
<hr style="height:2px;border-width:0;color:gray;background-color:gray">
""", unsafe_allow_html=True)

# working explaination 
st.markdown("""
This calculator determines the mass-to-charge (m/z) ratio of peptides based on their amino acid sequence, 
charge state, and modifications. It uses the pyOpenMS library for accurate mass spectrometry calculations.

**How to use:**
1. Enter your peptide sequence using single-letter amino acid codes
2. Specify the charge state (positive integer)
3. Select modifications (optional)
4. Click "Calculate m/z" to get the result
""")

st.markdown("---")

col1_calc, col2_calc = st.columns([2, 1])

with col1_calc:
    # Input with sample data I have provided as an example 
    peptide_sequence = st.text_input(
        "Peptide Sequence",
        value="PEPTIDE",
        help="Enter the peptide sequence using single-letter amino acid codes (e.g., PEPTIDE, MKWVTFISLLFLFSSAYS)",
        placeholder="Enter peptide sequence..."
    )
    
    # Modification selection
    modifications = st.selectbox(
        "Modifications",
        options=get_supported_modifications(), # Use backend function
        help="Select a common modification to apply to the peptide"
    )

with col2_calc:
    # Charge State
    charge_state = st.number_input(
        "Charge State",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="Enter the charge state (number of protons added)"
    )
    
    # Calculate button for result 
    calculate_button = st.button(
        "Calculate M/Z",
        type="primary",
        use_container_width=True
    )

st.markdown("---")

if calculate_button:
    if not peptide_sequence.strip():
        st.error("Please enter a peptide sequence.")
    else:
        # Validate sequence using backend function
        is_valid, clean_sequence = validate_peptide_sequence(peptide_sequence)
        
        if not is_valid:
            st.error("Invalid amino acid sequence. Please use only standard amino acid codes (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y).")
        elif len(clean_sequence) == 0:
            st.error("Please enter a valid peptide sequence.")
        else:
            try:
                # Calculate m/z using backend function
                results = calculate_peptide_mz(clean_sequence, charge_state, modifications)
                
                st.success("✅ Calculation Successful!")
                
                # result columns 
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.markdown("### 📊 Results")
                    st.markdown(f"**m/z Ratio:** `{results['mz_ratio']:.6f}`")
                    st.markdown(f"**Monoisotopic Mass:** `{results['monoisotopic_mass']:.6f}` Da")
                    st.markdown(f"**Charge State:** `{results['charge_state']}+`")
                
                with result_col2:
                    st.markdown("### 🧪 Sequence Information")
                    st.markdown(f"**Original Sequence:** `{results['original_sequence']}`")
                    if results['modification'] != "None":
                        st.markdown(f"**Modified Sequence:** `{results['modified_sequence']}`")
                    st.markdown(f"**Molecular Formula:** `{results['molecular_formula']}`")
                
                # additional info 
                with st.expander("📋 Additional Information"):
                    st.markdown(f"**Sequence Length:** {results['sequence_length']} amino acids")
                    st.markdown(f"**Applied Modification:** {results['modification']}")
                    
                    aa_composition = results['aa_composition']
                    if aa_composition:
                        st.markdown("**Amino Acid Composition:**")
                        composition_text = ", ".join([f"{aa}: {count}" for aa, count in sorted(aa_composition.items())])
                        st.markdown(f"`{composition_text}`")
                
            except ValueError as e: # Catch specific ValueError from backend
                st.error(f"❌ Error: {str(e)}")
            except Exception as e: # Catch any other unexpected errors
                st.error(f"❌ An unexpected error occurred: {str(e)}")
                
                st.markdown("""
                **Common issues:**
                - Invalid amino acid codes in sequence
                - Unsupported modification syntax
                - Invalid charge state
                - Modification not recognized by OpenMS
                
                **Troubleshooting:**
                - Try without modifications first
                - Use only standard amino acid codes
                - Check sequence for special characters
                """)

# info 
st.markdown("---")
with st.expander("ℹ️ About this Calculator"):
    st.markdown("""
    **Supported Amino Acids:**
    A, R, N, D, C, E, Q, G, H, I, L, K, M, F, P, S, T, W, Y, V
    
    **Modification Formats:**
    - Modifications are applied using OpenMS notation
    - Common modifications are pre-defined in the dropdown
    - For custom modifications, use the format: `AA(ModificationName)`
    - N-terminal modifications: `.(ModificationName)SEQUENCE`
    - C-terminal modifications: `SEQUENCE.(ModificationName)`
    
    **Calculation Method:**
    - Uses pyOpenMS AASequence class for accurate mass calculations
    - Monoisotopic masses are used for all calculations
    - m/z ratio is calculated as: (Monoisotopic Mass + Charge × Proton Mass) / Charge
    
    **Note:** Some modifications may not be recognized by OpenMS. If you encounter errors,
    try calculating without modifications first, or use standard UniMod modification names.
    
    **References:**
    - pyOpenMS Documentation: https://pyopenms.readthedocs.io/
    - OpenMS : https://www.openms.de/
    """)
