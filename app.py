import streamlit as st
import os
from src.parser import extract_text_from_pdf
from src.engine import SkillEngine

# --- Configuration ---
SKILL_HIERARCHY_PATH = "data/skill_hierarchy.json"

# --- Initialize SkillEngine (cached for performance) ---
@st.cache_resource
def get_skill_engine():
    return SkillEngine(SKILL_HIERARCHY_PATH)

engine = get_skill_engine()

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="GoldenHR: Semantic Skill Inference")

st.title("🚀 GoldenHR: Semantic Skill Inference System")
st.markdown("""
Welcome to GoldenHR, where we move beyond simple keyword matching to understand the true depth of a candidate's skill set.
Upload a resume (PDF) and let's uncover the explicit and implicit skills!
""")

st.header("1. Upload Resume (PDF Only)")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

extracted_text = ""
if uploaded_file is not None:
    # Save uploaded file temporarily to process
    temp_file_path = os.path.join("data", uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    
    extracted_text = extract_text_from_pdf(temp_file_path)
    
    if extracted_text:
        st.subheader("Extracted Text Preview")
        st.expander("Click to view full extracted text").write(extracted_text)
    else:
        st.warning("Could not extract text from the PDF. It might be an image-based PDF.")

    # Clean up temporary file
    os.remove(temp_file_path)

if extracted_text:
    st.header("2. Skill Analysis")
    inferred_skills = engine.infer_skills(extracted_text)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Explicit Skills Detected")
        if inferred_skills["explicit"]:
            st.markdown(f"**Total: {len(inferred_skills['explicit'])}**")
            for skill in sorted(list(inferred_skills["explicit"])):
                st.markdown(f"- `{skill}`")
        else:
            st.info("No explicit skills found matching our hierarchy.")

    with col2:
        st.subheader("Implicit Skills Inferred")
        if inferred_skills["implicit"]:
            st.markdown(f"**Total: {len(inferred_skills['implicit'])}**")
            for skill in sorted(list(inferred_skills["implicit"])):
                st.markdown(f"- `{skill}`")
        else:
            st.info("No new implicit skills inferred from the explicit ones.")
            
    st.subheader("All Skills (Explicit + Implicit)")
    if inferred_skills["all"]:
        st.markdown(f"**Total: {len(inferred_skills['all'])}**")
        st.write(", ".join(sorted(list(inferred_skills["all"]))))
    else:
        st.info("No skills detected or inferred.")

    st.header("3. Job Requirements Matching (Future Enhancement)")
    st.info("This section will allow you to input job requirements and see how well the candidate matches based on their inferred skills.")

st.markdown("---")
st.markdown("Powered by J.A.R.V.I.S. for GoldenHR")
