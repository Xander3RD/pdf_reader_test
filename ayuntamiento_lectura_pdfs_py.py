#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path, convert_from_bytes
import os 
import re
import pandas as pd
import glob
import streamlit as st
from pathlib import Path


#pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR\tesseract.exe"
gr1= []
gr2= []
gr3= []
texts= []
#aux_path= r'C:\Users\xande\Downloads\PDF_Papa\prueba\\'
with st.sidebar: 
    st.image("ayunta_imagen.png")

    st.title("Lector PDFs")
    choice = st.radio("Navegación", ["Upload","Profiling","Modelling", "Download"])
    st.info("This project application helps you build and explore your data.")

if choice == "Upload":
    st.title("Upload Your Dataset")
    
    files = st.file_uploader("Upload Your Dataset", type='pdf', accept_multiple_files=True)
    go= 'pass'
    
    button = st.button("Confirm")

    if button and files is not None:
        for file in files:
            if file is not None:
                print('holaaa ', file)
                #aux_path2= aux_path + file.name
                #pages = convert_from_path(aux_path2, 500)
                pages= convert_from_bytes(file.read())
                image_counter = 1

                # Iterate through all the pages stored above
                for page in pages:
                    filename = "page_"+str(image_counter)+".jpg"

                    # Save the image of the page in system
                    page.save(filename, 'JPEG')

                    # Increment the counter to update filename
                    image_counter = image_counter + 1


                #Part #2 - Recognizing text from the images using OCR

                # Variable to get count of total number of pages
                filelimit = image_counter-1

                # Iterate from 1 to total number of pages
                for i in range(1, filelimit + 1):

                    filename = "page_"+str(i)+".jpg"

                    # Recognize the text as string in image using pytesserct
                    text = str(((pytesseract.image_to_string(Image.open(filename)))))
                    text = text.replace('-\n', '')
                    text = text.replace('\n', ' ')
                    text = text.replace('|', '1')
                match1= re.search(r'(?:(Relacion Numero: |Relacién Numero: |Relación Numero: ))(\w*/\w*/\w*)', text)
                match2= re.search(r'(?: importe total de )(.* €)', text)
                match3= re.search(r'(?:La fecha de efectos del presente Decreto sera )((\w*/*\w*/\w*)|([0-9]* de .* de [0-9]{4}))', text)
                texts.append(text)
                try:
                    f1= match1.group(2)
                    f2= match2.group(1)
                    f3= match3.group(1).lstrip()
                    if len(f2)>20:
                        f2_2= re.search(r'(?: importe total de )(.* €)', f2)
                        f2= f2_2.group(1)

                except:
                    print(file)
                    go= 'next'

                if go=='pass':
                    gr1.append(f1)
                    gr2.append(f2)
                    gr3.append(f3)
                d= {'Relación Número': gr1, 'Importe Total': gr2, 'Fecha de Efectos del Decreto': gr3}
                df= pd.DataFrame(data= d)
    try:
        st.dataframe(df)
    except:
        print('suuuuuuuuu')

