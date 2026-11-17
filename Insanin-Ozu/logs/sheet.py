import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
fs=sorted(glob.glob('ai/*.jpg'))
def mk(files,tw,th,cols,out):
    rows=(len(files)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*(th+18)),(20,20,20));d=ImageDraw.Draw(S)
    for i,f in enumerate(files):
        im=Image.open(f);im.thumbnail((tw,th));x=(i%cols)*tw;y=(i//cols)*(th+18)
        S.paste(im,(x,y));d.text((x+3,y+th+2),os.path.basename(f)[:-4],fill=(255,220,120))
    S.save(out,quality=82)
mk([f for f in fs if '_w_' in f],320,182,8,'ai-sheet.jpg')
mk([f for f in fs if '_t_' in f],170,300,12,'ai-sheet-t.jpg')
