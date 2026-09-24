"""Make mobile comparison compositions from the current SVG artwork.

These are visual layouts, not screenshots from a running browser.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from pathlib import Path
root=Path(__file__).resolve().parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(s,b=False):return ImageFont.truetype(bold if b else font,s)
normal=[('CD4','#558ec5','#d5edfc',(19,16),(34,24),'fork'),('CD30','#df857d','#fff0e9',(83,16),(71,25),'cluster'),('CD7','#9379bc','#e6d8fb',(11,54),(19,58),'missing'),('Ki-67','#81a995','#d9f6e7',(86,80),(54,51),'ring')]
other=[('CD30','#f05b3f','#ffddd1',(83,14),(72,25),'cluster'),('CD7','#8840c6','#e5d1f8',(11,46),(22,60),'violet'),('BCL2','#d68f24','#ffebbc',(15,84),(37,69),'cyto'),('p53','#06add6','#cbf1f8',(84,77),(54,51),'nuclear')]
def label(canvas,draw,x,y,name,color,pale):
 w={'Ki-67':84,'BCL2':84}.get(name,79)
 under=Image.new('RGBA',canvas.size);sd=ImageDraw.Draw(under);sd.rounded_rectangle((x-w/2,y-16+5,x+w/2,y+20+5),radius=18,fill=(90,84,100,25))
 canvas.alpha_composite(under.filter(ImageFilter.GaussianBlur(8)))
 draw.rounded_rectangle((x-w/2,y-20,x+w/2,y+20),radius=19,fill=pale if name!='CD30' else '#ffccbf',outline='#ffffff',width=1)
 draw.text((x-w/2+18,y-10),name,font=F(15,True),fill='#9e3930' if name=='CD30' else '#3d5f81')
def receptor(canvas,draw,x,y,color,glyph):
 dark=tuple(max(0,int(v*.68)) for v in ImageColor.getrgb(color))
 light=tuple(min(255,int(v*.55+255*.45)) for v in ImageColor.getrgb(color))
 halo=Image.new('RGBA',canvas.size)
 ImageDraw.Draw(halo).ellipse((x-23,y-26,x+23,y+24),fill=(*ImageColor.getrgb(color),55 if glyph!='missing' else 24))
 canvas.alpha_composite(halo.filter(ImageFilter.GaussianBlur(10)))
 draw=ImageDraw.Draw(canvas)
 def orb(xx,yy,r):
  draw.ellipse((xx-r+1,yy-r+3,xx+r+1,yy+r+3),fill=(*dark,100))
  draw.ellipse((xx-r,yy-r,xx+r,yy+r),fill=color,outline=dark,width=1)
  draw.ellipse((xx-r+1,yy-r+1,xx+r-3,yy+r-3),fill=light)
  draw.ellipse((xx-r+2,yy-r+1,xx-r+5,yy-r+4),fill='#fff8f5')
 if glyph=='violet':
  draw.line((x+16,y,x-4,y),fill=dark,width=9);draw.line((x-4,y,x-17,y-13),fill=dark,width=8);draw.line((x-4,y,x-18,y+12),fill=dark,width=8)
  draw.line((x+15,y,x-3,y),fill=color,width=6);draw.line((x-3,y,x-17,y-13),fill=color,width=6);draw.line((x-3,y,x-18,y+12),fill=color,width=6)
  for xx,yy in ((x-19,y-15),(x-19,y+14),(x-5,y)):orb(xx,yy,7)
 elif glyph=='cyto':
  for xx,yy in ((x-12,y-7),(x+9,y-10),(x-13,y+12),(x+12,y+12),(x,y+2)):orb(xx,yy,6)
 elif glyph=='nuclear':
  for xx,yy in ((x-11,y-8),(x+3,y-15),(x+14,y-2),(x+8,y+13),(x-9,y+12),(x,y)):orb(xx,yy,5)
 elif glyph=='missing':
  draw.ellipse((x-13,y-14,x+13,y+12),outline=color,width=2)
  draw.line((x-6,y-1,x+6,y-1),fill=dark,width=3)
  draw.line((x,y+14,x,y+22),fill=color,width=2)
  for dx,dy in ((-13,-14),(13,-14)):
   draw.ellipse((x+dx-6,y+dy-6,x+dx+6,y+dy+6),outline=color,width=2)
 elif glyph=='ring':
  draw.ellipse((x-16,y-16,x+16,y+16),outline=color,width=2)
  for xx,yy in ((x,y-10),(x+9,y),(x,y+10),(x-9,y)):orb(xx,yy,3)
 elif glyph=='mito':
  draw.rounded_rectangle((x-19,y-12,x+19,y+12),radius=12,fill=light,outline=dark,width=2)
  draw.line((x-12,y-3,x-5,y+4,x+3,y-4,x+10,y+3),fill=dark,width=2)
  draw.arc((x-17,y-10,x+8,y+2),180,300,fill='#fff',width=2)
 elif glyph=='dots':
  draw.ellipse((x-16,y-16,x+16,y+16),outline=color,width=2)
  for xx,yy,r in ((x-8,y-6,3),(x+7,y-5,2),(x,y+7,3),(x+9,y+8,2)):orb(xx,yy,r)
 else:
  points=((x,y+18,x,y),(x,y+4,x-12,y-8),(x,y+4,x+12,y-8))
  for line in points:draw.line(line,fill=dark,width=8)
  for line in points:draw.line(line,fill=color,width=6)
  draw.line((x-2,y+13,x-2,y-1),fill=light,width=2)
  for xx,yy in ((x,y-11),(x-12,y-11),(x+12,y-11)):
   orb(xx,yy,7 if glyph=='cluster' else 5)
def card(mode,selected=False,neutral=False,locations=False):
 im=Image.new('RGBA',(390,844),'#faf7f1');d=ImageDraw.Draw(im)
 d.rounded_rectangle((22,20,48,46),radius=9,fill='#e4ecf6');d.text((29,23),'✳',font=F(15),fill='#6686b3')
 d.text((57,29),'VISIT EXPLAINED  /  CELL LAB',font=F(10,True),fill='#5d7090');d.line((22,66,368,66),fill='#e9e5e0')
 d.rounded_rectangle((22,84,368,132),radius=17,fill='#eeeae6')
 if mode=='a':d.rounded_rectangle((26,88,189,128),radius=13,fill='#fff')
 else:d.rounded_rectangle((193,88,364,128),radius=13,fill='#fff')
 d.text((37,102),'A  Interactive SVG',font=F(11,True),fill='#4f78a7' if mode=='a' else '#8a817b')
 d.text((203,102),'B  Illustration + Overlay',font=F(10,True),fill='#4f78a7' if mode=='b' else '#8a817b')
 d.text((25,157),'BIOMARKER VISUAL STUDY' if locations else 'YOUR BIOPSY, VISUALIZED',font=F(10,True),fill='#8e79b8')
 d.text((25,179),'Your T cell (simplified)',font=F(23,True),fill='#4a3b35')
 d.text((25,213),'Four illustrated markers; no patient results.' if locations else 'Tap a marker to explore your visit.',font=F(12),fill='#8b817b')
 aura=Image.new('RGBA',im.size);ImageDraw.Draw(aura).ellipse((40,258,350,591),fill=(221,225,247,85));im.alpha_composite(aura.filter(ImageFilter.GaussianBlur(28)))
 cell=Image.open(root/f'cell-{mode}.png').convert('RGBA').resize((390,390),Image.Resampling.LANCZOS);im.alpha_composite(cell,(0,225));d=ImageDraw.Draw(im)
 markers=other if locations else normal
 if not neutral:
  for name,color,pale,lp,rp,glyph in markers:
   x,y=round(rp[0]*3.9),225+round(rp[1]*3.9)
   if glyph in ('ring','dots','mito','cyto','nuclear'):
    endx,endy=round(lp[0]*3.9)-27,225+round(lp[1]*3.9)-17
    d.line((x+8,y+8,(x+endx)//2,y+25,endx,endy),fill=color,width=1)
   receptor(im,d,x,y,color,glyph)
  for name,color,pale,lp,rp,glyph in markers:label(im,d,round(lp[0]*3.9),225+round(lp[1]*3.9),name,color,pale)
 d.text((113 if not neutral else 86,634),'Tap a marker to explore' if not neutral else 'A quiet moment to see the cell itself',font=F(12),fill='#978d8c')
 d.rounded_rectangle((25,665,127,691),radius=13,fill='#e9f0f8' if not locations else '#fff9',outline='#d7e3f1',width=1)
 d.rounded_rectangle((134,665,246,691),radius=13,fill='#e9f0f8' if locations else '#fff9',outline='#d7e3f1',width=1)
 d.text((34,672),'Visit markers',font=F(10,True),fill='#536f9d' if not locations else '#7d797a')
 d.text((143,672),'Marker study',font=F(10,True),fill='#536f9d' if locations else '#7d797a')
 d.rounded_rectangle((25,711,61,732),radius=11,fill='#7897bf' if neutral else '#e2dedb')
 d.ellipse((43 if neutral else 28,714,58 if neutral else 43,729),fill='#fff');d.text((72,714),'View cell without markers',font=F(12),fill='#746a66')
 if selected:
  shadow=Image.new('RGBA',im.size);ImageDraw.Draw(shadow).rounded_rectangle((0,530,390,880),radius=29,fill=(75,64,77,40));im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
  d=ImageDraw.Draw(im);d.rounded_rectangle((0,530,390,880),radius=29,fill='#fffdfa');d.rounded_rectangle((178,540,213,544),radius=3,fill='#dedbd8')
  d.text((25,568),'MARKER DETAIL',font=F(9,True),fill='#df857d');d.text((25,587),'CD30',font=F(24,True),fill='#4a3b35')
  d.rounded_rectangle((106,593,173,616),radius=11,fill='#fff0e9');d.text((117,599),'Present',font=F(10,True),fill='#df857d');d.text((350,574),'×',font=F(24),fill='#706661')
  d.text((25,634),'What it normally does',font=F(12,True),fill='#4a3b35')
  d.text((25,655),'CD30 is a signaling protein found on some',font=F(11),fill='#746a66');d.text((25,672),'activated immune cells.',font=F(11),fill='#746a66')
  d.text((25,703),'Why doctors look at it',font=F(12,True),fill='#4a3b35')
  d.text((25,724),'Some lymphomas express CD30. The result may',font=F(11),fill='#746a66');d.text((25,741),'help describe the cells and guide discussion.',font=F(11),fill='#746a66')
  d.rounded_rectangle((25,770,365,851),radius=12,fill='#f6f3f9');d.rounded_rectangle((25,770,28,851),radius=1,fill='#df857d');d.text((40,785),'WHAT YOUR DOCTOR SAID',font=F(9,True),fill='#df857d');d.text((40,809),'“Your biopsy showed CD30-positive cells.”',font=F(11),fill='#564d52')
 suffix='-locations' if locations else '-selected' if selected else '-neutral' if neutral else ''
 im.convert('RGB').save(root/f'prototype-{mode}{suffix}.png')
for mode in ('a','b'):
 card(mode);card(mode,True);card(mode,neutral=True);card(mode,locations=True)
