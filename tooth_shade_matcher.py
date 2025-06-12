import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="AffoDent Tooth Shade Matcher", layout="centered")

st.title("🦷 AffoDent Tooth Shade Matcher")
st.markdown("Upload a close-up photo of the patient's tooth and click to match with a dental shade.")

# Define shade guide (Vita Classical) with approximate RGB
shade_guide = {
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

# Function to find closest shade
def get_closest_shade(input_rgb):
    min_dist = float('inf')
    closest = None
    for name, rgb in shade_guide.items():
        dist = np.linalg.norm(np.array(input_rgb) - np.array(rgb))
        if dist < min_dist:
            min_dist = dist
            closest = name
    return closest

# Upload image
uploaded_image = st.file_uploader("Upload a tooth image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="Uploaded Tooth Image", use_column_width=True)

    st.markdown("### Click to select a point on the image")
    st.markdown("*(Note: In this demo, click functionality is simulated)*")

    x = st.slider("Select X pixel", 0, img_array.shape[1]-1, img_array.shape[1]//2)
    y = st.slider("Select Y pixel", 0, img_array.shape[0]-1, img_array.shape[0]//2)

    selected_color = img_array[y, x]
    selected_rgb = tuple(int(v) for v in selected_color)

    st.markdown(f"**Selected Pixel Color:** RGB{selected_rgb}")
    st.color_picker("Preview", value="#%02x%02x%02x" % selected_rgb, label_visibility="collapsed")

    # Find closest shade
    match = get_closest_shade(selected_rgb)
    st.success(f"✅ Closest Match: **{match}** (RGB {shade_guide[match]})")

    # Optional manual override
    manual = st.selectbox("Or manually select shade", list(shade_guide.keys()))
    st.info(f"Manually selected: {manual}")
