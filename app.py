import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import uuid
import os

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

# Initialize session state for rating history
if "rating_history" not in st.session_state:
    st.session_state.rating_history = []
if "current_image_path" not in st.session_state:
    st.session_state.current_image_path = None

def is_blurry(image):
    grayscale_image = image.convert("L")
    edges = grayscale_image.filter(ImageFilter.FIND_EDGES)
    variance = np.var(np.array(edges))
    return variance < 50

def is_bright(image):
    np_image = np.array(image.convert("RGB"))
    avg_brightness = np.mean(np_image)
    return avg_brightness > 100

def is_colorful(image):
    np_image = np.array(image.convert("RGB"))
    colors = np_image.reshape(-1, 3)
    unique_colors = np.unique(colors, axis=0)
    return len(unique_colors) > 1000

def has_good_resolution(image):
    width, height = image.size
    return width >= 800 and height >= 600

def is_one_color(image):
    np_image = np.array(image.convert("RGB"))
    unique_colors = np.unique(np_image.reshape(-1, 3), axis=0)
    return len(unique_colors) == 1

def rate_image(image_path):
    image = Image.open(image_path)
    
    if is_one_color(image):
        return 0, rating_texts[0]
    
    score = 10
    
    if is_blurry(image):
        score -= 3
    if not is_bright(image):
        score -= 2
    if not is_colorful(image):
        score -= 2.5
    if not has_good_resolution(image):
        score -= 2
    
    score = max(-10, min(score, 10))
    
    return score, rating_texts.get(score, "Rating not available")

def add_to_history(image_path, score, rating):
    st.session_state.rating_history.append({
        "image_path": image_path,
        "score": score,
        "rating": rating
    })

def clear_history():
    st.session_state.rating_history = []
    st.session_state.current_image_path = None

# Streamlit UI with custom styles
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .main-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        max-width: 900px;
        margin: 40px auto;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #333333;
        margin-bottom: 20px;
    }
    .upload-area {
        text-align: center;
        padding: 20px;
        border: 2px dashed #bbbbbb;
        border-radius: 10px;
        background-color: #f7f9fc;
        margin-bottom: 20px;
    }
    .image-rating-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .uploaded-image {
        border-radius: 15px;
        border: 3px solid #e1e4e8;
        margin-right: 20px;
    }
    .rating-output {
        font-size: 1.5em;
        color: #444444;
        margin-left: 20px;
        text-align: center;
    }
    .history-container {
        margin-top: 30px;
    }
    .history-entry {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #e1e4e8;
    }
    .history-entry img {
        border-radius: 10px;
        margin-right: 20px;
    }
    .history-entry div {
        flex-grow: 1;
    }
    .clear-button {
        margin-top: 20px;
        background-color: #e63946;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        font-size: 1.2em;
        cursor: pointer;
        display: block;
        width: 100%;
        text-align: center;
    }
    .clear-button:hover {
        background-color: #d62839;
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
    unique_filename = f"temp_{uuid.uuid4().hex}.jpg"
    with open(unique_filename, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    st.session_state.current_image_path = unique_filename

    st.markdown("<div class='upload-area'>", unsafe_allow_html=True)
    st.image(unique_filename, caption="Uploaded Image", use_column_width=True, output_format="PNG", class_="uploaded-image")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<div class="image-rating-container"><img src="{unique_filename}" class="uploaded-image" /><div class="rating-output">Rating: {rating} - {rating_text}</div></div>', unsafe_allow_html=True)
    
    with col2:
        score, rating_text = rate_image(unique_filename)
        st.markdown(f'<div class="rating-output">Rating: {score} - {rating_text}</div>', unsafe_allow_html=True)
        add_to_history(unique_filename, score, rating_text)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<h2 class='title'>Rating History</h2>", unsafe_allow_html=True)

if st.button("Clear History", key="clear_history", class_="clear-button"):
    clear_history()

if st.session_state.rating_history:
    st.write("---")
    for entry in st.session_state.rating_history:
        col1, col2 = st.columns([1, 3])
        with col1:
            image = Image.open(entry["image_path"])
            st.image(image, width=100)
        with col2:
            st.write(f"Rating: {entry['score']} - {entry['rating']}")
else:
    st.write("No history yet.")
