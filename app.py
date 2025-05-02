import streamlit as st
import re
import zipfile
import os
import io
import tempfile
from PIL import Image

try:
    import rarfile
    RAR_AVAILABLE = True
except ImportError:
    RAR_AVAILABLE = False

# ====== Page Config ======
st.set_page_config(page_title="SDLXLIFF Processor", page_icon="⚙️", layout="wide")

# ====== Logo ======
def load_logo():
    try:
        return Image.open("assets/future-group-logo.png")
    except:
        return None

# ====== Transformation Logic ======
def process_content(xml_text):
    xml_text = re.sub(r'conf="[^"]*"\s+origin="mt"\s+origin-system="[^"]*"', 'conf="ApprovedTranslation" origin="interactive"', xml_text)
    xml_text = re.sub(r'origin="mt"\s+origin-system="[^"]*"', 'origin="interactive"', xml_text)
    return xml_text

# ====== Process File ======
def process_file(file_name, data, output_dir, log_list):
    try:
        content = data.decode("utf-8")
        processed = process_content(content)
        out_path = os.path.join(output_dir, file_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(processed)
        log_list.append(file_name)
        return True
    except Exception as e:
        return False

# ====== Layout ======
col1, col2 = st.columns([1, 4])
with col1:
    logo = load_logo()
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown("<div style='width:100px;height:100px;background:#eee;display:flex;align-items:center;justify-content:center;'><span style='color:#888;'>Logo</span></div>", unsafe_allow_html=True)
with col2:
    st.title("SDLXLIFF File Processor")
    st.caption("Future Group • Localization Engineering Tool • v1.0")

# ====== Sidebar ======
with st.sidebar:
    st.header("Developer Information")
    st.subheader("Ahmed Mostafa Saad")
    st.write("""
    - **Position**: Localization Engineering & TMS Support Team Lead  
    - **Contact**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)  
    - **Company**: Future Group Translation Services
    """)
    st.divider()
    st.markdown("### Instructions")
    st.markdown("- Upload a `.sdlxliff`, `.zip`, or `.rar` file\n- Tool replaces MT segments with `ApprovedTranslation`\n- Download processed ZIP")

# ====== File Upload ======
st.header("Upload File")
uploaded_file = st.file_uploader("Choose a .sdlxliff, .zip or .rar", type=["sdlxliff", "zip", "rar"] if RAR_AVAILABLE else ["sdlxliff", "zip"])

if uploaded_file:
    with st.spinner("Processing your file(s)..."):
        temp_dir = tempfile.mkdtemp()
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        processed_files = []
        total_files = 0

        # Single file
        if uploaded_file.name.endswith(".sdlxliff"):
            total_files = 1
            process_file(uploaded_file.name, uploaded_file.getvalue(), output_dir, processed_files)

        # ZIP archive
        elif uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".sdlxliff"):
                        total_files += 1
                        with open(os.path.join(root, file), "rb") as f:
                            process_file(file, f.read(), output_dir, processed_files)

        # RAR archive
        elif uploaded_file.name.endswith(".rar") and RAR_AVAILABLE:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_rar:
                tmp_rar.write(uploaded_file.read())
            rf = rarfile.RarFile(tmp_rar.name)
            rf.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".sdlxliff"):
                        total_files += 1
                        with open(os.path.join(root, file), "rb") as f:
                            process_file(file, f.read(), output_dir, processed_files)

        # Create ZIP for output
        zip_path = os.path.join(temp_dir, "processed.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for file in os.listdir(output_dir):
                zf.write(os.path.join(output_dir, file), arcname=file)

        # ====== Output Results ======
        st.success("✅ Processing Completed")
        st.write(f"Processed `{len(processed_files)}` of `{total_files}` file(s).")

        if processed_files:
            st.markdown("### Files Processed:")
            for fname in processed_files:
                st.write(f"- {fname}")

        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download Processed ZIP", data=f, file_name="processed_files.zip", mime="application/zip")

        # Play success sound
        st.components.v1.html("""
        <script>
            new Audio("https://www.soundjay.com/buttons/sounds/button-09.mp3").play();
        </script>
        """, height=0)
