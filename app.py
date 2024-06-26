# app.py
from flask import Flask, request, send_file, render_template  # Import render_template
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Create Flask app
app = Flask(__name__)

# Default route to render the form and handle POST requests
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Extract the form data for the prompt
        prompt = request.form.get("prompt", "")
        if prompt:  # Ensure prompt is not empty
            # Call generate_meme with the extracted prompt
            return generate_meme(prompt)
        else:
            return "Please enter some text to generate a meme.", 400
    
    # Render the HTML form on a GET request
    return render_template("index.html")

# Generate meme from a prompt
@app.route("/generate_meme", methods=["POST"])
def generate_meme(prompt=None):
    if prompt is None:
        prompt = request.form.get("prompt", "")  # Handle form data
        if not prompt:
            return {"error": "No prompt provided"}, 400

    # Fetch a random image from a predefined URL
    image_url = "https://source.unsplash.com/random/800x600"
    response = requests.get(image_url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch image"}, 500
    
    # Load the image into Pillow
    image = Image.open(io.BytesIO(response.content))

    # Draw text on the image
    draw = ImageDraw.Draw(image)
    font_path = "arial.ttf"  # Path to a TrueType font
    font = ImageFont.truetype(font_path, 40)

    text = prompt.upper()  # Convert text to uppercase for meme-like style

    # Calculate text position using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    width, height = image.size
    text_x = (width - text_width) / 2
    text_y = height - text_height - 10  # Position text near the bottom
    
    # Add text to the image
    draw.text((text_x, text_y), text, font=font, fill="white")

    # Save the image to a BytesIO object to send as a response
    image_io = io.BytesIO()
    image.save(image_io, "JPEG")
    image_io.seek(0)
    
    # Return the image as a response
    return send_file(image_io, mimetype="image/jpeg")
