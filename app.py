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

def rate_image(image_path):
    """Rate the image based on various criteria."""
    image = Image.open(image_path)
    
    score = 10

    # Criteria for rating
    
    # Check if the image is blurry
    if is_blurry(image):
        score -= 3
    
    # Check for low resolution (must be HD or higher)
    width, height = image.size
    if width < 1920 or height < 1080:
        score -= 3
    
    # Check brightness (must be sufficiently bright)
    grayscale_image = image.convert('L')
    brightness = np.mean(np.array(grayscale_image))
    if brightness < 120:
        score -= 2
    
    # Check color vibrancy (requires some level of color variation)
    color_image = np.array(image)
    if color_image.ndim == 3:
        colorfulness = np.std(color_image, axis=(0, 1)).mean()
        if colorfulness < 50:
            score -= 2
    
    # Additional criteria to make the rating 10 more exclusive
    if (is_blurry(image) or width < 1920 or height < 1080 or brightness < 120 or colorfulness < 50):
        score = max(score, 9)  # Enforce minimum score of 9 for rating 10
    
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
