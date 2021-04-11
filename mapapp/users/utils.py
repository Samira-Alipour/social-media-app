from flask import current_app
import os, secrets
from PIL import Image

def save_picture(picture):
	_, ext = os.path.splitext(picture.filename)
	random_hex = secrets.token_hex(8)
	filename = random_hex + ext
	file_path = os.path.join(current_app.root_path, 'static/images' , filename)
	i = Image.open(picture)
	output_size =(200,200)
	i.thumbnail(output_size)
	i.save(file_path)
	return filename
