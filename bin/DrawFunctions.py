from PIL import Image, ImageDraw, ImageFont
from .barcode import *
import os

from . import UpcFunctions

image_dir = 'images'


if not os.path.exists(image_dir):
    os.mkdir(image_dir)

BAR_COLORS = {
    "1": (0,0,0,255),
    "0": (255,255,255,255),
}

def make_barcode(bars_list, upc:str, scale=2, colors=BAR_COLORS, display_numbers=True, img_height=None, image_path=None):

    width = scale
    if not img_height:
        img_height = 80 * width
    x, y = 0, 0
    short = int(img_height - 10 * width)
    tall = int(img_height - 3 * width)
    module_width = scale * 7
    char_padding_x = scale
    char_padding_y = scale * 2
    char_width = module_width - char_padding_x * 2
    char_height = (img_height - short) - char_padding_y
    char_height = int(char_height * 0.9)
    print(char_height, img_height)
    char_y = img_height - char_height - char_padding_y
    total_bits = 0

    for bars in bars_list:
        for bar in bars:
            total_bits += bar[0]
    if not image_path:
        image_path = os.path.join(image_dir, upc + '.png')
    im = Image.new('RGBA', (width * total_bits, img_height), color=colors['0'])
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(os.path.join('fonts', 'mono.ttf'), size=char_height)
    index = 0
    for bars in bars_list:
        bar_height = short
        if len(bars) != 4:
            bar_height = tall
        else:
            if display_numbers:
                left = index < len(bars_list) // 2

                bar_text = UpcFunctions.get_digit_from_bars(bars, left)
                char_coordinates = [x + char_padding_x, char_y]
                draw.text(char_coordinates, bar_text, fill=colors['1'])


        for bar in bars:
            bar_width = bar[0] * width - 1
            draw.rectangle([x, y, x + bar_width, y + bar_height], fill=colors[str(bar[1])], width=0, outline=None)
            x += bar_width + 1
        index += 1

    im.save(image_path, 'PNG')

def make_barcode_path(upc:str):
    upc = makeNumeric(upc)
    upc = upc[0:11]
    imgpath = os.path.join(os.getcwd(), "cache", "%s.temp.png" % upc)
    upc += str(UpcFunctions.get_checkdigit(upc))

    upc_encoding = UpcFunctions.get_upc_encoding(upc)
    upc_bar_data = UpcFunctions.get_bars(upc_encoding)
    make_barcode(upc_bar_data, upc, scale=3, img_height=150, image_path=imgpath)
    return imgpath
