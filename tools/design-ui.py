"""Editable vector artboards for the 35 Zvezda-57 interface elements.

Run from the repository root: python3 tools/design-ui.py
PNG export and the browser gallery are built by export-ui.mjs.
"""
from pathlib import Path
import base64
import json
import math
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'UI'
OUT.mkdir(parents=True, exist_ok=True)
P = dict(navy='#172C3A', green='#244339', amber='#CB9E69', paper='#F5EFE0',
         red='#B64F49', mint='#3A998A', ink='#25353A', muted='#B8B8A9', brass='#82704F')
ART = ROOT / 'UI/Reference/office.jpg'
ART_URI = 'data:image/jpeg;base64,' + base64.b64encode(ART.read_bytes()).decode() if ART.exists() else ''
FONT = 'Arial, sans-serif'
SERIF = 'Georgia, serif'
MONO = 'Courier New, monospace'
names = ['MENU','BACK','HIGHLIGHT','CONTEXT','VIEW','QUEUE','YURA_CALL','YURA_STATUS',
         'CASE','DOCUMENT','REFERENCE_TABS','EVIDENCE','STAMP','SUBMIT','DIAL','PHONE_REPORT',
         'INCOMING','DIALOGUE','MAP','SECTOR_ALERT','INCIDENT','CREW','COUNTDOWN','ROUTE',
         'CITY_GAUGES','RESERVES','UPGRADES','APPROVE','SHIFT_REPORT','ENDING','PAUSE',
         'SETTINGS','SUBTITLES','BUTTON_STATES','CREDITS']

