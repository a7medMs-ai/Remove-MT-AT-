import streamlit as st
import re
from datetime import datetime
from PIL import Image
import io
import base64

# ====== Configuration ======
st.set_page_config(
    page_title="SDLXLIFF Processor",
    page_icon="⚙️",
    layout="wide"
)

# ====== Image Loading Function ======
def load_image():
    """Load company logo with error handling"""
    try:
        # Try loading from local assets first
        with open("assets/future-group-logo.png", "rb") as f:
            return Image.open(io.BytesIO(f.read()))
    except FileNotFoundError:
        st.warning("Company logo not found in assets folder")
        return None
    except Exception as e:
        st.warning(f"Error loading logo: {str(e)}")
        return None

# ====== Header Section ======
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        logo = load_image()
        if logo:
            st.image(logo, width=150)
        else:
            # Fallback text if logo can't be loaded
            st.markdown("""
            <div style="width:150px; height:150px; 
                       background-color:#f0f0f0; 
                       display:flex; 
                       align-items:center; 
                       justify-content:center;">
                <p style="color:#666;">Company Logo</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.title("SDLXLIFF File Processor")
        st.caption("Translation Engineering Tool - 2025 • v1.0.0")

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
    
    st.header("Tool Instructions")
    st.write("""
    1. Upload SDLXLIFF file
    2. Automatic processing will:
       - Change MT segments to interactive status
    3. Download modified file
    """)

# ====== Main Processing ======
st.header("File Processing")
uploaded_file = st.file_uploader(
    "Upload SDLXLIFF File", 
    type=["sdlxliff"],
    help="Select your SDLXLIFF file for processing"
)

if uploaded_file:
    with st.spinner("Processing your file..."):
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            
            # Process the content
            processed_content = re.sub(
                r'origin="mt"\s+origin-system=".*?"',
                'origin="interactive"',
                content
            )
            
            # Download button
            st.success("Processing completed successfully!")
            st.download_button(
                label="Download Processed File",
                data=processed_content,
                file_name=f"processed_{datetime.now().strftime('%Y%m%d_%H%M')}_{uploaded_file.name}",
                mime="application/xml",
                type="primary"
            )
            
            # File info
            st.divider()
            st.json({
                "file_info": {
                    "original_name": uploaded_file.name,
                    "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "modifications": {
                        "mt_conversion": True,
                        "origin_system_removed": True
                    }
                }
            })
            
        except Exception as e:
            st.error(f"Processing failed: {str(e)}")

# ====== Footer ======
st.divider()
st.markdown("""
<div style="text-align: center; color: #555; padding: 10px;">
    Future Group - Localization Engineering • © 2025 • v1.0.0
</div>
""", unsafe_allow_html=True)
