from PIL import Image, ImageDraw, ImageFont


im = Image.open("toutu3.png")
print(im.size)
bg = Image.new("RGBA", im.size)
draw2 = Image.blend(bg, im, 1.0)
draw = ImageDraw.Draw(draw2)
ttfont = ImageFont.truetype(r"C:\Windows\Fonts\STFANGSO.TTF", 18)
draw.text((150, 85), '你好', fill=(20, 20, 20), font=ttfont)
draw2.save('draw.png')