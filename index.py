from flask import Flask, send_file, make_response
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random
import string

app = Flask(__name__)

def generate_captcha_image():
    width, height = 200, 80
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 40
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('arial.ttf', font_size)
    except IOError:
        font = ImageFont.load_default()
    text_width, text_height = draw.textsize(captcha_text, font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), captcha_text, font=font, fill=text_color)
    for _ in range(10):
        start_point = (random.randint(0, width), random.randint(0, height))
        end_point = (random.randint(0, width), random.randint(0, height))
        draw.line([start_point, end_point], fill=(0, 0, 0), width=1)
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io, captcha_text

@app.route('/api/captcha', methods=['GET'])
def get_captcha():
    image_io, captcha_text = generate_captcha_image()
    response = make_response(send_file(image_io, mimetype='image/png'))
    response.headers['Captcha-Text'] = captcha_text
    return response
