"""Review plot of the saved geographic access manifest (north is up)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
data=json.loads((R/'data'/'campus-catalog.json').read_text(encoding='utf8'));survey=json.loads((R/'data'/'access-survey.json').read_text(encoding='utf8'))
im=Image.new('RGB',(2000,1430),'#f6f5f0');dr=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/NotoSansCJKjp-Regular.otf'),n)
def p(x,y):return (80+(x+315)*2.65,220+(215-y)*2.65)
dr.text((70,45),'松ヶ崎キャンパス｜校門・塔・出入口の修正',font=font(38),fill='#193b41')
dr.text((73,107),'v5　大学公式配置図・バリアフリーマップ・写真を建物輪郭へ対応',font=font(21),fill='#476469')
for poly in data['boundaries']:dr.polygon([p(*v) for v in poly],fill='#e5eadc',outline='#a7b69e')
for road in data['roads']:dr.polygon([p(*v) for v in road['points']],fill='#d6d9d5')
for b in data['catalog']:
 dr.polygon([p(*v) for v in b['points']],fill='#9eafb3',outline='#556d76')
 name=b['name'].split()[0]
 if name.isdigit() or name in ['E1','E2','E3','E4','2S','2N','17N','17S']:
  dr.text(p(*b['representative']),name,font=font(14),anchor='mm',fill='#183d4d')
# Historic 3 is a linked detailed model, so its outline is outside the generic catalog.
from shapely.geometry import Polygon,box
historic=next(b for b in data['buildings'] if b['index']==55)
shape=Polygon(historic['points']).intersection(box(-87,-140,0,-25))
if shape.geom_type=='Polygon':dr.polygon([p(*v) for v in shape.exterior.coords],fill='#9eafb3',outline='#556d76')
dr.text(p(-52,-71),'3号館',font=font(18),anchor='mm',fill='#183d4d')
for e in survey['entrances']:
 x,y=e['xy'];nx,ny=e['normal'];a=p(x,y);tail=p(x+nx*4.5,y+ny*4.5)
 dr.line([tail,a],fill='#c16b21',width=3);dr.ellipse((a[0]-3,a[1]-3,a[0]+3,a[1]+3),fill='#dc7725')
for i,g in enumerate(survey['gates'],1):
 x,y=p(*g['xy']);dr.ellipse((x-13,y-13,x+13,y+13),fill='#af3536',outline='white',width=2)
 dr.text((x,y-1),str(i),font=font(15),anchor='mm',fill='white')
 tx,ty=1740,255+(i-1)*62;dr.text((tx,ty),f'{i}  {g["name"]}',font=font(19),fill='#7f262c')
tx,ty=p(*survey['tower']['xy']);dr.rectangle((tx-8,ty-8,tx+8,ty+8),fill='#236c97',outline='white',width=2)
dr.line([(tx,ty),(tx+35,ty+55)],fill='#236c97',width=2);dr.text((tx+36,ty+47),'大学の塔',font=font(19),fill='#236c97')
dr.text((1740,815),'● 入口：65か所',font=font(20),fill='#b05b1e');dr.text((1740,850),'　対象：48棟',font=font(20),fill='#b05b1e')
dr.text((1740,925),'■ 塔の位置は',font=font(19),fill='#236c97');dr.text((1740,955),'　地図・写真から推定',font=font(16),fill='#236c97')
dr.text((1750,1100),'N',font=font(27),fill='#193b41');dr.line([(1762,1190),(1762,1140)],fill='#193b41',width=3);dr.polygon([(1762,1120),(1753,1143),(1771,1143)],fill='#193b41')
dr.line([p(-300,-145),p(-250,-145)],fill='#193b41',width=4);dr.text(p(-300,-150),'50 m',font=font(16),fill='#193b41')
dr.text((75,1320),'入口の面と相対位置を資料から読み取り。寸法・スロープ形状・塔の位置は推定を含みます。',font=font(21),fill='#476469')
dr.text((75,1373),'© OpenStreetMap contributors (ODbL 1.0) / 配置・入口の根拠：京都工芸繊維大学 公開資料　　調査 2026-09-10',font=font(16),fill='#637277')
im.save(R/'build'/'access-plan.png')
