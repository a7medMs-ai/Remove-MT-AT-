import streamlit as st

st.title("About SDLXLIFF Fix & Cleaner Tool")

st.write("""
## Overview

This tool is developed to assist localization professionals in handling common issues found in SDLXLIFF files. It aims to reduce manual effort, minimize QA issues, and streamline project workflows.

## Key Features

- **Fix Null Reference Errors**  
  Automatically resolves issues such as `Value cannot be null. Parameter name: rootContainer`.

- **Remove AT/MT Tags**  
  Cleans up segments marked as Machine Translation (MT) or Auto-Translation (AT) to ensure better segment status handling and prevent unwanted propagation.

- **Safe and Structure-Preserving**  
  Keeps the file structure intact while applying all necessary fixes.

## Technical Details

- Built with Python and Streamlit
- Uses regex and XML parsing for accurate manipulation
- Lightweight, portable, and user-friendly

## Developer Information

- **Name:** Ahmed Mostafa Saad  
- **Position:** Localization Engineering & TMS Support Team Lead  
- **Contact:** ahmed.mostafaa@future-group.com  
- **Company:** Future Group Translation Services
""")
