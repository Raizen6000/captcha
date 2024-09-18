from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

app = Flask(__name__)

def generate_captcha(text_length=6):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=text_length))
    
    width, height = 200, 70
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(captcha_text, font=font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), captcha_text, font=font, fill=(0, 0, 0))
 
    for _ in range(5):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(0, 0, 0), width=2)
      
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    return image_bytes

@app.route('/generate-captcha')
def generate_captcha_route():
    image_bytes = generate_captcha()
    return send_file(image_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
