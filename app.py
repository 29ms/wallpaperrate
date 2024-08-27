import streamlit as st
from PIL import Image, ImageFilter
import numpy as np

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
    """Check if the image is blurry using the variance of Laplacian method with PIL."""
    grayscale_image = image.convert("L")  # Convert to grayscale
    edges = grayscale_image.filter(ImageFilter.FIND_EDGES)
    variance = np.var(np.array(edges))
    return variance < 50  # Adjust threshold as needed

def is_bright(image):
    """Check if the image is bright enough."""
    np_image = np.array(image.convert("RGB"))
    avg_brightness = np.mean(np_image)
    return avg_brightness > 100  # Adjust brightness threshold as needed

def is_colorful(image):
    """Check if the image has good color variance."""
    np_image = np.array(image.convert("RGB"))
    colors = np_image.reshape(-1, 3)
    unique_colors = np.unique(colors, axis=0)
    return len(unique_colors) > 1000  # Adjust number of unique colors as needed

def has_good_resolution(image):
    """Check if the image has a good resolution."""
    width, height = image.size
    return width >= 800 and height >= 600  # Adjust these values as needed

def rate_image(image_path):
    """Rate the image based on various criteria."""
    image = Image.open(image_path)
    
    score = 10
    
    # Criteria for rating
    if is_blurry(image):
        score -= 3
    if not is_bright(image):
        score -= 2
    if not is_colorful(image):
        score -= 2.5  # Penalize low color variance by 2.5 points
    if not has_good_resolution(image):
        score -= 2  # Penalize low-resolution images

    # Ensure the maximum score is 10
    score = min(score, 10)
    # Ensure the score does not go below -10
    score = max(score, -10)
    
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
