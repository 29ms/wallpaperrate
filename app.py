import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import cv2

# Define custom text outputs for each rating possibility
rating_texts = {
    -10: "L WALLPAPER 😂",
    -9: "Absolute trash.",
    -8: "Terrible wallpaper",
    -7: "Awful just awful",
    -6: "Get a new wallpaper ASAP (rocky)",
    -5: "Pretty damn bad",
    -4: "Very bad",
    -3: "Very bad",
    -2: "WAY Below average. Needs work.",
    -1: "Awful",
    0: "Zero. Cmon dude",
    1: "Not good at all",
    2: "It should probably be lower.",
    3: "L wallpaper",
    4: "Big L Wallpaper",
    5: "Mid",
    6: "Above mid",
    7: "Not bad",
    8: "Pretty good",
    9: "Exceptional quality. Very impressive.",
    10: "W Wallpaper 💯"
}

def is_blurry(image):
    """Check if the image is blurry using the variance of Laplacian method."""
    image_np = np.array(image.convert("L"))
    focus = cv2.Laplacian(image_np, cv2.CV_64F).var()
    return focus < 500  # Adjust threshold as needed

def rate_image(image_path):
    """Rate the image based on various criteria."""
    image = Image.open(image_path)
    
    score = 10
    
    # Criteria for rating
    if is_blurry(image):
        score -= 3
    
    # Resolution check
    width, height = image.size
    if width < 1280 or height < 720:
        score -= 2
    
    # Brightness check
    brightness = np.mean(np.array(image.convert('L')))
    if brightness < 100:
        score -= 2
    
    # Color Vibrancy
    colorfulness = np.std(np.array(image), axis=(0, 1)).mean()
    if colorfulness < 30:
        score -= 1
    
    # Clutter (edges)
    edges = cv2.Canny(np.array(image.convert('L')), 100, 200)
    clutter = np.mean(edges)
    if clutter > 200:
        score -= 2
    
    # Normalize score within range
    score = max(-10, min(score, 10))
    return score, rating_texts.get(score, "Rating not available")

# Streamlit UI
st.title("Wallpaper Rating System")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    score, rating = rate_image("temp.jpg")
    st.write(f"Rating: {score} - {rating}")
