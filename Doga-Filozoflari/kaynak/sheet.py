import sys, os
from PIL import Image, ImageDraw
out = sys.argv[1]; fs = sys.argv[2:]; c = 6; tw, th = 320, 220
rows = (len(fs) + c - 1) // c; S = Image.new("RGB", (c * tw, rows * th), (30, 30, 30)); d = ImageDraw.Draw(S)
for k, f in enumerate(fs):
    im = Image.open(f).convert("RGB"); w, h = im.size; im.thumbnail((tw - 6, th - 26))
    x, y = (k % c) * tw, (k // c) * th; S.paste(im, (x + 3, y + 3)); d.text((x + 4, y + th - 20), f"{os.path.basename(f)[:30]} {w}x{h}", fill=(255, 255, 0))
S.save(out, quality=80)
