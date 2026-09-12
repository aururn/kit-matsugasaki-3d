"""V4 architectural components. Executed in the campus builder namespace.
Observed components are identified in profiles; unobserved dimensions are estimates.
"""
import hashlib
detail_counts={}
profiles={
 '1 Main teaching building':dict(kind='red laboratory',spacing=5.6,lights=4,vent='round',recess=.20,source='building1.jpg',features='brick piloti, corner-glazed stair tower, four-light windows, circular wall vents'),
 '2S Teaching building south':dict(kind='brown teaching block',spacing=4.8,lights=3,vent='hood',recess=.23,source='kitmap-building-11.png',features='five-storey observed facade including entrance level, broad column-supported canopy, upper window ventilation hoods'),
 '2N Teaching building north':dict(kind='teaching north wing',spacing=4.8,lights=3,vent='hood',recess=.23,source=None,features='window detailing inferred from adjoining south wing'),
 'University Library':dict(kind='library',spacing=5.8,lights=5,vent='round',recess=.18,source='kitmap-building-7.png',features='five-light windows, round ventilation inserts, shallow bronze entrance canopy, glass vestibule'),
 'University Hall':dict(kind='student hall',spacing=6.2,lights=3,vent=None,recess=.30,source='kitmap-building-10.png',features='square tile field, contrasting horizontal bands, open double-height colonnade and broad red tiled stair'),
 'E1 East Building 1':dict(kind='east laboratory',spacing=5.6,lights=5,vent='round',recess=.22,source='kitmap-building-13.jpg',features='five-storey ribbon glazing, small projecting balconies, deep roof eaves, tiled entrance canopy'),
 'E2 East Building 2':dict(kind='east laboratory',spacing=5.6,lights=5,vent='round',recess=.22,source=None,features='details inferred from adjoining east 1 building'),
 '15 Teaching building':dict(kind='newer laboratory',spacing=3.5,lights=2,vent='louver',recess=.28,source='kitmap-building-15.jpg',features='narrow upper windows, broad white floor ledges, recessed shadow lines and upper ventilation grilles'),
 '14 Teaching building':dict(kind='newer laboratory',spacing=3.5,lights=2,vent='louver',recess=.28,source=None,features='details inferred from adjoining 15 building'),
 'Museum of Arts and Crafts':dict(kind='museum',spacing=5,lights=3,vent=None,recess=.32,source='kitmap-building-6.png',features='deep central entrance void, projected upper picture window, sparse slit windows, vertical concrete fins'),
 'Plaza KIT':dict(kind='perforated metal pavilion',spacing=2,lights=2,vent=None,recess=.16,source='kitmap-building-8.png',features='folded metal screen, glass doorway, projecting thin roof and concrete entrance wall'),
 'KIT HOUSE':dict(kind='brick-screen dining pavilion',spacing=2,lights=2,vent=None,recess=.16,source='1-kit_house_D02-2000x1334.jpg',features='brick screen, rooflight frames and flashings, terrace railings and stair fittings'),
 '60th Anniversary Hall':dict(kind='white anniversary pavilion',spacing=2,lights=2,vent=None,recess=.18,source='hall60-100.jpg',features='curved upper envelope, sheet-metal panel seams, lobby transoms and eaves gutter'),
 'Center Hall and learning building':dict(kind='brick auditorium',spacing=2,lights=2,vent=None,recess=.22,source='kitmap-building-4.png',features='stepped lobby, dark horizontal glazing, recessed entry door, separate lower learning wing'),
}
base_profiles={
 'lab':dict(kind='research laboratory',spacing=4.2,lights=3,vent='hood',recess=.22),
 'cream':dict(kind='painted teaching block',spacing=4.4,lights=3,vent='round',recess=.18),
 'brown':dict(kind='brown teaching block',spacing=4.8,lights=4,vent='round',recess=.21),
 'research13':dict(kind='glazed research block',spacing=3.0,lights=2,vent=None,recess=.20),
 'heritage':dict(kind='timber heritage building',spacing=3.8,lights=2,vent=None,recess=.20),
 'historic_extension':dict(kind='historic return extension',spacing=3.8,lights=3,vent=None,recess=.22),
 'industrial':dict(kind='workshop',spacing=4.5,lights=4,vent='louver',recess=.20),
 'shed':dict(kind='service outbuilding',spacing=4.5,lights=2,vent='louver',recess=.17),
 'gym':dict(kind='sports hall',spacing=5.5,lights=4,vent='louver',recess=.25),
 'dlab':dict(kind='design laboratory',spacing=2.5,lights=2,vent=None,recess=.18),
 'pavilion':dict(kind='pavilion',spacing=3.2,lights=2,vent=None,recess=.20),
 'plaza':dict(kind='light pavilion',spacing=2.5,lights=2,vent=None,recess=.16),
}
for b in data['catalog']:
 p=dict(profiles.get(b['name'],base_profiles.get(b['style'],base_profiles['cream'])))
 p.setdefault('source',None);p.setdefault('features','constructed window reveals, separate sashes, door joinery, drainage and roof services; locations inferred')
 p['evidence_level']='photo-informed components; dimensions estimated' if p['source'] else 'architectural detailing inferred; not photographically verified'
 profiles[b['name']]=p;b['detail_profile']=p
 if b['name']=='2S Teaching building south':b['floors']=5;b['height']=19.1;b['style']='brown'
 if b['name']=='University Hall':b['style']='brown'