def r(x,y,w,h,fill,stroke='none',sw=1,rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def l(x1,y1,x2,y2,c=P['brass'],sw=1,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" {extra}/>'
def circle(x,y,rad,fill,stroke='none',sw=1,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def text(x,y,s,size=24,c=None,weight=400,font=FONT,anchor='start',spacing=0,extra=''):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{c or P["paper"]}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}" {extra}>{escape(str(s))}</text>'
def lines(x,y,ss,size=24,c=None,leading=36,**kw):
    return ''.join(text(x,y+i*leading,s,size,c,**kw) for i,s in enumerate(ss))
def group(s,x=0,y=0,scale=1,extra=''):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{s}</g>'
def screw(x,y):
    return circle(x,y,4,'#A69B7B')+l(x-2,y+2,x+2,y-2,'#35434A',1.3)
def metal(x,y,w,h):
    return r(x+4,y+6,w,h,'#080F13',rx=5)+r(x,y,w,h,P['navy'],'#6B7269',1.5,5)+r(x+8,y+8,w-16,h-16,'none','#3B4F54',1,2)+''.join(screw(a,b) for a,b in [(x+17,y+17),(x+w-17,y+17),(x+17,y+h-17),(x+w-17,y+h-17)])
def paper(x,y,w,h):
    return r(x+7,y+9,w,h,'#050B0E',extra='opacity=".3"')+r(x,y,w,h,P['paper'],'#C4B693',1)+r(x+9,y+9,w-18,h-18,'url(#papergrain)',extra='opacity=".2"')
def icon(name,x,y,size=32,c=None):
    c=c or P['amber']
    shapes={
      'arrow':'<path d="M21 6 9 16l12 10M9 16h24"/>',
      'folder':'<path d="M3 10h12l4 5h18v21H3zM3 10V6h12l4 4"/>',
      'check':'<path d="m5 20 9 9L35 7"/>',
      'cross':'<path d="m9 9 22 22M31 9 9 31"/>',
      'clock':'<circle cx="20" cy="20" r="16"/><path d="M20 9v12l8 5"/>',
      'phone':'<path d="M10 4 4 8c-3 12 16 31 28 28l4-6-9-7-5 5c-6-2-10-6-12-12l5-5z"/>',
      'person':'<circle cx="20" cy="11" r="7"/><path d="M6 36v-7c0-12 28-12 28 0v7z"/>',
      'flame':'<path d="M21 2c0 12-11 14-6 23-7-2-6-8-6-8C-3 38 36 45 34 24c-1-6-7-11-7-11s2 13-4 15c5-11-6-14-2-26Z"/>',
      'shield':'<path d="m20 3 15 6v12c0 9-15 16-15 16S5 30 5 21V9zM14 20l4 5 10-12"/>',
      'wrench':'<path d="M24 3c-9-1-12 7-8 13L3 29l7 7 13-13c10 3 17-6 12-14l-7 8-6-6z"/>',
      'radio':'<path d="M6 13h28v22H6zM11 13 29 2M11 19h18M11 25h8M25 29h4"/>',
      'bolt':'<path d="M23 2 7 23h12l-3 15 17-23H21z"/>',
      'mouse':'<rect x="9" y="3" width="22" height="34" rx="11"/><path d="M20 3v14M9 17h22"/>',
      'pen':'<path d="m5 28 4 8 8-4L34 9l-7-6L5 28zM5 28l12 4M23 9l7 6"/>',
      'pause':'<path d="M13 7v26M27 7v26"/>',
      'sound':'<path d="M5 16h7L22 7v26L12 24H5zM28 13c7 4 7 10 0 14M32 7c14 9 14 17 0 26"/>',
      'star':'<path d="m20 2 5 12 13 1-10 9 3 13-11-7-11 7 3-13L2 15l13-1z"/>',
      'train':'<rect x="8" y="4" width="24" height="27" rx="5"/><path d="M8 17h24M20 4v13M13 31l-5 7M27 31l5 7M12 36h16"/><circle cx="14" cy="25" r="2"/><circle cx="26" cy="25" r="2"/>',
      'lock':'<rect x="7" y="17" width="26" height="20" rx="2"/><path d="M12 17V9c0-10 16-10 16 0v8M20 24v6"/>',
    }
    return f'<g transform="translate({x} {y}) scale({size/40})" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{shapes.get(name,shapes["star"])}</g>'
def lamp(x,y,c=None,rad=8):
    c=c or P['mint']
    return circle(x,y,rad+4,'#111D21','#7B735D',1)+circle(x,y,rad,c)+circle(x-2,y-2,max(2,rad/3),'#FFF3CE',extra='opacity=".65"')
def button(x,y,w,label,state='normal',kind='paper',h=70):
    disabled=state=='disabled'; selected=state=='selected'
    fill=P['paper'] if kind=='paper' else '#263D45'
    ink=P['ink'] if kind=='paper' else P['paper']
    if disabled: fill='#B7B3A6' if kind=='paper' else '#28363B'; ink='#686E69'
    if state=='pressed': fill='#D2C6AC' if kind=='paper' else '#0E202A'
    edge=P['amber'] if state in ['hover','pressed'] else P['mint'] if selected else '#8C846E'
    s=r(x,y+4,w,h,'#080F13',rx=3)+r(x,y,w,h,fill,edge,2 if state in ['hover','selected'] else 1,3)
    s+=l(x+8,y+7,x+w-8,y+7,'#FFFFFF' if kind=='paper' else '#63706B',extra='opacity=".25"')
    if selected: s+=r(x+12,y+12,4,h-24,P['mint'])
    return s+text(x+w/2,y+h/2+9,label,25,ink,600,anchor='middle',spacing=1)
def back(x=64,y=946,dark=True):
    return button(x,y,188,'НАЗАД',kind='metal' if dark else 'paper',h=64)+icon('arrow',x+17,y+17,28,P['paper'] if dark else P['ink'])
def tag(x,y,label,c=None,w=None):
    w=w or len(label)*13+48
    return r(x,y,w,38,P['navy'],c or P['brass'],1,2)+text(x+16,y+26,label,19,c or P['paper'],600,spacing=1)
def eyebrow(x,y,s,c=None): return text(x,y,s,18,c or P['amber'],600,spacing=3)
def title(x,y,s,size=44,c=None): return text(x,y,s,size,c or P['paper'],400,SERIF)
def separator(x,y,w,c=None): return l(x,y,x+w,y,c or '#A29578')
def office(shade=.55):
    return (f'<image href="{ART_URI}" x="0" y="-100" width="1920" height="1280" preserveAspectRatio="xMidYMid slice"/>' if ART_URI else r(0,0,1920,1080,P['green']))+r(0,0,1920,1080,'#09141B',extra=f'opacity="{shade}"')
def desk():
    return r(0,0,1920,1080,'#10252C')+r(40,40,1840,1000,P['green'],'#806C4D',3,8)+r(58,58,1804,964,'url(#felt)',extra='opacity=".45"')
def header(zone='ИНСПЕКТОРСКИЙ СТОЛ'):
    return tag(64,52,'ЗВЕЗДА-57',P['amber'],190)+text(282,79,zone,19,P['paper'],spacing=2)+tag(1474,52,'СМЕНА 02',w=186)+button(1708,48,148,'ПАУЗА',kind='metal',h=50)
def base(zone='ИНСПЕКТОРСКИЙ СТОЛ',photo=True):
    return (office(.45) if photo else desk())+header(zone)
def panel_head(x,y,w,kicker,heading,on_paper=False):
    return eyebrow(x,y,kicker,P['brass'] if on_paper else None)+title(x,y+57,heading,c=P['ink'] if on_paper else None)+separator(x,y+84,w)
def note(x,y,ss,w=540,caption='СЛУЖЕБНАЯ ЗАПИСКА'):
    h=100+len(ss)*35
    return paper(x,y,w,h)+eyebrow(x+28,y+35,caption,P['brass'])+lines(x+28,y+83,ss,23,P['ink'],leading=35)

def folder(x,y,w=260,h=140,num='01',state='ОЖИДАЕТ'):
    return r(x,y-18,w*.52,24,'#A39770',rx=3)+r(x,y,w,h,'#CCBC8C','#81724F',1,3)+text(x+24,y+52,f'№ {num}',36,P['ink'],font=SERIF)+text(x+24,y+h-24,state,18,P['ink'],spacing=2)
def case_tag(x=670,y=936):
    return paper(x,y,580,75)+icon('folder',x+20,y+19,32,P['brass'])+text(x+72,y+34,'ДЕЛО № 2.3 / МОРОЗОВ',24,P['ink'],600)+text(x+72,y+59,'Проверка документов',18,'#6B6A59')+lamp(x+545,y+37)
def stamp(x,y,label='ДОПУСТИТЬ',c=None,angle=-8):
    c=c or P['green']
    return f'<g transform="rotate({angle} {x+130} {y+42})" opacity=".88">'+r(x,y,260,84,'none',c,4)+r(x+7,y+7,246,70,'none',c,1)+text(x+130,y+52,label,25,c,600,anchor='middle',spacing=2)+'</g>'
def document(x,y,w=650,h=800):
    s=paper(x,y,w,h)+eyebrow(x+40,y+45,'МИНИСТЕРСТВО СРЕДНЕГО МАШИНОСТРОЕНИЯ',P['brass'])
    s+=text(x+40,y+98,'Командировочное',37,P['ink'],font=SERIF)+text(x+40,y+143,'предписание',37,P['ink'],font=SERIF)
    s+=separator(x+40,y+175,w-80)
    s+=r(x+w-184,y+204,140,170,'#BBB49F','#92886D')+icon('person',x+w-150,y+238,72,'#655F51')+text(x+w-114,y+356,'ФОТО 3 × 4',13,'#655F51',anchor='middle')
    s+=eyebrow(x+40,y+224,'ФАМИЛИЯ И ИНИЦИАЛЫ',P['brass'])+text(x+40,y+270,'Л. Д. Морозов',30,P['ink'],font=SERIF)
    fields=[('НАПРАВЛЕН ИЗ','НИИ-42 / Обнинск'),('МЕСТО НАЗНАЧЕНИЯ','Лаборатория № 3'),('ОСНОВАНИЕ','Приказ № 117/57'),('СРОК КОМАНДИРОВКИ','14 — 18 октября 1957 г.')]
    for i,(a,b) in enumerate(fields):
        yy=y+326+i*88
        s+=eyebrow(x+40,yy,a,P['brass'])+text(x+40,yy+37,b,25,P['ink'])
    s+=separator(x+40,y+h-130,w-80)+text(x+40,y+h-95,'Подпись ответственного',18,'#6F6A58')+l(x+290,y+h-92,x+w-40,y+h-92,'#8A8065')
    return s
def tabs(x,y,active=0,vertical=True):
    s=''
    for i,label in enumerate(['НИИ','ПЕЧАТИ','ГРУЗЫ','ТЕЛЕФОНЫ']):
        xx=x if vertical else x+i*195; yy=y+i*106 if vertical else y
        fill=P['amber'] if i==active else '#BCB89F'
        s+=r(xx-10 if i==active else xx,yy,182 if vertical else 180,84,fill,'#6D705D',1,2)
        s+=text(xx+80,yy+49,label,22,P['ink'],600,anchor='middle',spacing=1)
    return s
def phone(x,y,scale=1,cream=False):
    s=''
    body='#C9C0A4' if cream else '#151F22'; edge='#8C8367' if cream else '#5A5D55'
    s+=f'<path d="M45 205Q60 115 145 110h180q90 5 105 95l35 110H10Z" fill="{body}" stroke="{edge}" stroke-width="4"/>'
    s+=r(4,304,462,43,body,edge,3,15)
    s+=f'<path d="M65 100Q73 25 155 35h170q83-8 88 65l-65 20-32-35H164l-32 35Z" fill="{body}" stroke="{edge}" stroke-width="4"/>'
    s+=circle(235,217,109,'#8E896F','#C7BC99',4)+circle(235,217,68,body,'#5B604F',2)+circle(235,217,33,'#D6C9A6','#7E765D',2)
    s+=text(235,222,'1957',15,P['ink'],anchor='middle',font=SERIF)
    for i,n in enumerate('1234567890'):
        a=math.radians(-65-i*28)
        xx=235+87*math.cos(a); yy=217+87*math.sin(a)
        s+=circle(xx,yy,16,'#16232B','#D4C8A8',2)+text(xx,yy+7,n,19,P['paper'],anchor='middle')
    s+=f'<path d="M414 80c100 5 40 100 90 150s-35 40 0 80" fill="none" stroke="{body}" stroke-width="22" stroke-dasharray="5 3"/>'
    return group(s,x,y,scale)

sectors=[[(90,80),(450,35),(480,245),(335,325),(75,275)],[(480,40),(790,70),(875,270),(520,280)],[(815,70),(1110,100),(1190,300),(900,285)],[(70,300),(330,350),(455,525),(105,575),(35,430)],[(370,350),(535,310),(855,320),(785,570),(485,550)],[(890,320),(1200,335),(1130,570),(830,590)]]
centers=[(260,180),(650,175),(1005,205),(230,425),(630,440),(1010,450)]
sector_names=['ВОКЗАЛ','ЖИЛОЙ РАЙОН','ТОКАМАК','ЭНЕРГОБЛОК','СКЛАД','РАДИОУЗЕЛ']
def map_board(x=96,y=172,scale=1,selected=3,route=False):
    s=metal(0,0,1260,660)+r(24,24,1212,612,'#18382F','#6D7763',1,2)
    for xx in range(65,1210,55): s+=l(xx,30,xx,630,'#365044',.6)
    for yy in range(48,640,48): s+=l(28,yy,1225,yy,'#365044',.6)
    for i,pts in enumerate(sectors):
        s+=f'<polygon points="'+ ' '.join(f'{a},{b}' for a,b in pts)+f'" fill="{P["red"] if i==selected else P["green"]}" fill-opacity="{.25 if i==selected else .6}" stroke="{P["amber"] if i==selected else "#ABAE8D"}" stroke-width="{3 if i==selected else 1.5}"/>'
        xx,yy=centers[i]
        # The street/building marks are subordinate to numbers and statuses.
        for j in range(5):
            s+=r(xx-100+j*41,yy+25+(j%2)*8,25,12,'#5B6F58',rx=1)
        s+=text(xx,yy-28,f'0{i+1}',46,P['paper'],font=SERIF,anchor='middle')
        s+=text(xx,yy+6,sector_names[i],18,P['paper'],600,anchor='middle',spacing=1)
        s+=lamp(xx,yy+70,P['red'] if i==selected else P['mint'],7)
    s+=text(50,620,'ЗВЕЗДА-57  /  ОПЕРАТИВНАЯ СХЕМА',16,P['amber'],spacing=2)
    if route:
        s+='<path d="M630 550 540 500 440 485 230 455" fill="none" stroke="#CB9E69" stroke-width="4" stroke-dasharray="12 10"/>'+icon('flame',390,452,32,P['paper'])+tag(440,386,'В ПУТИ',P['amber'],160)
    return group(s,x,y,scale)
def switchboard(x=96,y=850,w=1260):
    s=metal(x,y,w,150)
    for i,(label,c) in enumerate([('ОПЕРГРУППА',P['amber']),('ВОХР',P['mint']),('ПОЖАРНЫЕ',P['red']),('РЕМОНТ','#A7AB8E')]):
        xx=x+64+i*(w-100)/4
        s+=r(xx,y+22,230,34,'#B4A17A','#5D533F',1,2)+text(xx+115,y+46,label,18,P['ink'],600,anchor='middle',spacing=1)
        s+=circle(xx+26,y+101,19,'#0A171C','#99856A',5)+circle(xx+26,y+101,7,c)+lamp(xx+73,y+101,c,6)+text(xx+96,y+108,'СВОБОДЕН',16,P['paper'],spacing=1)
    return s
def incident(x=1400,y=172,w=440):
    s=paper(x,y,w,640)+eyebrow(x+30,y+40,'КАРТОЧКА ПРОИСШЕСТВИЯ',P['brass'])
    s+=title(x+30,y+102,'Энергоблок',36,P['ink'])+text(x+30,y+143,'СЕКТОР 04',21,P['ink'],600,spacing=2)+separator(x+30,y+172,w-60)
    s+=icon('bolt',x+30,y+206,42,P['red'])+text(x+91,y+234,'СБОЙ ПИТАНИЯ',25,P['ink'],600)
    s+=lines(x+30,y+290,['На подстанции пропало','напряжение. Причина','пока не установлена.'],24,P['ink'],leading=35)
    s+=text(x+30,y+432,'ПРИОРИТЕТ',17,P['brass'],600,spacing=2)+text(x+30,y+469,'!  ВЫСОКИЙ',25,P['red'],600)
    s+=r(x+30,y+502,w-60,95,P['navy'],rx=3)+text(x+48,y+531,'ДО УХУДШЕНИЯ',17,P['paper'],spacing=2)+text(x+w-50,y+576,'00:38',42,P['amber'],font=MONO,anchor='end')
    return s
def gauge(x,y,label,value,c=None,scale=1):
    c=c or P['mint']
    s=metal(0,0,420,335)+r(28,28,364,230,P['paper'],'#8F856B',2,12)
    s+='<path d="M66 210A145 145 0 0 1 354 210" fill="none" stroke="#928D76" stroke-width="2"/>'
    for i in range(11):
        a=math.pi+(i/10)*math.pi
        xa=210+143*math.cos(a); ya=210+143*math.sin(a)
        xb=210+(126 if i%5 else 118)*math.cos(a); yb=210+(126 if i%5 else 118)*math.sin(a)
        s+=l(xa,ya,xb,yb,P['ink'],2)
    a=math.pi+value/100*math.pi
    s+=l(210,210,210+110*math.cos(a),210+110*math.sin(a),P['red'],4)+circle(210,210,9,P['ink'])
    s+=text(70,235,'0',16,P['ink'])+text(350,235,'100',16,P['ink'],anchor='end')+text(210,172,value,34,P['ink'],font=SERIF,anchor='middle')
    s+=text(210,298,label,22,P['paper'],600,anchor='middle',spacing=2)+lamp(370,290,c,6)
    return group(s,x,y,scale)

upgrades=[('Оперативная группа','Второй канал оперативников',3,'person'),('Пожарный расчёт','Второй пожарный экипаж',3,'flame'),('Ремонтная бригада','Второй ремонтный экипаж',3,'wrench'),('Быстрые выезды','Сокращает время в пути',2,'train'),('Усиленная радиосвязь','Улучшает координацию',2,'radio'),('Пожарное оснащение','Ускоряет тушение',1,'shield')]
def upgrade_card(x,y,i,state='normal'):
    name,effect,cost,ico=upgrades[i]
    fill='#E6E7D9' if state=='selected' else '#EAE4D2' if state!='disabled' else '#E0DDD1'
    s=r(x,y,700,165,fill,P['mint'] if state=='selected' else '#A9A38E',2 if state=='selected' else 1,2)
    s+=r(x+20,y+24,86,86,P['navy'],rx=3)+icon(ico,x+39,y+43,48,P['amber'])
    s+=text(x+128,y+51,name,28,P['ink'],600)+text(x+128,y+89,effect,23,'#646958')
    s+=circle(x+650,y+49,25,P['navy'])+text(x+650,y+57,cost,25,P['paper'],600,anchor='middle')
    if state=='selected': s+=icon('check',x+128,y+113,25,P['mint'])+text(x+166,y+137,'ВЫБРАНО',18,P['green'],600,spacing=1)
    elif state=='bought': s+=text(x+128,y+137,'✓  ВЫДЕЛЕНО',18,P['green'],600,spacing=2)
    elif state=='disabled': s+=icon('lock',x+128,y+113,24,'#6E7366')+text(x+164,y+137,'Недостаточно резервов',18,'#6E7366')
    else: s+=text(x+128,y+137,'Нажмите, чтобы выбрать',18,'#68705E')
    return s
def reserves(approved=False):
    s=office(.7)+paper(155,75,1610,930)
    s+=eyebrow(205,125,'ВЕДОМОСТЬ № 02 / 16 ОКТЯБРЯ 1957',P['brass'])+title(205,190,'Распределение резервов',48,P['ink'])
    s+=text(1705,125,'ДОСТУПНО',17,P['brass'],600,anchor='end',spacing=2)+text(1705,190,'5 очков',46,P['ink'],font=SERIF,anchor='end')
    s+=separator(205,224,1500)
    for i in range(6): s+=upgrade_card(205+(i%2)*770,260+(i//2)*190,i,['selected','normal','disabled','selected','bought','normal'][i])
    s+=text(205,890,'Будет потрачено: 5  /  Остаток: 0',23,P['ink'])+text(205,931,'Остаток переносится на следующую смену.',19,'#69715F')
    s+=button(1160,862,545,'УТВЕРДИТЬ РЕЗЕРВЫ',state='selected',kind='metal',h=76)
    return s

def ending_art(kind=0):
    # Deliberately vector-native concept art, independent of game text.
    skies=['#203D46','#26343E','#0B171E']; light=['#E4B37B','#B9B8AE','#B64F49'][kind]
    s=r(0,0,1920,1080,skies[kind])
    s+=circle(1430,240,118,'#CFBE99',extra='opacity=".18"')
    for yy in range(300,710,55): s+=l(0,yy,1920,yy,'#66716D',extra='opacity=".1"')
    s+='<path d="M0 630 130 612 200 652 340 588 490 625 660 580 850 630 1060 597 1270 628 1510 577 1720 612 1920 580V1080H0Z" fill="#142C31"/>'
    for i in range(12):
        xx=140+i*143; hh=90+(i%3)*30
        s+=r(xx,690-hh,115,hh,'#23383A','#4F5C52',1)
        if kind!=2:
            for a in range(3):
                for b in range(3): s+=r(xx+18+a*29,690-hh+18+b*22,11,12,light,extra=f'opacity="{.8 if kind==0 else .2}"')
    s+=r(1140,425,400,285,'#2B4345','#738075',2)+r(1105,688,470,25,'#1B2F33')
    s+='<path d="M1160 425A180 155 0 0 1 1520 425Z" fill="#4A6360" stroke="#9C9B82" stroke-width="2"/>'
    s+=r(1570,230,48,480,'#314448','#7B7E68',2)+r(1563,230,62,20,'#AB9B78')
    for yy in range(280,650,65): s+=l(1570,yy,1618,yy,'#A89572',3)
    s+=r(1320,557,70,153,'#14262C','#AB9B78',2)
    if kind==0: s+=r(1327,567,56,143,light)+circle(1355,603,170,light,extra='opacity=".05"')
    if kind==2: s+='<path d="M1110 585c-120-140 60-170-40-270 120 20 150 90 120 150 110 0 140 75 80 120" fill="#14252B" opacity=".9"/>'+circle(1594,270,8,P['red'])
    s+='<path d="M0 820 400 760 800 830 1200 740 1600 800 1920 760V1080H0Z" fill="#14272D"/>'
    for xx in [80,370,1730,1840]: s+=r(xx,730,7,290,'#17282D')+l(xx-20,770,xx+27,770,'#57605B',4)
    return s

def draw(n):
    if n==1:
        s=office(.38)+r(0,0,845,1080,P['navy'],extra='opacity=".88"')
        s+=eyebrow(110,128,'ЗАКРЫТЫЙ ГОРОД / ОКТЯБРЬ 1957')+icon('star',112,190,48,P['amber'])
        s+=text(105,330,'ЗВЕЗДА',100,P['paper'],font=SERIF)+text(110,438,'— 57',96,P['amber'],font=SERIF)
        s+=text(114,506,'Служба особого контроля',26,P['paper'])
        for i,label in enumerate(['НАЧАТЬ','НАСТРОЙКИ','ВЫХОД']): s+=button(112,574+i*101,492,label,'hover' if i==0 else 'normal',h=77)
        s+=text(112,1008,'ДОПУСК В ГОРОД НАЧИНАЕТСЯ ЗДЕСЬ',17,P['muted'],spacing=2)
        s+=tag(1550,964,'МАТЕРИАЛЫ И ТИТРЫ',w=300)
        return s
    if n==2:
        s=base('ОКОШКО ПРИЁМА')+back()+note(1290,780,['Документы ожидают','в приёмном лотке.'],w=520)
        s+=tag(66,875,'01 / ОКОШКО',w=235)
        return s
    if n==3:
        s=base('ПРЕДМЕТНОЕ ВЗАИМОДЕЙСТВИЕ')
        s+='<path d="m390 740 270-25 40 245-320 28z" fill="none" stroke="#CB9E69" stroke-width="4"/>'
        s+='<path d="m1070 791 190 15 24 105-210-5z" fill="none" stroke="#3A998A" stroke-width="4"/>'
        s+=tag(403,666,'ПАПКА / ДОСТУПНО',P['amber'],300)+tag(1060,730,'ШТАМП / ВЫБРАН',P['mint'],300)
        return s+back()+icon('mouse',770,966,27)+text(814,990,'ВЗЯТЬ ПАПКУ',24)
    if n==4:
        return base('РАБОЧЕЕ МЕСТО')+back()+metal(695,938,595,76)+icon('mouse',721,957,36)+text(779,985,'ОТКРЫТЬ КАРТУ',25,P['paper'],600,spacing=2)
    if n==5:
        return office(.3)+tag(64,64,'03 / КАРТА ГОРОДА',P['paper'],350)+back()
    if n==6:
        s=base('ОКОШКО ПРИЁМА')+metal(75,158,560,320)+eyebrow(107,203,'ПРИЁМ ПОСЕТИТЕЛЕЙ')
        for i in range(3): s+=folder(110+i*163,260,145,150,f'0{i+1}','ПОЛУЧЕНО' if i==0 else 'ОЖИДАЕТ')
        s+=lamp(574,200,P['amber'])+text(108,449,'2 папки ожидают приёма',21)
        return s+back()
    if n==7:
        return base('ОКОШКО ПРИЁМА')+button(1270,785,520,'ЮРА, ЗАБЕРИ',kind='metal',h=90)+icon('person',1300,810,36)+note(1270,895,['Поручение принято. Иду к окошку.'],520,caption='ЮРА')+back()
    if n==8:
        s=base('ПОМОЩНИК ИНСПЕКТОРА')+metal(1110,172,690,420)+eyebrow(1150,221,'ЮРА / СОСТОЯНИЕ ПОМОЩНИКА')
        for i,(lab,c) in enumerate([('СВОБОДЕН',P['mint']),('НЕСЁТ ПАПКУ',P['amber']),('ПРОВЕРЯЕТ ДЕЛО',P['muted'])]):
            yy=277+i*107
            s+=lamp(1165,yy,c)+text(1200,yy+8,lab,26,c,600,spacing=1)
        return s+back()
    if n==9:
        return base()+case_tag()+back()
    if n==10:
        s=office(.8)+document(620,117,680,850)+back()+button(1410,820,360,'УВЕЛИЧИТЬ',kind='metal',h=64)
        return s+text(1510,795,'МАСШТАБ 100%',19,P['muted'])+text(676,1010,'Лист 1 из 2',21,P['paper'])
    if n==11:
        s=desk()+header('СПРАВОЧНИК ИНСПЕКТОРА')+paper(225,166,1295,710)+l(860,180,860,860,'#B7A87F',3)
        s+=eyebrow(274,217,'СПРАВОЧНИК / РАЗДЕЛ 01',P['brass'])+title(274,280,'Институты и города',38,P['ink'])
        for i,(code,city) in enumerate([('НИИ-42','Обнинск'),('НИИ-17','Свердловск'),('НИИ-03','Москва'),('НИИ-28','Томск')]):
            yy=371+i*104
            s+=text(276,yy,code,27,P['ink'],600)+text(582,yy,city,26,P['ink'])+separator(276,yy+27,520,'#C4BBA1')
        s+=eyebrow(916,227,'ПРАВИЛА ПРОВЕРКИ',P['brass'])+lines(916,296,['Сопоставьте код института','с городом в предписании.','','При сомнениях позвоните','в справочную организацию.'],25,P['ink'],leading=42)
        s+=text(916,805,'Служебное пользование / 1957',18,P['brass'])+tabs(1520,208)+back()
        return s
    if n==12:
        return office(.8)+document(585,125,700,830)+note(1330,694,['Несоответствие записано.','Источник: телефонная проверка.'],500,caption='ПОДТВЕРЖДЁННОЕ НАБЛЮДЕНИЕ')+icon('pen',1360,846,30,P['brass'])+back()
    if n==13:
        s=desk()+header('РЕЗОЛЮЦИЯ ИНСПЕКТОРА')+paper(130,185,1000,690)
        s+=eyebrow(178,237,'ДЕЛО № 2.3 / МОРОЗОВ',P['brass'])+title(178,302,'Резолюция',48,P['ink'])
        s+=text(178,355,'Отметка инспектора по результатам проверки',24,P['ink'])+separator(178,389,904)
        s+=stamp(215,490,'ДОПУСТИТЬ',P['green'])+stamp(650,500,'ПЕРЕПРОВЕРИТЬ','#976B36',5)+stamp(446,685,'ЗАДЕРЖАТЬ',P['red'],-3)
        for i,(lab,c) in enumerate([('ДОПУСТИТЬ',P['mint']),('ПЕРЕПРОВЕРИТЬ',P['amber']),('ЗАДЕРЖАТЬ',P['red'])]):
            xx=1210+i*196
            s+=r(xx+52,363,48,175,'#623C28','#AC7B4B',3,18)+r(xx+28,515,100,40,'#2C3330','#AB966F',3,4)+r(xx+10,552,140,24,'#7C6651','#B3A279',1,3)
            s+=text(xx+80,637,lab,16,P['paper'],600,anchor='middle')
        s+=tag(1215,706,'✓  КРАСКА НАБРАНА',P['mint'],480)+back()
        return s
    if n==14:
        return base()+case_tag()+button(1280,808,510,'ПЕРЕДАТЬ ДЕЛО',h=82)+text(1292,936,'Резолюция: допустить',24,P['paper'])+text(1292,974,'До передачи решение можно изменить.',21,P['muted'])+back()
    if n==15:
        return desk()+header('ТЕЛЕФОННАЯ ПРОВЕРКА')+phone(486,182,1.7)+paper(1180,240,590,172)+eyebrow(1215,283,'НАБРАННЫЙ НОМЕР',P['brass'])+text(1215,365,'2 — 0 — 4',56,P['ink'],font=MONO)+button(1220,480,510,'СБРОСИТЬ НОМЕР',kind='metal')+note(1180,640,['Зажмите цифру на диске.','Поверните до упора и отпустите.'],590,caption='ПЕРВЫЙ НАБОР')+back()
    if n==16:
        s=office(.72)+phone(137,460,1.1)+paper(780,200,980,620)
        s+=panel_head(824,248,890,'ЛИНИЯ 204 / НИИ-42','Служебная сводка',True)
        s+=lines(824,414,['Морозов Л. Д. направлен в ваш город.','Приказ № 117/57 подтверждаем.','Срок командировки — до 18 октября.'],29,P['ink'],leading=54)
        s+=separator(824,610,890)+text(824,657,'ПОЛУЧЕНО В 14:32',20,P['brass'],600,spacing=2)+stamp(1390,670,'ПОЛУЧЕНО',P['green'],0)
        return s+back()
    if n==17:
        return office(.62)+phone(1090,375,1.3,True)+metal(1050,180,740,130)+lamp(1096,245,P['red'],12)+eyebrow(1140,226,'ВХОДЯЩИЙ ВЫЗОВ')+text(1140,274,'МОСКВА / ПРЯМАЯ ЛИНИЯ',29,P['paper'],600)+button(1160,893,590,'СНЯТЬ ТРУБКУ',h=80)+back()
    if n==18:
        s=office(.27)+r(235,676,1450,344,P['navy'],extra='opacity=".96"')+eyebrow(279,722,'ЮРА / ПОМОЩНИК ИНСПЕКТОРА')
        s+=text(279,770,'Папка на столе. Проверить человека по картотеке?',29)
        s+=button(279,810,1362,'ДА, ПРОВЕРЬ ПО КАРТОТЕКЕ',state='hover',h=66)
        s+=button(279,894,1362,'ПОКА НЕ НУЖНО. Я ПРОВЕРЮ ДОКУМЕНТЫ.',h=66)
        return s
    if n in [19,24]:
        s=desk()+header('ОПЕРАТИВНАЯ КАРТА')+map_board(route=n==24)+incident()+switchboard()
        s+=back(1450,925)
        return s
    if n==20:
        s=desk()+header('ОПЕРАТИВНАЯ КАРТА / СИГНАЛЫ СЕКТОРА')+panel_head(140,190,1640,'СЕКТОР 04 / ЭНЕРГОБЛОК','От тревоги до отбоя')
        for i,(status,c,ico,desc) in enumerate([('ТРЕВОГА',P['red'],'cross','Требуется реакция'),('ПРИНЯТО',P['amber'],'clock','Экипаж направлен'),('ЗАВЕРШЕНО',P['mint'],'check','Происшествие закрыто')]):
            xx=140+i*570
            s+=metal(xx,345,500,480)+r(xx+24,369,452,310,P['green'])
            s+=f'<path d="m{xx+75} 420 270-15 85 190-250 45-90-120z" fill="none" stroke="{c}" stroke-width="3"/>'
            s+=text(xx+250,495,'04',58,P['paper'],font=SERIF,anchor='middle')+lamp(xx+250,565,c,14)+icon(ico,xx+340,435,40,c)
            s+=text(xx+250,733,status,26,c,600,anchor='middle',spacing=2)+text(xx+250,782,desc,23,P['paper'],anchor='middle')
        return s+back()
    if n==21:
        return desk()+header('ОПЕРАТИВНАЯ КАРТА / СВОДКА ПО СЕКТОРУ')+map_board(90,260,.83)+incident(1240,170,560)+tag(190,855,'СЕКТОР 04 / ВЫБРАН',P['amber'],410)+back()
    if n==22:
        s=desk()+header('КОММУТАТОР / КАНАЛЫ СЛУЖБ')+panel_head(140,197,1640,'РАСПРЕДЕЛЕНИЕ ЭКИПАЖЕЙ','Состояние служб')
        services=[('ОПЕРГРУППА','СВОБОДЕН',P['mint'],'person'),('ВОХР','В ПУТИ',P['amber'],'shield'),('ПОЖАРНЫЕ','НА МЕСТЕ',P['red'],'flame'),('РЕМОНТ','ВОЗВРАЩАЕТСЯ',P['muted'],'wrench')]
        for i,(name,status,c,ico) in enumerate(services):
            xx=140+i*426
            s+=metal(xx,330,370,480)+icon(ico,xx+146,365,78,P['amber'])+text(xx+185,502,name,24,P['paper'],600,anchor='middle',spacing=1)
            s+=circle(xx+185,595,41,'#0D1D22','#9E8B65',6)+circle(xx+185,595,17,c)+lamp(xx+53,707,c)+text(xx+82,715,status,21,c,600)
            s+=text(xx+185,774,'КАНАЛ 01',18,P['muted'],anchor='middle',spacing=2)
        return s+back()
    if n==23:
        s=desk()+header('ПРОИСШЕСТВИЕ / ОСТАВШЕЕСЯ ВРЕМЯ')
        for i,(time,label,c) in enumerate([('01:24','ШТАТНЫЙ ОТСЧЁТ',P['amber']),('00:18','!  КРИТИЧЕСКИ МАЛО',P['red'])]):
            xx=155+i*860
            s+=metal(xx,280,750,430)+eyebrow(xx+45,340,'СЕКТОР 04 / ДО УХУДШЕНИЯ')+text(xx+375,523,time,112,c,font=MONO,anchor='middle')+text(xx+375,638,label,24,c,600,anchor='middle',spacing=2)
        return s+back()
    if n==25:
        s=desk()+header('СОСТОЯНИЕ ГОРОДА')+panel_head(160,192,1600,'КОНТРОЛЬНЫЕ ПОКАЗАТЕЛИ','Город готовится к пуску')
        for i,(label,v,c) in enumerate([('ПУСК',68,P['mint']),('СЕКРЕТНОСТЬ',84,P['mint']),('СПОКОЙСТВИЕ',29,P['red'])]): s+=gauge(160+i*550,350,label,v,c,1.18)
        s+=note(160,800,['−15 к спокойствию: задержана калибровка.'],780,caption='ИЗМЕНЕНИЕ ПО ПОСЛЕДНЕМУ СОБЫТИЮ')+tag(1320,830,'!  СПОКОЙСТВИЕ КРИТИЧНО',P['red'],450)
        return s+back()
    if n==26: return reserves()
    if n==27:
        s=desk()+header('РЕЗЕРВЫ / КАРТОЧКИ УЛУЧШЕНИЙ')+panel_head(190,190,1540,'ШЕСТЬ УЛУЧШЕНИЙ / ЕДИНЫЙ КОМПОНЕНТ','Ведомственные резервы')
        for i in range(6): s+=upgrade_card(190+(i%2)*800,340+(i//2)*190,i,['normal','selected','disabled','normal','bought','normal'][i])
        return s+back()
    if n==28:
        s=reserves()+r(0,0,1920,1080,P['navy'],extra='opacity=".8"')+paper(490,265,940,550)
        s+=icon('check',920,314,80,P['mint'])+text(960,464,'Резервы утверждены',44,P['ink'],font=SERIF,anchor='middle')
        s+=lines(960,537,['Выделены оперативная группа','и ускоренный выезд. Потрачено: 5 очков.'],25,P['ink'],anchor='middle',leading=39)
        return s+button(620,659,680,'НАЧАТЬ СЛЕДУЮЩУЮ СМЕНУ',kind='metal',h=76)
    if n==29:
        s=office(.78)+paper(390,70,1140,940)+panel_head(447,123,1026,'СМЕНА 02 / 16 ОКТЯБРЯ 1957','Итоговая сводка',True)
        for i,(num,label) in enumerate([('12','ДЕЛ ОБРАБОТАНО'),('03','ЧП ЗАКРЫТО'),('02','УЛИКИ ПОЛУЧЕНЫ')]):
            xx=447+i*350
            s+=text(xx,345,num,76,P['ink'],font=SERIF)+text(xx,386,label,18,P['brass'],600,spacing=1)
        s+=separator(447,427,1026)
        for i,(lab,val,delta) in enumerate([('Пуск','68 / 100','+12'),('Секретность','84 / 100','+4'),('Спокойствие','29 / 100','−15')]):
            yy=491+i*79
            s+=text(447,yy,lab,28,P['ink'])+text(1187,yy,val,28,P['ink'],anchor='end')+text(1458,yy,delta,28,P['red'] if i==2 else P['green'],600,anchor='end')+separator(447,yy+28,1026,'#C7BDA3')
        s+=text(447,777,'Резервов к распределению: 5 очков',25,P['ink'])+text(447,823,'Все последствия сохранены в журнале смены.',22,'#68705E')
        return s+button(447,885,1026,'ПРОДОЛЖИТЬ',kind='metal',h=76)
    if n==30:
        return ending(0)
    if n==31:
        s=office(.78)+paper(590,183,740,715)+text(960,241,'ЗВЕЗДА-57 / СМЕНА 02',18,P['brass'],600,anchor='middle',spacing=3)
        s+=text(960,321,'Пауза',61,P['ink'],font=SERIF,anchor='middle')+text(960,372,'Время в городе остановлено',24,'#68705E',anchor='middle')
        for i,lab in enumerate(['ПРОДОЛЖИТЬ','ЗАНОВО СМЕНУ','ГЛАВНОЕ МЕНЮ']): s+=button(650,425+i*112,620,lab,'hover' if i==0 else 'normal',h=78)
        return s+text(960,831,'Настройки',25,P['ink'],anchor='middle')
    if n==32:
        s=office(.78)+paper(430,95,1060,890)+panel_head(490,153,940,'ПАРАМЕТРЫ ИГРЫ','Настройки',True)
        for i,(lab,value) in enumerate([('Звук',80),('Музыка',55),('Голоса',100)]):
            yy=351+i*113
            s+=text(490,yy,lab,28,P['ink'])+r(810,yy-13,500,6,'#BBB49C',rx=3)+r(810,yy-13,value*5,6,P['green'],rx=3)+circle(810+value*5,yy-10,15,P['paper'],P['green'],3)+text(1420,yy,f'{value}%',23,P['ink'],anchor='end',font=MONO)
        for i,lab in enumerate(['Субтитры','Подсказки']):
            yy=701+i*93
            s+=text(490,yy,lab,28,P['ink'])+r(1290,yy-30,130,45,P['green'],rx=23)+circle(1396,yy-8,17,P['paper'])+text(1360,yy+5,'ВКЛ',15,P['paper'],anchor='end',weight=600)
        return s+button(490,866,940,'НАЗАД',kind='metal',h=65)
    if n==33:
        s=office(.25)+r(325,863,1270,147,P['navy'],extra='opacity=".96"')+eyebrow(365,904,'ЮРА / ПО РАДИО')
        return s+lines(365,948,['Инспектор, в четвёртом секторе перебои с питанием.','Карта уже у вас. Ждём распоряжений.'],27,P['paper'],leading=39)
    if n==34:
        s=desk()+header('ЕДИНЫЕ СОСТОЯНИЯ УПРАВЛЕНИЯ')+panel_head(130,190,1660,'КОМПОНЕНТЫ / КНОПКИ','Понятная обратная связь')
        for i,(state,label) in enumerate([('normal','ОБЫЧНОЕ'),('hover','НАВЕДЕНИЕ'),('pressed','НАЖАТО'),('selected','ВЫБРАНО'),('disabled','НЕДОСТУПНО')]):
            yy=330+i*123
            s+=text(130,yy+40,label,22,P['paper'],600,spacing=2)+button(510,yy,560,'ПЕРЕДАТЬ ДЕЛО',state,h=70)+button(1170,yy,370,'НАЗАД',state,'metal',70)
        return s
    if n==35:
        s=office(.8)+paper(390,75,1140,930)+panel_head(450,132,1020,'ЗВЕЗДА-57 / СПРАВОЧНЫЕ МАТЕРИАЛЫ','Титры и источники',True)
        content=[('ПРОЕКТ','«Звезда-57» — служба особого контроля'),('ТЕХНОЛОГИИ','Игровой движок Unity · язык C#'),('МУЗЫКА И ЗВУК','Авторы и лицензии аудиозаписей'),('ИЗОБРАЖЕНИЯ И ИИ','Иллюстрация кабинета предоставлена в каталоге проекта.'),('ИСТОЧНИКИ','Перечень авторов, инструментов и лицензий')]
        for i,(a,b) in enumerate(content):
            yy=322+i*116
            s+=eyebrow(450,yy,a,P['brass'])+text(450,yy+43,b,23,P['ink'])
        s+=r(1478,277,6,524,'#C4BBA1',rx=3)+r(1478,277,6,150,P['brass'],rx=3)+button(450,903,700,'НАЗАД',kind='metal',h=61)+button(1195,903,114,'↑',h=61)+button(1350,903,114,'↓',h=61)
        return s
    raise ValueError(n)

def ending(kind):
    s=ending_art(kind)+r(0,674,1920,406,P['navy'],extra='opacity=".96"')
    names_=['Пуск состоялся','Город замолчал','Аварийная тьма']
    summaries=[['Реактор выведен на расчётную мощность.','Ваши решения позволили завершить подготовку.'],['Подготовка остановлена. Жители покидают город.','Решение о новом пуске отложено.'],['Энергоблок потерян. Пуск отменён.','Город переходит на аварийное питание.']]
    s+=eyebrow(96,727,'ИТОГ ОПЕРАЦИИ / ЗВЕЗДА-57')+title(96,802,names_[kind],58)+lines(98,855,summaries[kind],25,P['paper'],leading=39)
    return s+button(1120,904,350,'ГЛАВНОЕ МЕНЮ',h=74)+button(1510,904,310,'ЗАНОВО',kind='metal',h=74)

DEFS='''<defs>
<pattern id="papergrain" width="19" height="19" patternUnits="userSpaceOnUse"><path d="M1 4h3M11 14h2M6 10h1M16 3h1" stroke="#887A5A" stroke-width=".5" opacity=".5"/></pattern>
<pattern id="felt" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 1h7M1 0v7" stroke="#728069" opacity=".1" stroke-width=".5"/></pattern>
</defs>'''
def svg(s,w=1920,h=1080,label='Звезда 57'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">{DEFS}{s}</svg>'

def main():
    catalog=json.loads((ROOT/'UI/catalog.json').read_text())
    for item in catalog['items']:
        n=item['number']; filename=f'UI_{n:03}_{names[n-1]}'
        item.update(svg=f'UI-{n:03}.svg',png=f'Previews/1080p/{filename}.png',preview=f'Previews/720p/{filename}.png')
        (OUT/f'UI-{n:03}.svg').write_text(svg(draw(n),label=item['name']))
        duplicate=ROOT/f'UI/Source/Artboards/{filename}.svg'
        if duplicate.exists(): duplicate.unlink()
    # All three endings use the same editable UI layer and different backgrounds.
    for k,name in enumerate(['LAUNCH','EMPTY_CITY','BLACKOUT']):
        (ROOT/f'UI/Source/Artboards/UI_030_ENDING_{name}.svg').write_text(svg(ending(k),label=f'Концовка {name}'))
        (ROOT/f'UI/Source/Components/UI_030_BACKGROUND_{name}.svg').write_text(svg(ending_art(k),label=f'Фон концовки {name}'))
    comp=ROOT/'UI/Source/Components'
    for state in ['normal','hover','pressed','selected','disabled']:
        for kind in ['paper','metal']:
            # Blank nine-slice backgrounds: all dynamic labels stay in runtime text.
            value=button(0,0,560,'',state,kind,80)
            (comp/f'UI_034_BUTTON_{kind}_{state}.svg').write_text(svg(value,560,86,'Подложка кнопки'))
    for kind,content,w,h in [('PAPER',paper(0,0,512,512),524,526),('METAL',metal(0,0,512,256),520,266)]:
        (comp/f'UI_PANEL_{kind}.svg').write_text(svg(content,w,h,'Подложка'))
    for name in ['arrow','folder','check','cross','clock','phone','person','flame','shield','wrench','radio','bolt','mouse','pen','pause','sound','star','train','lock']:
        (comp/f'UI_ICON_{name}.svg').write_text(svg(icon(name,8,8,48),64,64,name))
    for i,(name,effect,cost,ico) in enumerate(upgrades):
        (comp/f'UI_027_UPGRADE_ICON_{i+1:02}.svg').write_text(svg(icon(ico,8,8,48),64,64,name))
    for state in ['normal','hover','pressed']:
        for kind in ['paper','metal']:
            (comp/f'UI_002_BACK_{kind}_{state}.svg').write_text(svg(button(0,0,230,'',state,kind,64)+icon('arrow',18,17,28,P['ink'] if kind=='paper' else P['paper']),234,70,'Назад'))
    for status,color in [('available',P['mint']),('enroute',P['amber']),('working',P['red']),('returning',P['muted'])]:
        (comp/f'UI_022_CREW_{status}.svg').write_text(svg(lamp(24,24,color,12),48,48,status))
    for status,color,ico in [('alert',P['red'],'cross'),('response',P['amber'],'clock'),('resolved',P['mint'],'check')]:
        (comp/f'UI_020_MAP_{status}.svg').write_text(svg(circle(32,32,28,P['navy'],color,2)+icon(ico,14,14,36,color),64,64,status))
    (comp/'UI_001_LOGO.svg').write_text(svg(text(0,105,'ЗВЕЗДА',100,P['paper'],font=SERIF)+text(5,215,'— 57',96,P['amber'],font=SERIF),650,240,'Звезда 57'))
    # UI labels below are examples; localized strings are stored separately in catalog.json.
    (comp/'UI_010_DOCUMENT_blank.svg').write_text(svg(paper(0,0,680,850),690,860,'Подложка документа'))
    def emit(name,content,w,h):
        (comp/f'{name}.svg').write_text(svg(content,w,h,name))
    # Runtime assets deliberately exclude variable text, costs, names and timers.
    emit('UI_001_MENU_background',office(.38)+r(0,0,845,1080,P['navy'],extra='opacity=".88"'),1920,1080)
    emit('UI_004_CONTEXT_available',metal(0,0,595,76)+icon('mouse',26,19,36),603,86)
    emit('UI_004_CONTEXT_busy',metal(0,0,595,76)+icon('clock',26,19,36,P['muted']),603,86)
    for key,shape in [('left','M10 6h9v11h-9z'),('right','M21 6h9v11h-9z'),('wheel','M18 7h4v9h-4z')]:
        emit(f'UI_004_MOUSE_{key}',icon('mouse',12,7,40)+f'<path transform="translate(12 7)" d="{shape}" fill="{P["amber"]}"/>',64,56)
    emit('UI_005_VIEW_base',r(0,0,350,42,P['navy'],P['brass'],1,2),350,42)
    emit('UI_006_QUEUE_folder',r(0,0,78,20,'#A39770',rx=2)+r(0,16,150,150,'#CCBC8C','#81724F',1,3),152,168)
    for key,state in [('available','normal'),('busy','disabled')]:
        emit(f'UI_007_YURA_CALL_{key}',button(0,0,520,'',state,'metal',90)+icon('person',30,25,36),524,98)
    for key,c in [('free',P['mint']),('carrying',P['amber']),('checking',P['muted'])]:
        emit(f'UI_008_YURA_{key}',lamp(24,24,c,12),48,48)
    emit('UI_009_CASE_base',paper(0,0,580,75)+icon('folder',20,19,32,P['brass'])+lamp(545,37),590,86)
    for key,c in [('normal','#BCB89F'),('active',P['amber'])]:
        emit(f'UI_011_TAB_{key}',r(0,0,182,84,c,'#6D705D',1,2),184,86)
    emit('UI_012_EVIDENCE_base',paper(0,0,500,130)+icon('pen',24,28,32,P['brass']),510,140)
    emit('UI_013_INK_ready',icon('check',4,4,40,P['mint']),48,48)
    emit('UI_013_INK_empty',icon('cross',4,4,40,P['muted']),48,48)
    for key,state in [('enabled','normal'),('disabled','disabled')]:
        emit(f'UI_014_SUBMIT_{key}',button(0,0,510,'',state,h=82),515,90)
    emit('UI_015_DIAL_strip',paper(0,0,590,172),600,182)
    emit('UI_016_PHONE_REPORT_base',paper(0,0,980,620),990,630)
    for key,c in [('active',P['red']),('missed',P['muted'])]:
        emit(f'UI_017_INCOMING_{key}',metal(0,0,740,130)+lamp(46,65,c,12),748,140)
    emit('UI_018_DIALOGUE_base',r(0,0,1450,344,P['navy'],extra='opacity=".96"'),1450,344)
    map_base=map_board(0,0,1,-1)
    # The map asset contains no labels; sector numbers are runtime text.
    map_base=re.sub(r'<text\b[^>]*>.*?</text>','',map_base)
    emit('UI_019_MAP_base',map_base,1270,672)
    emit('UI_021_INCIDENT_base',paper(0,0,440,640)+separator(30,172,380)+r(30,502,380,95,P['navy'],rx=3),450,650)
    for key,c in [('normal',P['amber']),('critical',P['red'])]:
        emit(f'UI_023_COUNTDOWN_{key}',metal(0,0,750,430)+r(30,400,690,3,c),758,440)
    emit('UI_024_ROUTE_base','<path d="M12 100 120 100 260 30 475 30" fill="none" stroke="#CB9E69" stroke-width="4" stroke-dasharray="12 10"/>',500,130)
    gauge_base=gauge(0,0,'',0)
    gauge_base=re.sub(r'<text\b[^>]*>.*?</text>','',gauge_base)
    # Remove the red needle from the dial; a separate centered needle is animated in Unity.
    gauge_base=re.sub(r'<line\b[^>]*stroke="#B64F49"[^>]*/>','',gauge_base)
    emit('UI_025_GAUGE_base',gauge_base,430,345)
    emit('UI_025_GAUGE_needle',l(112,12,12,12,P['red'],4)+circle(112,12,8,P['ink']),124,24)
    emit('UI_026_RESERVES_base',paper(0,0,1610,930),1620,940)
    for key,color in [('normal','#A9A38E'),('selected',P['mint']),('purchased',P['green']),('disabled','#8D9387')]:
        emit(f'UI_027_UPGRADE_{key}',r(0,0,700,165,'#EAE4D2',color,2,2)+r(20,24,86,86,P['navy'],rx=3)+circle(650,49,25,P['navy']),704,169)
    emit('UI_028_APPROVE_base',button(0,0,545,'',kind='metal',h=76),550,84)
    emit('UI_029_SHIFT_REPORT_base',paper(0,0,1140,940),1150,950)
    emit('UI_030_ENDING_caption',r(0,0,1920,406,P['navy'],extra='opacity=".96"'),1920,406)
    emit('UI_031_PAUSE_base',paper(0,0,740,715),750,725)
    confirm=office(.78)+paper(490,315,940,450)+text(960,404,'Начать смену заново?',44,P['ink'],font=SERIF,anchor='middle')+text(960,471,'Несохранённые решения этой смены будут потеряны.',25,P['ink'],anchor='middle')+button(550,573,390,'ВЕРНУТЬСЯ',h=80)+button(980,573,390,'НАЧАТЬ ЗАНОВО',kind='metal',h=80)
    (ROOT/'UI/Source/Artboards/UI_031_PAUSE_CONFIRM.svg').write_text(svg(confirm,label='Подтверждение перезапуска'))
    emit('UI_032_SLIDER_track',r(0,12,500,6,'#BBB49C',rx=3),500,30)
    emit('UI_032_SLIDER_fill',r(0,12,500,6,P['green'],rx=3),500,30)
    emit('UI_032_SLIDER_handle',circle(20,20,15,P['paper'],P['green'],3),40,40)
    for key,on in [('on',True),('off',False)]:
        emit(f'UI_032_TOGGLE_{key}',r(0,0,130,45,P['green'] if on else '#777B70',rx=23)+circle(106 if on else 24,22,17,P['paper']),132,47)
    emit('UI_033_SUBTITLES_base',r(0,0,1270,147,P['navy'],extra='opacity=".96"'),1270,147)
    emit('UI_035_CREDITS_base',paper(0,0,1140,930),1150,940)
    # Words in the three ink marks are intentional fixed artwork, not dynamic labels.
    for label,key,c in [('ДОПУСТИТЬ','ALLOW',P['green']),('ПЕРЕПРОВЕРИТЬ','RECHECK','#976B36'),('ЗАДЕРЖАТЬ','DETAIN',P['red'])]:
        (comp/f'UI_013_STAMP_{key}.svg').write_text(svg(stamp(20,25,label,c,0),300,135,label))
    (ROOT/'UI/manifest.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2))
    (ROOT/'UI/Materials/design-tokens.json').write_text(json.dumps({'colors':P,'canvas':{'width':1920,'height':1080,'safeMargin':48},'type':{'body':24,'heading':44,'caption':18,'font':FONT,'headingFont':SERIF},'button':{'states':['normal','hover','pressed','selected','disabled'],'minHitArea':48,'nineSliceBorder':16},'motion':{'hoverMs':100,'viewLabelMs':1600,'alertPulseMs':1800,'reducedMotion':True},'text':'All dynamic labels are separate text nodes. PNG artboards are previews only.'},ensure_ascii=False,indent=2))
    print('Wrote 35 artboards, 3 ending variants and reusable vector components.')

if __name__=='__main__': main()
