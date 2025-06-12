import streamlit as st
import numpy as np
from PIL import Image
import cv2
from streamlit_drawable_canvas import st_canvas

# Page setup
st.set_page_config(page_title="Tooth Shade Matcher - AffoDent", layout="centered")
st.title("🦷 AffoDent Tooth Shade Matcher")
st.markdown("Upload a clear photo of the patient's tooth and **tap on the tooth** to find the closest matching shade from the Vita Classical shade guide.")

# Shade reference (Vita Classical)
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

# Convert RGB to Lab
def rgb_to_lab(rgb):
    rgb_arr = np.uint8([[list(rgb)]])
    lab = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2LAB)
    return lab[0][0]

# Find closest shade in Lab space
def get_closest_shade_lab(input_rgb):
    input_lab = rgb_to_lab(input_rgb)
    closest = None
    min_dist = float("inf")
    for shade, ref_rgb in shade_guide_rgb.items():
        ref_lab = rgb_to_lab(ref_rgb)
        dist = np.linalg.norm(input_lab - ref_lab)
        if dist < min_dist:
            min_dist = dist
            closest = shade
    return closest

# Upload image
uploaded_image = st.file_uploader("📤 Upload tooth image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    img_array = np.array(image)

    st.markdown("### ✏️ Click on the tooth to detect its color")

    # Convert to RGBA for canvas
    rgba_image = image.convert("RGBA")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=1,
        background_image=rgba_image,
        update_streamlit=True,
        height=rgba_image.height,
        width=rgba_image.width,
        drawing_mode="point",
        point_display_radius=5,
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        last_point = canvas_result.json_data["objects"][-1]
        x = int(last_point["left"])
        y = int(last_point["top"])

        if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
            selected_rgb = tuple(int(c) for c in img_array[y, x])
            st.markdown(f"🎯 **Selected RGB:** {selected_rgb}")
            st.color_picker("Color Preview", value="#%02x%02x%02x" % selected_rgb, label_visibility="collapsed")

            match = get_closest_shade_lab(selected_rgb)
            st.success(f"🟢 Closest Match: **{match}**")
            st.markdown(f"Reference RGB: `{shade_guide_rgb[match]}`")
    else:
        st.info("Click anywhere on the image to sample the tooth color.")