def tally(b,what,n=1):
 d=detail_counts.setdefault(b['name'],{});d[what]=d.get(what,0)+n

def small_round(mx,point,u,v,z,r,mat):
 # Raised vent cap with an actual cylindrical rim.
 mx.beam(point(u,v-.04,z),point(u,v+.015,z),r,mat,12)
 mx.beam(point(u,v-.052,z),point(u,v-.043,z),r*.68,dark,12)

def refined_window(mx,boxloc,point,b,u,ww,low,high,door,ei,j,f):
 p=profiles[b['name']];recess=p['recess'];hh=high-low
 if hh<.2:return
 # Opening has its own deep lining and a second slim sash frame.
 for x in [-ww/2+.038,ww/2-.038]:boxloc(u+x,.16,(low+high)/2,.055,.30,hh,frames)
 for z in [low+.035,high-.035]:boxloc(u,.16,z,ww,.30,.05,frames)
 lights=max(2,min(p['lights'],int(ww/.38)))
 for i in range(lights):
  x=u-ww/2+(i+.5)*ww/lights;w=ww/lights-.07
  for xx in [-w/2,w/2]:boxloc(x+xx,.025,(low+high)/2,.026,.045,hh-.10,frames)
  for zz in [low+.08,high-.08]:boxloc(x,.025,zz,w,.045,.026,frames)
  if not door:
   # Partial interior blinds leave some room depth visible.
   fraction=[.16,.28,.49,.72,.91][(i+j*3+f+ei)%5]
   blindh=max(.12,(hh-.15)*fraction)
   boxloc(x,.36,high-.075-blindh/2,w,.02,blindh,glasses[2])
   for k in range(int(blindh/.13)):
    boxloc(x,.34,high-.09-k*.13,w,.017,.012,white)
   boxloc(x+w*.38,-.015,(low+high)/2,.021,.035,.16,frames)
 if door:
  for x in [-ww*.24,ww*.24]:
   boxloc(u+x,.028,low+.19,ww*.47,.045,.28,frames)
   for zz in [low+.4,high-.18]:boxloc(u+x,.015,zz,ww*.46,.035,.035,frames)
   boxloc(u+x,-.045,high-.25,.20,.10,.045,grey)
  boxloc(u,-.03,low+.015,ww+.10,.48,.032,grey)
  boxloc(u,-.06,high+.10,ww,.045,.13,frames)
  # Recessed mat, entry light, control panel and tactile warning strip.
  boxloc(u,-.65,.155,min(ww,1.9),.75,.012,dark)
  boxloc(u+ww/2+.30,-.06,1.4,.13,.09,.24,grey)
  boxloc(u+ww/2+.30,-.112,1.45,.08,.008,.06,glass)
  boxloc(u,-.35,high+.23,.75,.17,.05,white)
  for xx in range(12):boxloc(u-.60+xx*.10,-1.6,.16,.045,.38,.015,concrete)
  tally(b,'detailed entrance assemblies')
 else:
  boxloc(u,-.20,low-.10,ww+.13,.46,.035,grey)
  boxloc(u,-.425,low-.075,ww+.13,.025,.09,grey)
  boxloc(u,-.02,high+.055,ww+.13,.055,.045,grey)
  if p['vent']=='round' and ww>1.5:
   for ss in [-1,1]:
    x=u+ss*(ww/2-.18);boxloc(x,.009,high-.22,.31,.04,.31,white);small_round(mx,point,x,-.024,high-.22,.103,frames)
  elif p['vent']=='hood':
   boxloc(u,-.045,high-.22,.22,.20,.18,grey)
   boxloc(u,-.15,high-.30,.22,.03,.025,dark)
  elif p['vent']=='louver':
   for z in range(5):boxloc(u,-.03,high-.04-z*.038,ww-.12,.035,.016,grey)
  tally(b,'detailed window assemblies')

