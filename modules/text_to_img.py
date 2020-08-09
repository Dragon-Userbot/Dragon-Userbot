from pyrogram import Message, Filters
from PIL import Image, ImageDraw, ImageFont
from utils import app
import time


@app.on_message(Filters.command('tti', ['.']) & Filters.me)
def text_to_img(client, message):
	text_color = message.command[1]
	background_color = message.command[2]
	text = ' '.join(message.command[3:])
	font_size = 20
	message.delete()
	print(text)
	font = ImageFont.truetype("modules/arial.ttf", 20)
	width = font.getsize(max(text.split('\n'), key=len))[0] + 40
	height = font.getsize(text.split('\n')[0])[1] * text.count('\n') + 40
	font = ImageFont.truetype("modules/arial.ttf", font_size)
	img = Image.new('RGB', (width, height), color=f'{background_color}')
	draw = ImageDraw.Draw(img)
	draw.text((10, 10), text, font=font, fill=f'{text_color}')
	img.save('img.png')

	client.send_photo(message.chat.id, 'img.png')

