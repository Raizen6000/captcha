from flask import Flask, send_file
import io
import random
import string
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/api/captcha')
def captcha():
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    image = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png')

if __name__ == "__main__":
    app.run()
