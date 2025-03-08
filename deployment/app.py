# app.py

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import torch
import base64
import os

# Load model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/content/drive/MyDrive/best.pt')

# Function to get base64 encoding of a file
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp{
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to predict disease
def predict(image):
    result = model(image)
    st.image(result.render()[0], caption='Uploaded Image', use_column_width=True)
    labels = result.xyxy
    labels = labels[0]
    if list(labels.shape)[0] == 0:
        return "Healthy"
    m = labels[0][-1]
    if m == 0:
        # Bacterial blight
        st.write("Detected Disease: Bacterial blight")
        st.write("""Here are some recommendations for managing bacterial blight in cotton plants:
        1. Use disease-free seeds.
        2. Practice crop rotation.
        3. Sanitation.
        4. Chemical control.
        5. Cultural control.
        6. Monitoring.""")
    elif m == 2:
        # Cotton leaf curl virus (CLCuV)
        st.write("Detected Disease: Cotton leaf curl virus (CLCuV)")
        st.write("""Here are some recommendations for managing CLCuV in cotton plants:
        1. Crop rotation.
        2. Use of resistant varieties.
        3. Chemical control.
        4. Sanitation.""")
    elif m == 1:
        # Fusarium wilt
        st.write("Detected Disease: Fusarium wilt")
        st.write("""Here are some recommendations for managing Fusarium wilt in cotton plants:
        1. Crop rotation.
        2. Use of resistant varieties.
        3. Chemical control.
        4. Sanitation.""")

# Main app
def main():
    set_background('/content/Background.jpg')
    st.title('Plant Disease Detection')
    uploaded_file = st.file_uploader("Please upload an image", type=['jpg', 'png', 'jpeg'])
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        predict(uploaded_file)

if __name__ == "__main__":
    main()
