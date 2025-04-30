import streamlit as st
import re
from datetime import datetime
from PIL import Image
import io
import base64
import zipfile
import os
import tempfile

# ====== Configuration ======
st.set_page_config(
    page_title="SDLXLIFF Processor",
    page_icon="⚙️",
    layout="wide"
)

# ====== Image Loading Function ======
def load_image():
    try:
        with open("assets/future-group-logo.png", "rb") as f:
            return Image.open(io.BytesIO(f.read()))
    except:
        return None

# ====== Header Section ======
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        logo = load_image()
        if logo:
            st.image(logo, width=150)
        else:
            st.markdown(\"\"\"
            <div style="width:150px; height:150px; 
                       background-color:#f0f0f0; 
                       display:flex; 
                       align-items:center; 
                       justify-content:center;">
                <p style="color:#666;">Company Logo</p>
            </div>
            \"\"\", unsafe_allow_html=True)
    with col2:
        st.title("SDLXLIFF File Processor")
        st.caption("Translation Engineering Tool - 2025 • v1.0.0")

# ====== Sidebar ======
with st.sidebar:
    st.header("Developer Information")
    st.subheader("Ahmed Mostafa Saad")
    st.write(\"\"\"
    - **Position**: Localization Engineering & TMS Support Team Lead
    - **Contact**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)
    - **Company**: Future Group Translation Services
    \"\"\")
    st.divider()
    
    st.header("Tool Instructions")
    st.write(\"\"\"
    1. Upload .sdlxliff file, or ZIP containing them
    2. Automatic processing will:
       - Convert all MT segments to: conf="ApprovedTranslation" origin="interactive"
    3. Download processed files as ZIP
    \"\"\")

# ====== File Processing ======
st.header("File Processing")
uploaded_file = st.file_uploader(
    "Upload SDLXLIFF / ZIP file", 
    type=["sdlxliff", "zip"],
    help="Supports single SDLXLIFF or ZIP with multiple files"
)

def process_content(xml_text):
    # Replace full pattern using function to maintain order
    def replacer(match):
        return 'conf="ApprovedTranslation" origin="interactive"'
    xml_text = re.sub(
        r'conf="[^"]*"\\s+origin="mt"\\s+origin-system="[^"]*"',
        replacer,
        xml_text
    )
    # Fallback cleanup
    xml_text = re.sub(
        r'origin="mt"\\s+origin-system="[^"]*"',
        'origin="interactive"',
        xml_text
    )
    return xml_text

if uploaded_file:
    with st.spinner("Processing your file(s)..."):
        temp_dir = tempfile.mkdtemp()
        processed_dir = os.path.join(temp_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        file_count = 0
        processed_count = 0

        def process_single_file(file_name, raw_data):
            nonlocal processed_count
            try:
                xml = raw_data.decode("utf-8")
                processed = process_content(xml)
                with open(os.path.join(processed_dir, file_name), "w", encoding="utf-8") as f_out:
                    f_out.write(processed)
                processed_count += 1
            except:
                pass

        if uploaded_file.name.endswith(".sdlxliff"):
            process_single_file(uploaded_file.name, uploaded_file.getvalue())
            file_count = 1

        elif uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".sdlxliff"):
                            file_count += 1
                            file_path = os.path.join(root, file)
                            with open(file_path, "rb") as f:
                                process_single_file(file, f.read())

        # Compress processed files
        zip_output_path = os.path.join(temp_dir, "processed_output.zip")
        with zipfile.ZipFile(zip_output_path, "w") as zf:
            for file in os.listdir(processed_dir):
                zf.write(os.path.join(processed_dir, file), arcname=file)

        st.success("Processing completed successfully!")
        with open(zip_output_path, "rb") as f:
            st.download_button(
                label="Download Processed Files",
                data=f,
                file_name="processed_output.zip",
                mime="application/zip"
            )

        st.write(f"✅ {processed_count} of {file_count} file(s) processed.")

        st.markdown(\"\"\"
        <script>
        var snd = new Audio("https://www.soundjay.com/buttons/sounds/button-09.mp3");
        snd.play();
        </script>
        \"\"\", unsafe_allow_html=True)
