from PIL import Image, ImageDraw, ImageFont
import textwrap, math

W,H=1024,1024
PAPER=(247,243,232); INK=(17,17,17); NAVY=(15,42,68); GOLD=(212,175,55)
RED=(178,34,34); TEAL=(0,120,110)
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def f(p,s): return ImageFont.truetype(p,s)
img=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(img)

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def text_block(x,y,text,font,maxw,color=INK,leading=None):
    ls=wrap(d,text,font,maxw); lh=leading or int(font.size*1.25)
    for ln in ls:
        d.text((x,y),ln,font=font,fill=color); y+=lh
    return y

def burst(cx,cy,r,col):
    pts=[]
    for i in range(16):
        a=i*math.pi/8; rr=r if i%2==0 else r*0.45
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d.polygon(pts, fill=col)

# ---------- masthead ----------
d.rectangle([0,0,W,122], fill=NAVY)
d.text((24,14),"WORLD NEWS",font=f(FS,58),fill=(255,255,255))
d.text((24,82),"SATURDAY  21  NOVEMBER  2026",font=f(FB,30),fill=GOLD)
d.text((700,30),"THE DAY",font=f(FB,26),fill=(255,255,255))
d.text((700,62),"IN ONE IMAGE",font=f(FB,26),fill=(255,255,255))
d.line([0,122,W,122],fill=GOLD,width=4)

# ---------- lead: Iran / Bahrain ----------
lx,ly,lw,lh=16,134,992,250
d.rectangle([lx,ly,lx+lw,ly+lh],outline=INK,width=2,fill=(255,255,255))
# illustration left 470x258
ix,iy,iw,ih=lx,ly,470,258
d.rectangle([ix,iy,ix+iw,iy+ih],fill=(10,25,50))
# sea
d.rectangle([ix,iy+180,ix+iw,iy+ih],fill=(20,60,90))
# skyline
for bx,bw,bh in [(10,40,90),(60,30,120),(100,50,80),(160,35,140),(210,45,100),(270,30,130),(320,40,85),(380,35,115)]:
    d.rectangle([ix+bx,iy+180-bh,ix+bx+bw,iy+180],fill=(5,15,30))
# explosion
burst(ix+330,iy+90,55,(255,140,0)); burst(ix+330,iy+90,32,(255,220,80))
# missile arcs
d.arc([ix+40,iy+10,ix+300,iy+130],start=200,end=340,fill=(255,255,255),width=4)
d.arc([ix+120,iy+5,ix+420,iy+110],start=200,end=330,fill=(255,220,80),width=4)
d.ellipse([ix+295,iy+95,ix+303,iy+103],fill=(255,255,255))
d.text((ix+16,iy+196),"BAHRAIN  •  GULF",font=f(FB,18),fill=(255,255,255))
# lead text right
tx=lx+490
d.text((tx,ly+14),"LEAD STORY — MIDDLE EAST",font=f(FB,17),fill=RED)
y=text_block(tx,ly+42,"Iran strikes Bahrain",f(FS,34),480)
y=text_block(tx,y+6,"Iran says it hit two US bases; Bahrain reports a fire at an industrial site — no injuries.",f(FR,19),480,leading=24)
d.text((tx,ly+lh-36),"Air defences intercepted other attacks.",font=f(FB,17),fill=(60,60,60))

# ---------- panels ----------
def panel(x,y,w,h,kicker,kcolor,headline,body,drawfn):
    d.rectangle([x,y,x+w,y+h],outline=INK,width=2,fill=(255,255,255))
    drawfn(x,y,w,80)
    d.text((x+14,y+88),kicker,font=f(FB,15),fill=kcolor)
    yy=text_block(x+14,y+108,headline,f(FS,22),w-28,leading=25)
    text_block(x+14,yy+3,body,f(FR,16),w-28,leading=19)

def p_mexico(x,y,w,hh):
    d.rectangle([x,y,x+w,y+hh],fill=(210,150,60))
    d.polygon([(x,y+hh),(x+120,y+30),(x+260,y+hh)],fill=(150,90,40))
    d.polygon([(x+180,y+hh),(x+320,y+10),(x+480,y+hh)],fill=(170,105,45))
    d.rectangle([x,y+70,x+w,y+hh],fill=(120,80,40))
    # flashing lights
    d.ellipse([x+60,y+30,x+90,y+60],fill=(220,30,30)); d.ellipse([x+100,y+30,x+130,y+60],fill=(30,80,220))
    d.text((x+150,y+28),"SINALOA",font=f(FB,20),fill=(255,255,255))
def p_ukraine(x,y,w,hh):
    d.rectangle([x,y,x+w,y+hh],fill=(70,90,120))
    for bx,bw,bh in [(10,50,50),(70,40,70),(120,60,45),(200,45,75),(270,50,55),(340,40,65),(400,55,50)]:
        d.rectangle([x+bx,y+hh-bh,x+bx+bw,y+hh],fill=(35,45,60))
    burst(x+330,y+40,38,(255,140,0)); burst(x+330,y+40,20,(255,220,80))
    d.arc([x+40,y+5,x+280,y+75],start=200,end=340,fill=(255,255,255),width=3)
    d.rectangle([x+20,y+12,x+70,y+30],fill=(255,255,255)); d.rectangle([x+20,y+30,x+70,y+48],fill=(220,40,40))
    d.text((x+80,y+16),"POLAND",font=f(FB,16),fill=(255,255,255))