def rail(mx,point,u0,u1,v,z):
 for zz in [z+.52,z+1.05]:mx.beam(point(u0,v,zz),point(u1,v,zz),.027,frames)
 for j in range(max(2,int((u1-u0)/.8))+1):
  u=u0+(u1-u0)*j/max(2,int((u1-u0)/.8));mx.beam(point(u,v,z),point(u,v,z+1.06),.021,frames)

def entrance_portico(mx,boxloc,point,b,length,h,kind):
 u=primary_entry_u(b,active_entry_edge,length);w=min(length*.48,10.5);depth=3.4;z=3.35
 if kind=='library':w=min(7,length*.5);depth=2.4;z=3.05
 if kind=='east laboratory':w=min(8,length*.4);depth=3.8;z=3.45
 # A sheltered approach supported by real columns and a jointed soffit.
 boxloc(u,-depth/2,z,w,depth,.20,brown if kind=='east laboratory' else grey)
 boxloc(u,-depth/2,z-.13,w-.20,depth-.12,.045,white)
 for x in [-w/2+.18,w/2-.18]:boxloc(u+x,-depth+.25,z/2,.23,.23,z,frames)
 for i in range(max(2,int(w))):boxloc(u-w/2+(i+.5)*w/max(2,int(w)),-depth/2,z-.17,.012,depth-.15,.015,grey)
 for x in [-w*.23,w*.23]:boxloc(u+x,-depth*.55,z-.18,.45,.45,.03,white)
 if b['name'] not in access_manifest:
  for i in range(5):boxloc(u,-depth-.6+i*.30,.06+i*.035,w+1,.35,.07,concrete)
 else:boxloc(u,-depth/2,.08,w+.5,depth,.12,concrete)
 tally(b,'individual entrance portico')

def refined_edge(mx,boxloc,point,b,length,ei,dooridx,n,pitch,h):
 name=b['name'];p=profiles[name];fh=(h-.6)/b['floors']
 if length<4:return
 # Expansion joints and rainwater hopper heads placed at wall piers.
 for u in [1.1,length-1.1]:
  boxloc(u,-.14,h-.18,.20,.27,.28,grey)
  mx.beam(point(u,-.14,h-.20),point(u,-.25,h-.48),.045,grey)
  mx.beam(point(u,-.14,.32),point(u,-.40,.12),.045,grey)
  boxloc(u,-.47,.09,.45,.35,.05,grey)
  for k in range(5):boxloc(u-.18+k*.09,-.47,.12,.014,.29,.016,dark)
 for j in range(2,n,3):boxloc(j*pitch,-.006,h/2,.017,.02,h-.3,dark)
 global active_entry_edge
 active_entry_edge=ei
 if ei==dooridx and (name in ['2S Teaching building south','University Library','E1 East Building 1','E2 East Building 2']):entrance_portico(mx,boxloc,point,b,length,h,p['kind'])
 if name in ['E1 East Building 1','E2 East Building 2'] and ei==dooridx and length>25:
  # Stair/service strip and compact balconies visible in the east 1 photograph.
  u=length*.57
  for f in range(1,b['floors']):
   z=f*fh+.35;boxloc(u,-.67,z,1.6,1.40,.16,brown)
   for x in [-.76,.76]:boxloc(u+x,-.65,z+.50,.09,1.35,1.0,brown)
   rail(mx,point,u-.78,u+.78,-1.31,z+.10)
  for k in range(int(length/3)):
   u=(k+.5)*length/int(length/3);boxloc(u,-.61,h-.13,.12,1.25,.23,concrete)
  tally(b,'balconies',b['floors']-1)
 if b['style']=='lab15':
  for f in range(1,b['floors']):boxloc(length/2,-.12,f*fh-.22,length,.16,.05,dark)
 if b['style']=='heritage':
  for j in range(int(length/.18)):
   boxloc((j+.5)*length/int(length/.18),-.032,h*.24,.018,.02,h*.45,dark)
  for j in range(int(length/.45)):
   boxloc((j+.5)*length/int(length/.45),-.40,h-.02,.09,.85,.14,timber)
  tally(b,'timber wall and eaves joinery')
 if b['style'] in ['shed','industrial'] and ei==dooridx and length>6:
  # Small stores retain modest loading doors and ventilation, not office details.
  u=length*.23;ww=min(2.2,length*.20)
  boxloc(u,-.06,1.35,ww,.08,2.5,grey)
  for j in range(17):boxloc(u,-.11,.20+j*.14,ww,.025,.025,frames)
  boxloc(u,-.15,.40,.25,.06,.045,dark)
  tally(b,'service roller shutter')
 tally(b,'drainage and facade joints')

