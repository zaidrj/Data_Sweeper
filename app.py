import streamlit as st 
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🗃Data Sweeper", layout="wide")
st.title("📁Data sweeper")
st.write("This app is designed to help you clean your data and transform your data files b/w CSV and Excel formats.")

uploade_files = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'],
                                 accept_multiple_files=True)

if uploade_files:
    for file in uploade_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Please upload a valid CSV or Excel file, unsupported file format: {file_ext}")
            continue
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        st.write("Dataframe Head Preview")
        st.write(df.head())

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for: {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully")
            with col2:
                if st.button(f"Fill missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled successfully")

        st.subheader("Select columns to convert")
        columns = st.multiselect(f"Choose Column for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        st.subheader("Data Visualization")
        if st.checkbox(f"Show Data Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
               df.to_csv(buffer, index=False)
               file_name = file.name.replace(file_ext, ".csv")
               mime_type = "text/csv"
            
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


            st.download_button(
                label=f"⬇ Click here to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )



st.success("Thank you for using this app 😊")
                