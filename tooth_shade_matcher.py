import streamlit as st
import numpy as np
from PIL import Image
import cv2
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="AffoDent Tooth Shade Matcher", layout="centered")

st.title("🦷 AffoDent Tooth Shade Matcher")
st.markdown("Upload a clear tooth photo, then **tap or click** on the tooth to match the closest Vita Classical shade using **Lab color analysis**.")

# Vita shade guide with reference RGB values
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
    rgb_array = np.uint8([[list(rgb)]])
    lab = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2LAB)
    return lab[0][0]

# Find closest shade in Lab color space
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

# File uploader
uploaded_image = st.file_uploader("Upload a tooth image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    img_array = np.array(image)

    st.markdown("### 👆 Click on the image to pick the tooth color")

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
        stroke_width=1,
        background_image=image.convert("RGBA"),  # ✅ Proper format for canvas
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        point_display_radius=5,
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        point = canvas_result.json_data["objects"][-1]
        x = int(point["left"])
        y = int(point["top"])

        if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
            selected_rgb = tuple(int(c) for c in img_array[y, x])
            st.markdown(f"**Selected Pixel RGB:** {selected_rgb}")
            st.color_picker("Color Preview", value="#%02x%02x%02x" % selected_rgb, label_visibility="collapsed")

            matched_shade = get_closest_shade_lab(selected_rgb)
            st.success(f"✅ Closest Vita Classical Match: **{matched_shade}**")
            st.markdown(f"Reference RGB: `{shade_guide_rgb[matched_shade]}`")
    else:
        st.info("Click on the tooth area to pick a color.")
