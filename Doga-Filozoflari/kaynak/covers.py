# Doga covers: Kapak-16x9-A/B (1280x720), Kapak-9x16-A/B (1080x1920). Anton, white + yellow, no signature.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K = os.path.join(R, "kaynak")
G = os.path.join(R, "gorseller", "secilen"); OUT = os.path.join(R, "teslim")
ANTON = os.path.join(K, "fonts", "Anton-Regular.ttf")
YEL = (255, 206, 46)

def cover_fit(im, W, H, ax=0.5, ay=0.4):
    r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * ax); y = int((im.height - H) * ay); return im.crop((x, y, x + W, y + H))

def text(d, xy, s, size, fill, anchor="la", stroke=6):
    f = ImageFont.truetype(ANTON, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(10, 10, 10))
    return d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke)

def make(name, img, W, H, lines, ax=0.5, ay=0.35, strike_line=None, side="left", ytop=None, right_portrait=False):
    src = Image.open(os.path.join(G, img)).convert("RGB")
    if right_portrait:   # portrait on the right, blurred self on the left
        im = ImageEnhance.Brightness(cover_fit(src, W, H, 0.5, 0.4).filter(ImageFilter.GaussianBlur(30))).enhance(0.5)
        r = H / src.height; fg = src.resize((round(src.width * r), H), Image.LANCZOS); im.paste(fg, (W - fg.width, 0))
    else:
        im = cover_fit(src, W, H, ax, ay)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    # soft shadow behind text only (glow under letters, not a band)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    vert = H > W
    x = W // 2 if vert else (60 if side == "left" else W - 60)
    anchor = ("m" if vert else ("l" if side == "left" else "r"))
    y = int(H * (ytop if ytop is not None else (0.12 if vert else 0.1)))
    boxes = []
    for s, size, col in lines:
        b = text(d, (x, y), s, size, col, anchor + "t", stroke=max(4, size // 18)); boxes.append(b); y = b[3] + int(size * 0.12)
    for li in ([] if strike_line is None else ([strike_line] if isinstance(strike_line, int) else strike_line)):
        b = boxes[li]; yy = (b[1] + b[3]) // 2
        d.line([(b[0] - 10, yy), (b[2] + 10, yy)], fill=(230, 40, 40), width=max(8, (b[3] - b[1]) // 9))
    sh = layer.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.6))
    base = im.convert("RGBA"); base.paste((0, 0, 0, 255), (0, 0), sh); base.alpha_composite(layer)
    base.convert("RGB").save(os.path.join(OUT, name + ".png"))

A = [("EVREN", 150, (255, 255, 255)), ("NEYDEN", 150, (255, 255, 255)), ("YAPILDI?", 170, YEL)]
B = [("2600 YILLIK", 130, (255, 255, 255)), ("KAVGA", 200, YEL)]
make("Kapak-16x9-A", "atina-merkez.jpg", 1280, 720, A, ax=0.5, ay=0.5, side="left", ytop=0.12)
make("Kapak-16x9-B", "rubens-ikili.jpg", 1280, 720, B, ax=0.5, ay=0.3, side="left", ytop=0.5)
A9 = [("EVREN", 210, (255, 255, 255)), ("NEYDEN", 210, (255, 255, 255)), ("YAPILDI?", 220, YEL)]
B9 = [("2600 YILLIK", 160, (255, 255, 255)), ("KAVGA", 260, YEL)]
make("Kapak-9x16-A", "atina-merkez.jpg", 1080, 1920, A9, ax=0.5, ay=0.5, ytop=0.08)
make("Kapak-9x16-B", "rubens-ikili.jpg", 1080, 1920, B9, ax=0.62, ay=0.5, ytop=0.62)
print("covers ok")
