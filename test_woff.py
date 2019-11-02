#!/usb/bin/python
# coding=utf-8
import os

import PIL.Image, PIL.ImageDraw, PIL.ImageFont
import chardet
from pytesseract import pytesseract

from PIL import Image


if __name__ == "__main__":

    image=PIL.Image
    ImageDraw=PIL.ImageDraw
    ImageFont=PIL.ImageFont

    # \ue110.\uf5c5
    text = "\uf2ce万"
    # text = "\uea79\uea79"
    print("__main__::text = ", text)


    im = image.new("RGB", (300, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("mao_yan_font.woff"), 30)

    dr.text((50, 10), text+text, font=font, fill="#000000")

    # im.show()
    im.save("test_font.png")

    image2 = Image.open("test_font.png")
    code = pytesseract.image_to_string(image2)
    print(code)

    # font1 = TTFont('base_mao_yan_font.woff')
    # cmap=font1['cmap']
    # cdict=cmap.getBestCmap()
    # acs=ord('3')
    # print (acs)
    # print(cdict)
