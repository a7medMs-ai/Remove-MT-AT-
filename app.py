import streamlit as st
import re
import zipfile
import os
import io
import tempfile
import rarfile
from PIL import Image

# ====== Configuration ======
st.set_page_config(page_title="SDLXLIFF Processor", page_icon="⚙️", layout="wide")

# ====== Load logo (optional) ======
def load_logo():
    try:
        return Image.open("assets/future-group-logo.png")
    except:
        return None

# ====== Process Function ======
def process_content(xml_text):
    xml_text = re.sub(
        r'conf="[^"]*"\s+origin="mt"\s+origin-system="[^"]*"',
        'conf="ApprovedTranslation" origin="interactive"',
        xml_text
    )
    xml_text = re.sub(
        r'origin="mt"\s+origin-system="[^"]*"',
        'origin="interactive"',
        xml_text
    )
    return xml_text

# ====== Process Single File ======
def process_single_file(file_name, file_bytes, output_dir, processed_files):
    try:
        xml = file_bytes.decode("utf-8")
        modified = process_content(xml)
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f_out:
            f_out.write(modified)
        processed_files.append(file_name)
        return True
    except:
        return False

# ====== Header ======
col1, col2 = st.columns([1, 4])
with col1:
    logo = load_logo()
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown(
            """
            <div style="width:100px;height:100px;background:#eee;display:flex;align-items:center;justify-content:center;">
            <span style="color:#888;">Logo</span>
            </div>
            """, unsafe_allow_html=True
        )
with col2:
    st.title("SDLXLIFF File Processor")
    st.caption("Future Group • Localization Engineering Tool • v1.0")

# ====== Sidebar ======
with st.sidebar:
    st.header("About the Developer")
    st.markdown("""
    **Ahmed Mostafa Saad**  
    Team Lead - Localization Engineering  
    [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)
    """)
    st.divider()
    st.markdown("### Instructions")
    st.markdown("""
    - Upload a `.sdlxliff`, `.zip`, or `.rar` file  
    - Tool replaces MT segments with `ApprovedTranslation`  
    - Download processed output as ZIP  
    """)

# ====== Upload ======
st.header("Upload File")
uploaded_file = st.file_uploader(
    "Choose a .sdlxliff, .zip or .rar file",
    type=["sdlxliff", "zip", "rar"]
)

if uploaded_file:
    with st.spinner("Processing..."):
        temp_dir = tempfile.mkdtemp()
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        processed_files = []
        file_count = 0

        # ----- Handle different file types -----
        if uploaded_file.name.endswith(".sdlxliff"):
            file_count = 1
            process_single_file(uploaded_file.name, uploaded_file.getvalue(), output_dir, processed_files)

        elif uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(uploaded_file, "r") as zf:
                zf.extractall(temp_dir)
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".sdlxliff"):
                            file_count += 1
                            with open(os.path.join(root, file), "rb") as f:
                                process_single_file(file, f.read(), output_dir, processed_files)

        elif uploaded_file.name.endswith(".rar"):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_rar:
                tmp_rar.write(uploaded_file.read())
                rar_path = tmp_rar.name
            rf = rarfile.RarFile(rar_path)
            rf.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".sdlxliff"):
                        file_count += 1
                        with open(os.path.join(root, file), "rb") as f:
                            process_single_file(file, f.read(), output_dir, processed_files)

        # ----- ZIP output -----
        result_zip = os.path.join(temp_dir, "processed_files.zip")
        with zipfile.ZipFile(result_zip, "w") as zipf:
            for file in os.listdir(output_dir):
                zipf.write(os.path.join(output_dir, file), arcname=file)

        st.success("✅ Processing Completed!")
        st.write(f"Processed {len(processed_files)} of {file_count} file(s).")

        if processed_files:
            st.markdown("### Files Processed:")
            for f in processed_files:
                st.markdown(f"- {f}")

        with open(result_zip, "rb") as f:
            st.download_button(
                label="⬇️ Download ZIP",
                data=f,
                file_name="processed_files.zip",
                mime="application/zip"
            )

        # Play sound on finish
        st.components.v1.html(
            """
            <script>
            new Audio("https://www.soundjay.com/buttons/sounds/button-09.mp3").play();
            </script>
            """, height=0
        )
