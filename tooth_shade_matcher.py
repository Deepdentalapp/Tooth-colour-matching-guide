# app.py

import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="AffoDent Tooth Shade Matcher (Lab Based)", layout="centered")

st.title("🦷 AffoDent Tooth Shade Matcher")
st.markdown("Upload a close-up photo of the tooth and select a point to match the closest shade using Lab color space.")

# Vita Classical shades with RGB references
shade_guide_rgb = {
    "A1": (255, 240, 220),
    "A2": (240, 224, 200),
    "A3": (225, 205, 185),
    "A3.5": (210, 190, 170),
    "B1": (250, 235, 210),
    "B2": (235, 215, 190),
    "C1": (220, 200, 180),
    "C2": (205, 185, 165),
    "D2": (200, 180, 160)
}

# Convert RGB to Lab using OpenCV
def rgb_to_lab(rgb):
    pixel = np.uint8([[list(rgb)]])
    lab = cv2.cvtColor(pixel, cv2.COLOR_RGB2LAB)
    return lab[0][0]

# Get closest shade in Lab space
def get_closest_shade_lab(input_rgb):
    input_lab = rgb_to_lab(input_rgb)
    min_dist = float('inf')
    closest_shade = None
    for name, ref_rgb in shade_guide_rgb.items():
        ref_lab = rgb_to_lab(ref_rgb)
        dist = np.linalg.norm(input_lab - ref_lab)
        if dist < min_dist:
            min_dist = dist
            closest_shade = name
    return closest_shade

# Upload image
uploaded_image = st.file_uploader("Upload a tooth image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="Uploaded Tooth Image", use_column_width=True)

    st.markdown("### Select pixel coordinates (approximate for now)")
    x = st.slider("X position", 0, img_array.shape[1] - 1, img_array.shape[1] // 2)
    y = st.slider("Y position", 0, img_array.shape[0] - 1, img_array.shape[0] // 2)

    selected_rgb = tuple(int(v) for v in img_array[y, x])
    st.markdown(f"**Selected RGB color:** {selected_rgb}")
    st.color_picker("Preview", value="#%02x%02x%02x" % selected_rgb, label_visibility="collapsed")

    match = get_closest_shade_lab(selected_rgb)
    st.success(f"✅ Closest Vita Classical Match: **{match}** (Reference RGB: {shade_guide_rgb[match]})")

    # Optional manual override
    manual = st.selectbox("Or manually select shade", list(shade_guide_rgb.keys()))
    st.info(f"Manually selected: {manual}")
