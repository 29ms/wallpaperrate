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
    -5: "Damn that's Pretty damn bad",
    -4: "Very bad",
    -3: "Simply awful.",
    -2: "WAY Below average. Needs work.",
    -1: "Awful",
    0: "How bad is this wallpaper 😂",
    0.5: "Really bru? 💀🙏",
    1: "Not good at all",
    2: "Get a new wallpaper ASAP (rocky)",
    3: "NO.",
    3.5: "No way 🤦❌",
    4: "Big L Wallpaper",
    5: "Mid",
    5.5: "Barely Mid",
    6: "Above mid 👊",
    7: "Not bad eh?",
    8: "Pretty damn good",
    9: "Ooh Lala! 👏",
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

def is_one_color(image):
    np_image = np.array(image.convert("RGB"))
    unique_colors = np.unique(np_image.reshape(-1, 3), axis=0)
    return len(unique_colors) == 1

def rate_image(image_path):
    image = Image.open(image_path)
    
    # Check if the image is only one color
    if is_one_color(image):
        return 0, rating_texts[0]  # Automatically score 0 if only one color
    
    score = 10
    
    if is_blurry(image):
        score -= 3
    if not is_bright(image):
        score -= 2
    if not is_colorful(image):
        score -= 2.5
    if not has_good_resolution(image):
        score -= 2
    
    # Normalize score to be within the defined range
    score = max(-10, min(score, 10))
    
    return score, rating_texts.get(score, "Rating not available")

# Streamlit UI with custom styles
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;
    }
    .main-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        max-width: 800px;
        margin: 40px auto;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #333333;
    }
    .upload-area {
        text-align: center;
        padding: 20px;
        border: 2px dashed #bbbbbb;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 20px;
    }
    .rating-output {
        text-align: center;
        font-size: 1.5em;
        color: #555555;
        margin-top: 20px;
    }
    .uploaded-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 15px;
        border: 3px solid #eeeeee;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-container">
        <h1 class="title">AI Wallpaper Rater</h1>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True, output_format="PNG")
    
    score, rating = rate_image("temp.jpg")
    st.markdown(f'<div class="rating-output">Rating: {score} - {rating}</div>', unsafe_allow_html=True)
