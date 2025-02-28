import time
import numpy as np
import streamlit as st
import pandas as pd
import os
from io import BytesIO
st.set_page_config(page_title="WK Data Sweeper", layout='wide')
st.title('Data Sweeper 💿')
st.write("Effortlessly transform your files between CSV and Excel formats with built-in data cleaning, intelligent formatting, and powerful visualization tools, enabling seamless analysis, insightful reporting, and enhanced decision-making.")
    

uploaded_files = st.file_uploader("Upload your CSV or Excel Files here;", type=("csv", "xlsx"), accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"not a correct file type, Expected csv/xlsx but got {file_ext}")
            continue
    

        st.write(f"**File Name** {file.name}")
        st.write(f"**File size** {file.size/1024} KB")

        st.write("Preview the Head of Dataframe with cool writing Animation")


        def stream_data(df):
            placeholder = st.empty()
            text = ""  # Initialize text before using it
            head_df = df.head().to_string(index=False)  # Convert DataFrame head to a string

            for char in head_df:
                text += char
                placeholder.code(text)  # Display it in a code block to mimic typing
                time.sleep(0.02)  # Adjust speed of animation

        if st.button("Click Here to Preview"):
            stream_data(df)

        




        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                if st.button(f"Fill Missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled")
                
        st.subheader("Select olumns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default = df.columns)
        df = df[columns]


        st.subheader("Data Visualizaton")
        if st.checkbox(f"Show Visuaalization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


            st.subheader ("Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext,".csv")
                    mime_type = "text/csv"
                elif conversion_type =="Excel":
                    df.to_excel(buffer, Index = False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformals-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                    st.download_button(
                        label = f"Download{file.name} as {conversion_type}",
                        data=buffer,
                        filename=file_name,
                        mime=mime_type
                    )




st.write(1234)
st.write(
    pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
)