def p_cop(x,y,w,hh):
    d.rectangle([x,y,x+w,y+hh],fill=(0,110,90))
    d.ellipse([x+330,y+2,x+440,y+78],fill=(20,160,120))
    d.ellipse([x+350,y+14,x+420,y+40],fill=(120,220,160)); d.ellipse([x+360,y+44,x+410,y+66],fill=(40,140,100))
    d.rectangle([x+30,y+55,x+150,y+hh],fill=(255,255,255))
    d.polygon([(x+30,y+55),(x+90,y+25),(x+150,y+55)],fill=(200,220,210))
    d.text((x+170,y+28),"ANTALYA",font=f(FB,20),fill=(255,255,255))
    d.text((x+170,y+54),"TURKEY",font=f(FB,20),fill=(255,255,255))
def p_markets(x,y,w,hh):
    d.rectangle([x,y,x+w,y+hh],fill=(255,255,255))
    d.line([(x+20,y+15),(x+130,y+30),(x+220,y+28),(x+320,y+55),(x+420,y+72)],fill=RED,width=6)
    d.polygon([(x+420,y+72),(x+398,y+58),(x+435,y+58)],fill=RED)
    for bx,bh in [(40,25),(110,35),(180,20),(250,45)]:
        d.rectangle([x+bx,y+hh-bh,x+bx+45,y+hh],fill=(200,200,200))
def p_dengue(x,y,w,hh):
    d.rectangle([x,y,x+w,y+hh],fill=(200,240,200))
    d.ellipse([x+330,y+8,x+450,y+78],fill=(0,140,80))
    d.text((x+345,y+22),"69%",font=f(FB,34),fill=(255,255,255))
    d.ellipse([x+60,y+35,x+110,y+55],fill=(40,40,40))
    d.line([(x+60,y+45),(x+20,y+25)],fill=(40,40,40),width=3); d.line([(x+60,y+45),(x+20,y+65)],fill=(40,40,40),width=3)
    d.ellipse([x+95,y+18,x+135,y+38],fill=(255,255,255))
    d.text((x+150,y+28),"BRAZIL",font=f(FB,20),fill=(0,100,60))

gx,gy=16,396; pw=488; ph=182; gap=12
panel(gx,gy,pw,ph,"MEXICO — CRIME",RED,"‘El Chapo Isidro’ captured","Mexico seizes FBI most-wanted boss Fausto Isidro Meza Flores in Sinaloa; at least 11 dead.",p_mexico)
panel(gx+pw+gap,gy,pw,ph,"UKRAINE — WAR",RED,"Missile hits Zelenskyy’s hometown","A Russian missile strikes Kryvyi Rih, killing 2 and wounding dozens; missiles also cross into Poland.",p_ukraine)
panel(gx,gy+ph+gap,pw,ph,"CLIMATE — COP31",TEAL,"Climate talks run past deadline","In Antalya, talks run into overtime over fossil fuels, close to a final deal, the summit president says.",p_cop)
panel(gx+pw+gap,gy+ph+gap,pw,ph,"MARKETS — ECONOMY",RED,"AI sell-off turns into a correction","The Nasdaq suffers its worst week since March 2020 and erases its 2026 gains as chip shares plunge.",p_markets)
panel(gx,gy+2*(ph+gap),pw,ph,"HEALTH — SCIENCE",TEAL,"Mosquitoes that beat dengue","Specially bred mosquitoes cut dengue in children by about 69% in a major Brazil study.",p_dengue)
# also panel
x=gx+pw+gap; y=gy+2*(ph+gap); w=pw; h=ph
d.rectangle([x,y,x+w,y+h],outline=INK,width=2,fill=(15,42,68))
d.text((x+14,y+12),"ALSO ON SATURDAY",font=f(FB,17),fill=GOLD)
items=[
 ("•  ","Russian cargo ship Sparta II burns in the Gulf of Finland after a drone strike."),
 ("•  ","GTA VI sets a record: $3.79bn in first-day sales, Rockstar says."),
 ("•  ","A 6.9 earthquake shakes the Peruvian Andes."),
]
yy=y+44
for b,t in items:
    d.text((x+14,yy),b,font=f(FB,18),fill=(255,255,255))
    yy=text_block(x+34,yy,t,f(FR,17),w-48,color=(255,255,255),leading=21)
    yy+=8

# footer
d.text((16,980),"Events of 21 November 2026, as reported that day  •  Reuters / AP / CNN",font=f(FR,14),fill=(90,90,90))
img.save("/home/hatch/workspace/makefun/entry-news-image/entry.png",optimize=True)
print("saved", img.size)
import os; print(os.path.getsize("/home/hatch/workspace/makefun/entry-news-image/entry.png"))
