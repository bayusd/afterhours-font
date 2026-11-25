#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D = os.path.dirname(os.path.abspath(__file__))
OTF = os.path.join(D, 'Afterhours-Regular.otf')
BG = (10, 10, 18)
def F(sz): return ImageFont.truetype(OTF, sz)
def neon_text(draw, xy, text, font, fill, glow):
    x, y = xy
    g = Image.new('RGBA', draw._image.size, (0,0,0,0))
    gd = ImageDraw.Draw(g)
    gd.text((x, y), text, font=font, fill=glow + (255,))
    g = g.filter(ImageFilter.GaussianBlur(14))
    draw._image.alpha_composite(g)
    draw.text((x, y), text, font=font, fill=fill)
# hero
W, H = 1400, 520
img = Image.new('RGBA', (W, H), BG + (255,))
d = ImageDraw.Draw(img)
neon_text(d, (60, 90), 'AFTER HOURS', F(150), (235, 245, 255), (0, 229, 255))
d.text((62, 300), 'a gothic manuscript hacked by a future city', font=F(44), fill=(255, 80, 200))
d.text((62, 380), 'Afterhours Regular  \u00b7  Gothic x Cyberpunk Display  \u00b7  by bayusd', font=F(36), fill=(150, 160, 190))
img.convert('RGB').save(os.path.join(D, 'preview-hero.png'))
# specimen
W, H = 1400, 1150
img = Image.new('RGBA', (W, H), BG + (255,))
d = ImageDraw.Draw(img)
y = 40
d.text((60, y), 'ABCDEFGHIJKLM', font=F(96), fill=(235, 245, 255)); y += 130
d.text((60, y), 'NOPQRSTUVWXYZ', font=F(96), fill=(235, 245, 255)); y += 130
d.text((60, y), 'abcdefghijklm', font=F(96), fill=(0, 229, 255)); y += 130
d.text((60, y), 'nopqrstuvwxyz', font=F(96), fill=(0, 229, 255)); y += 130
d.text((60, y), '0123456789 . , ! ? - \' : ; &', font=F(96), fill=(255, 80, 200)); y += 150
d.text((60, y), 'AFTER HOURS', font=F(150), fill=(235, 245, 255)); y += 200
d.text((60, y), 'After Hours - heading sample', font=F(72), fill=(150, 160, 190)); y += 110
d.text((60, y), 'The city never sleeps. 0123456789', font=F(54), fill=(200, 210, 230))
img.convert('RGB').save(os.path.join(D, 'preview-specimen.png'))
print('rendered')