def inside_footprint(x,y,p):
 yes=False
 for a,c in zip(p,p[1:]+p[:1]):
  if (a[1]>y)!=(c[1]>y) and x<(c[0]-a[0])*(y-a[1])/(c[1]-a[1])+a[0]:yes=not yes
 return yes

def roof_detail(mx,b,pts,h):
 if b['style'] in ['heritage','gym','shed','industrial']:return
 # Service equipment lies on the mapped roof; arrangement is explicitly inferred.
 cx,cy=b['representative'];accepted=[]
 for dx,dy in [(5,0),(-5,0),(0,5),(0,-5),(6,5),(-6,-5)]:
  x,y=cx+dx,cy+dy
  if all(inside_footprint(x+xx,y+yy,pts) for xx in [-1.4,1.4] for yy in [-1.1,1.1]):accepted.append((x,y))
 for x,y in accepted[:3]:
  mx.box((x,y,h+.08),(2.4,1.7,.24),concrete)
  mx.box((x,y,h+.56),(2.1,1.45,.74),cream)
  for xx in [-.52,.52]:
   mx.beam((x+xx,y,h+.94),(x+xx,y,h+.98),.37,grey,16)
   for k in range(7):mx.box((x+xx-.27+k*.09,y,h+1.005),(.013,.56,.014),frames)
  for z in range(8):mx.box((x,y-.737,h+.25+z*.07),(1.95,.022,.022),grey)
  mx.box((x,y+.80,h+.25),(1.7,.13,.14),grey)
 # Perimeter flashings, drains and joint seams are independent of cosmetic texture.
 for a,c in zip(pts,pts[1:]+pts[:1]):
  length=math.dist(a,c)
  if length<.2:continue
  for j in range(max(1,int(length/1.2))):
   t=(j+.5)/max(1,int(length/1.2));x=a[0]*(1-t)+c[0]*t;y=a[1]*(1-t)+c[1]*t
   mx.box((x,y,h+.155),(.025,.47,.016),dark,math.atan2(c[1]-a[1],c[0]-a[0]))
 tally(b,'roof service units',len(accepted[:3]));tally(b,'roof flashing joints')

def facade_frame(mx,a,c):
 theta=math.atan2(c[1]-a[1],c[0]-a[0]);cs=math.cos(theta);sn=math.sin(theta)
 def boxloc(u,v,z,w,d,hh,mat):mx.box((a[0]+u*cs-v*sn,a[1]+u*sn+v*cs,z),(w,d,hh),mat,theta)
 def point(u,v,z):return (a[0]+u*cs-v*sn,a[1]+u*sn+v*cs,z)
 return boxloc,point

def building_sign(b,ob):
 # English model identification plaques; the exact real signage is not asserted.
 pts=b['points'];pts=pts[:-1] if pts[0]==pts[-1] else pts
 if signed_area(pts)<0:pts=pts[::-1]
 edges=list(zip(pts,pts[1:]+pts[:1]));edges=[(a,c) for a,c in edges if c[0]>a[0] and abs(c[0]-a[0])>abs(c[1]-a[1])] or edges
 a,c=max(edges,key=lambda ac:math.dist(*ac));ln=math.dist(a,c)
 if ln<4:return
 font=bpy.data.curves.new(b['name']+' identification','FONT');font.body=b['name'];font.size=min(.20,ln*.007);font.extrude=.0015;font.align_x='CENTER'
 o=bpy.data.objects.new(b['name']+' | nameplate lettering',font);ob.users_collection[0].objects.link(o)
 o.location=((a[0]+c[0])/2,(a[1]+c[1])/2-.22,3.0);o.rotation_euler=(math.pi/2,0,math.atan2(c[1]-a[1],c[0]-a[0]));font.materials.append(white);o['belongs_to_building']=b['name']

def write_detail_catalog():
 report={'version':4,'scope':'Matsugasaki east and west','profiles':profiles,'generated_components':detail_counts,'limitations':'Observed components do not establish exact dimensions, quantities or every facade. Roof-service layout and unidentified buildings remain inferred.'}
 (R/'data'/'building-details.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
