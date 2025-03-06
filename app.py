import streamlit as st
import pandas as pd
import os
import subprocess
from io import BytesIO

# Install openpyxl at runtime if missing (for Streamlit Cloud)
try:
    import openpyxl
except ImportError:
    subprocess.run(["pip", "install", "openpyxl"])
    import openpyxl  # Re-import after installation

# Streamlit Page Config
st.set_page_config(page_title="🗃 Data Sweeper", layout="wide")
st.title("📁 Data Sweeper")
st.write("This app helps clean your data and transform files between CSV and Excel formats.")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your CSV or Excel file",
    type=['csv', 'xlsx'],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file based on extension
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file, encoding="utf-8", errors="replace")
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"Unsupported file format: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error loading file {file.name}: {str(e)}")
            continue

        # Display file details
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        st.write("**Dataframe Preview:**")
        st.write(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for: {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed successfully!")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled successfully!")

        # Column selection for conversion
        st.subheader("🔄 Select Columns for Conversion")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # Conversion Options
        st.subheader("📂 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False, encoding="utf-8")
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                buffer.seek(0)
                st.download_button(
                    label=f"⬇ Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
            except Exception as e:
                st.error(f"Error converting file: {str(e)}")

st.success("✅ Thank you for using Data Sweeper! 😊")
