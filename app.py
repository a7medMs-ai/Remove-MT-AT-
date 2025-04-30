import streamlit as st
import re
from datetime import datetime
from PIL import Image
import io
import zipfile
import os
import tempfile
import rarfile

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
            st.markdown(
                \"\"\"<div style='width:150px; height:150px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center;'>
                <p style='color:#666;'>Company Logo</p>
                </div>\"\"\",
                unsafe_allow_html=True
            )
    with col2:
        st.title("SDLXLIFF File Processor")
        st.caption("Translation Engineering Tool - 2025 • v1.0.0")

# ====== Sidebar ======
with st.sidebar:
    st.header("Developer Information")
    st.subheader("Ahmed Mostafa Saad")
    st.write(
        '''
        - **Position**: Localization Engineering & TMS Support Team Lead
        - **Contact**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)
        - **Company**: Future Group Translation Services
        '''
    )
    st.divider()
    st.header("Tool Instructions")
    st.write(
        '''
        1. Upload .sdlxliff file, or ZIP/RAR containing them
        2. Automatic processing will:
           - Convert all MT segments to: conf="ApprovedTranslation" origin="interactive"
        3. Download processed files as ZIP
        '''
    )

# ====== File Processing ======
st.header("File Processing")
uploaded_file = st.file_uploader(
    "Upload SDLXLIFF / ZIP / RAR file",
    type=["sdlxliff", "zip", "rar"],
    help="Supports single SDLXLIFF, ZIP or RAR with multiple files"
)

def process_content(xml_text):
    xml_text = re.sub(
        r'conf="[^"]*"\\s+origin="mt"\\s+origin-system="[^"]*"',
        'conf="ApprovedTranslation" origin="interactive"',
        xml_text
    )
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
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".sdlxliff"):
                            file_count += 1
                            with open(os.path.join(root, file), "rb") as f:
                                process_single_file(file, f.read())

        elif uploaded_file.name.endswith(".rar"):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_rar:
                tmp_rar.write(uploaded_file.read())
                tmp_rar_path = tmp_rar.name

            rf = rarfile.RarFile(tmp_rar_path)
            rf.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".sdlxliff"):
                        file_count += 1
                        with open(os.path.join(root, file), "rb") as f:
                            process_single_file(file, f.read())

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

        st.components.v1.html(
            '''
            <script>
                var snd = new Audio("https://www.soundjay.com/buttons/sounds/button-09.mp3");
                snd.play();
            </script>
            ''',
            height=0
        )
