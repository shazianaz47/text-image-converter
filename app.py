
import streamlit as st
import time
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import io

# Custom CSS for Animation
st.markdown("""
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .animated-text {
        animation: fadeIn 2s ease-in-out;
        font-size: 34px;
        font-weight: bold;
        color:rgb(13, 9, 92);
        text-align: center;
        margin-top: 10px;
    }
    .centered {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Load & Display Logo
logo_path = "logo.png"  # Ensure logo.png is available in the working directory

# Create a horizontal layout
col1, col2 = st.columns([1, 3])  # First column (logo), second column (text)

with col1:
    st.image(logo_path, width=60)  

with col2:
# Animated Welcome Message
    st.markdown('<div class="animated-text">Welcome to Design-o-Pedia</div>', unsafe_allow_html=True)

# Streamlit App Title
st.title("📝 Text-to-Image & Image-to-Text Converter")

# Select Feature
option = st.radio("Choose a feature:", ["Text to Image", "Image to Text"])

# 🖼️ TEXT TO IMAGE SECTION
if option == "Text to Image":
    user_text = st.text_input("Enter your text:")
    font_size = st.slider("Select Font Size", 10, 100, 40)
    color = st.color_picker("Pick a Text Color", "#000000")  # Default black

    def create_image(text, font_size, color):
        img = Image.new("RGB", (500, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text_position = (50, 130)
        draw.text(text_position, text, fill=color, font=font)

        return img

    if st.button("Generate Image"):
        if user_text:
            with st.spinner("Generating Image..."):
                time.sleep(2)  # Simulating a loading effect
                image = create_image(user_text, font_size, color)
                st.image(image, caption="Generated Image", use_container_width=True)

                # Download Image Option
                img_io = io.BytesIO()
                image.save(img_io, format="PNG")
                img_io.seek(0)
                st.download_button(label="📥 Download Image", data=img_io, file_name="generated_image.png", mime="image/png")
        else:
            st.warning("Please enter some text to generate an image.")

# 🔍 IMAGE TO TEXT SECTION
elif option == "Image to Text":
    uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                time.sleep(2)
                extracted_text = pytesseract.image_to_string(image)
                st.text_area("Extracted Text:", extracted_text, height=150)

                # Copy to Clipboard Button (For web, this feature depends on JS)
                st.write("✅ Text extracted successfully!")

# USER REVIEW FEATURE
st.markdown("---")
st.subheader("💬 User Reviews")

# Initialize session state for storing reviews
if "reviews" not in st.session_state:
    st.session_state.reviews = []

# Text area for user to enter review
user_review = st.text_area("Write your review about this tool:")

if st.button("Submit Review"):
    if user_review.strip():  # Check if review is not empty
        st.session_state.reviews.append(user_review)
        st.success("✅ Thank you for your feedback!")
    else:
        st.warning("⚠️ Please write something before submitting.")

# Display user reviews
if st.session_state.reviews:
    st.markdown("### 📝 User Feedback")
    for idx, review in enumerate(st.session_state.reviews[::-1], start=1):  # Reverse order to show latest first
        st.write(f"**{idx}.** {review}")