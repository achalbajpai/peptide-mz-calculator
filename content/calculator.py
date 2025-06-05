"""
Peptide m/z Calculator functionality.

This module provides a peptide m/z calculator using pyOpenMS for accurate mass spectrometry calculations.
"""

import streamlit as st
import pyopenms as poms


from src.common.common import page_setup

# functions for peptide sequence validation and modification application
def validate_sequence(sequence):
    """Validate peptide sequence contains only valid amino acids."""
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    sequence_clean = ''.join(c for c in sequence.upper() if c.isalpha())
    return all(aa in valid_aa for aa in sequence_clean), sequence_clean

def apply_modification(sequence, modification):
    """Apply the selected modification to the peptide sequence."""
    if modification == "None":
        return sequence
    elif modification == "Oxidation (M)":
        return sequence.replace("M", "M(Oxidation)")
    elif modification == "Carbamidomethyl (C)":
        return sequence.replace("C", "C(Carbamidomethyl)")
    elif modification == "Phosphorylation (S/T/Y)":
        for aa in ['S', 'T', 'Y']:
            if aa in sequence:
                return sequence.replace(aa, f"{aa}(Phospho)", 1)
        return sequence
    elif modification == "Acetylation (N-term)":
        return f".(Acetyl){sequence}"
    elif modification == "Methylation (K/R)":
        for aa in ['K', 'R']:
            if aa in sequence:
                return sequence.replace(aa, f"{aa}(Methyl)", 1)
        return sequence
    elif modification == "Deamidation (N/Q)":
        for aa in ['N', 'Q']:
            if aa in sequence:
                return sequence.replace(aa, f"{aa}(Deamidated)", 1)
        return sequence
    else:
        return sequence

page_setup(page="calculator")

st.markdown("# 🧮 Peptide m/z Calculator")
st.markdown("## Calculate mass-to-charge ratio for peptides")

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

col1, col2 = st.columns([2, 1])

with col1:
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
        options=[
            "None",
            "Oxidation (M)",
            "Carbamidomethyl (C)",
            "Phosphorylation (S/T/Y)",
            "Acetylation (N-term)",
            "Methylation (K/R)",
            "Deamidation (N/Q)"
        ],
        help="Select a common modification to apply to the peptide"
    )

with col2:
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
        # Validate sequence
        is_valid, clean_sequence = validate_sequence(peptide_sequence)
        
        if not is_valid:
            st.error("Invalid amino acid sequence. Please use only standard amino acid codes (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y).")
        elif len(clean_sequence) == 0:
            st.error("Please enter a valid peptide sequence.")
        else:
            try:
                modified_sequence = apply_modification(clean_sequence, modifications)
                
                aa_sequence = poms.AASequence.fromString(modified_sequence)
                
                # calculate m/z ratio
                mz_ratio = aa_sequence.getMZ(charge_state)
                
                # additional information
                mono_weight = aa_sequence.getMonoWeight()
                formula = aa_sequence.getFormula()
                st.success("✅ Calculation Successful!")
                
                # result columns 
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.markdown("### 📊 Results")
                    st.markdown(f"**m/z Ratio:** `{mz_ratio:.6f}`")
                    st.markdown(f"**Monoisotopic Mass:** `{mono_weight:.6f}` Da")
                    st.markdown(f"**Charge State:** `{charge_state}+`")
                
                with result_col2:
                    st.markdown("### 🧪 Sequence Information")
                    st.markdown(f"**Original Sequence:** `{peptide_sequence.upper()}`")
                    if modifications != "None":
                        st.markdown(f"**Modified Sequence:** `{modified_sequence}`")
                    st.markdown(f"**Molecular Formula:** `{formula.toString()}`")
                
                # additional info 
                with st.expander("📋 Additional Information"):
                    st.markdown(f"**Sequence Length:** {len(clean_sequence)} amino acids")
                    st.markdown(f"**Applied Modification:** {modifications}")
                    
                    aa_composition = {}
                    for aa in clean_sequence:
                        aa_composition[aa] = aa_composition.get(aa, 0) + 1
                    
                    if aa_composition:
                        st.markdown("**Amino Acid Composition:**")
                        composition_text = ", ".join([f"{aa}: {count}" for aa, count in sorted(aa_composition.items())])
                        st.markdown(f"`{composition_text}`")
                
            except Exception as e:
                error_msg = str(e).lower()
                if "unknown" in error_msg or "modification" in error_msg:
                    st.error("❌ Error: Unknown modification or invalid modification syntax.")
                    st.info("Try using 'None' for modifications or check if the modification name is correct.")
                elif "sequence" in error_msg:
                    st.error("❌ Error: Invalid peptide sequence format.")
                    st.info("Please check your peptide sequence for invalid characters or formatting.")
                else:
                    st.error(f"❌ Error in calculation: {str(e)}")
                
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