import streamlit as st
from PIL import Image
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from core.image_transformation import load_and_process_image, rotate_image, translate_image, scale_image

st.set_page_config(page_title="Basic Image Transformation", layout="wide")

# Sidebar
st.sidebar.title("Controls")
uploaded_image = st.sidebar.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

# Main area
st.title(f"Basic Image Transformation")

# Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Uploaded Image")
    if uploaded_image is not None:
    # Display the uploaded image
        image = Image.open(uploaded_image)
        #Display the image
        st.image(image, caption="Uploaded Image", width=400, output_format="auto")

with col2:
    st.subheader("Processed Grayscale Image")
    if uploaded_image is not None:
    # Display the processed image
        processed_image_matrix = load_and_process_image(uploaded_image)
        processed_image = Image.fromarray(processed_image_matrix)
        st.image(processed_image, caption="Grayscale Image", width=400, output_format="auto")

st.markdown("---")
st.title("Transformation Menu")
st.subheader("Choose Transformation Type")
tab1, tab2, tab3 = st.tabs(["Rotation", "Translation", "Scaling"])

with tab1:
    st.write("Apply Rotation on an Image")
    if uploaded_image is not None:
        degree = st.number_input("Enter Rotation value (in deg)")
        if st.button("Apply Rotation", key="rotate"):
            with st.spinner("Applying Image Rotation..."):
                rotate_image_matrix = rotate_image(processed_image_matrix, degree)
                rotate_image = Image.fromarray(rotate_image_matrix)
                st.image(rotate_image, caption=f"Image Rotate at {degree} degree", width=400)
                st.success("Image Rotated Successfully")

with tab2:
    st.write("Apply Translation on an Image")
    if uploaded_image is not None:
        tx = st.number_input("Enter translation x value")
        ty = st.number_input("Enter translation y value")
        if st.button("Apply Translation", key="translate"):
            with st.spinner("Applying Image Translation..."):
                translate_image_matrix = translate_image(processed_image_matrix, tx, ty)
                translate_image = Image.fromarray(translate_image_matrix)
                st.image(translate_image, caption=f"Image Translation with tx:{tx}, ty:{ty}", width=400)
                st.success("Image Translated Successfully")

with tab3:
    st.write("Apply Scaling on an Image")
    if uploaded_image is not None:
        scaling_factor = st.number_input("Enter Scaling factor",value=1.0)
        if st.button("Apply Scaling", key="scale"):
            with st.spinner("Applying Image Scaling..."):
                scale_image_matrix = scale_image(processed_image_matrix, scaling_factor)
                scale_image = Image.fromarray(scale_image_matrix)
                st.image(scale_image, caption=f"Image scaled by {scaling_factor}", width=400)
                st.success("Image Scaled Successfully")
