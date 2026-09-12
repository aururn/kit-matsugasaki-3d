"""Photo-observed gates and tower. Map coordinates use the inherited OSM origin.
Gate nodes are OSM positions; other locations and all unmeasured dimensions are estimates.
"""
accesscol=collection('09 | 校門・大学の塔・出入口 - Surveyed access')
gate_stone=material('Gate weathered granite',(.48,.49,.45),.88)
gate_metal=material('Gate dark green bronze metal',(.09,.14,.12),.38,.65)
gate_tiles=masonry('Gate golden scratch tiles',(.38,.22,.105),(.42,.25,.13))
gate_glow=material('Gate lantern frosted glass',(.67,.71,.60),.25)
gate_font=bpy.data.fonts.load(str(R/'assets/fonts/NotoSansCJKjp-Regular.otf'))

def frame(mx,x,y,theta):
 cs,sn=math.cos(theta),math.sin(theta)
 def pt(u,v,z):return (x+u*cs-v*sn,y+u*sn+v*cs,z)
 def box(u,v,z,w,d,h,mat):mx.box(pt(u,v,z),(w,d,h),mat,theta)
 return pt,box

def inscription(name,text,pt,u,v,z,size,theta,mat=gate_metal):
 f=bpy.data.curves.new(name,'FONT');f.body=text;f.font=gate_font;f.size=size;f.extrude=.003;f.align_x='CENTER'
 ob=bpy.data.objects.new(name,f);accesscol.objects.link(ob);ob.location=pt(u,v,z);ob.rotation_euler=(math.pi/2,0,theta);f.materials.append(mat);return ob

def lattice(mx,pt,hinge,width,height,opened=0,diamonds=True):
 # A hinged gate leaf with true holes; diagonal rods are clipped to its rectangle.
 cs,sn=math.cos(opened),math.sin(opened)
 def q(u,z):return pt(hinge+u*cs,u*sn,z)
 for z in [.17,.47,height]:mx.beam(q(0,z),q(width,z),.035,gate_metal,6)
 for u in [0,width]:mx.beam(q(u,.12),q(u,height),.04,gate_metal,6)
 if diamonds:
  low=.49;top=height-.08;slope=1.45
  for sign in [-1,1]:
   for j in range(-20,32):
    intercept=j*.52;hits=[]
    for u in [0,width]:
     z=sign*slope*u+intercept
     if low<=z<=top:hits.append((u,z))
    for z in [low,top]:
     u=(z-intercept)/(sign*slope)
     if 0<=u<=width:hits.append((u,z))
    if len(hits)>=2:mx.beam(q(*hits[0]),q(*hits[1]),.013,gate_metal,5)
 else:
  for j in range(1,max(2,int(width/.14))):
   u=j*width/max(2,int(width/.14));mx.beam(q(u,.3),q(u,height-.05),.018,gate_metal,6)
 for u in [width*.22,width*.60]:
  for z in [.31]:mx.beam(q(u-.16,.17),q(u+.16,.46),.015,gate_metal,5);mx.beam(q(u-.16,.46),q(u+.16,.17),.015,gate_metal,5)

def lantern(mx,pt,u):
 mx.beam(pt(u,0,2.03),pt(u,0,2.34),.065,gate_metal)
 # Tapered six-sided lantern with a separate cap and metal ribs.
 for j in range(6):
  a=j*math.tau/6;b=(j+1)*math.tau/6
  pa=pt(u+.17*math.cos(a),.17*math.sin(a),2.34);pb=pt(u+.25*math.cos(a),.25*math.sin(a),2.77)
  qa=pt(u+.17*math.cos(b),.17*math.sin(b),2.34);qb=pt(u+.25*math.cos(b),.25*math.sin(b),2.77)
  mx.face([pa,qa,qb,pb],gate_glow);mx.beam(pa,pb,.022,gate_metal,5)
  mx.face([pb,qb,pt(u,0,2.92)],gate_metal)

gate_specs=[
 dict(id='central-east',name='中央東門',xy=[17.14,27.27],theta=-90,kind='brick',width=8.0,source='OSM node 12491770519; Iwasaki 2025 photo; masterplan 2025 p42'),
 dict(id='central-west',name='中央西門',xy=[-2.10,26.97],theta=90,kind='brick',width=9.0,source='OSM node 12506432003; official 2025 map; Commons NI3 photo'),
 dict(id='historic-east',name='東門・旧正門',xy=[1.28,-119.36],theta=45,kind='historic',width=5.4,source='OSM node 1345835370; Cultural Heritage Online 153575; masterplan 2025 p42'),
 dict(id='west',name='西門',xy=[-281.8,-124.0],theta=-45,kind='bars',width=7.6,source='official masterplan 2025 p42 photo and boundary map; position traced'),
 dict(id='northwest',name='西北門',xy=[-279.5,127.4],theta=-135,kind='northwest',width=4.5,source='official masterplan 2025 p42 photo and boundary map; position traced'),
 dict(id='mabashi',name='馬橋門',xy=[219.27,-15.95],theta=45,kind='bars',width=6.4,source='OSM node 12491770520; official masterplan 2025 p42 photo'),
 dict(id='central-south',name='中央南門',xy=[15.0,-25.8],theta=-90,kind='small',width=2.6,source='official masterplan 2025 p42 photo and map; position traced'),
 dict(id='central-west-cycle',name='中央西自転車用門',xy=[-1.0,42.0],theta=90,kind='small',width=2.8,source='official masterplan 2025 p42; position traced'),
]
for spec in gate_specs:
 x,y=spec['xy'];theta=math.radians(spec['theta']);kind=spec['kind'];w=spec['width']
 mx=Mesh('Gate | '+spec['name'],accesscol);pt,box=frame(mx,x,y,theta)
 box(0,0,.04,w+5,4,.08,concrete)
 if kind=='brick':
  for ss in [-1,1]:
   u=ss*(w/2+2.4);box(u,0,1.0,4.8,.95,2,gate_tiles);box(u,0,2.04,5.02,1.16,.13,gate_stone)
   box(u,0,.13,4.98,1.08,.20,gate_stone);lantern(mx,pt,u)
   # Open leaves preserve a clear pedestrian passage like the current photographs.
   lattice(mx,pt,ss*w/2,2.1,1.83,math.radians(84 if ss<0 else 96))
  box(-w/2-2.4,-.487,1.50,2.65,.03,.27,gate_metal)
  inscription(spec['name']+' 銘板','京都工芸繊維大学',pt,-w/2-2.4,-.51,1.42,.205,theta,gate_stone)
  for off in [-.75,.75]:
   u=w/2+2.35+off;box(u,-.50,1.02,1.30,.055,1.53,white)
   for zz in [.24,1.80]:box(u,-.55,zz,1.37,.075,.055,gate_metal)
   for uu in [-.66,.66]:box(u+uu,-.55,1.02,.05,.075,1.58,gate_metal)
 elif kind=='historic':
  for u in [-w/2-.34,w/2+.34,-w/2-2.2,w/2+1.8]:
   h=2.8 if abs(u)<3.5 else 2.2;box(u,0,h/2,.68,.76,h,gate_stone);box(u,0,h+.08,.83,.91,.16,gate_stone)
   for zz in [.40,.95,1.5,2.05,2.6]:
    if zz<h:box(u,-.383,zz,.68,.012,.018,grey)
  lattice(mx,pt,-w/2,2.7,2.22,math.radians(85));lattice(mx,pt,w/2,2.7,2.22,math.radians(95))
  lattice(mx,pt,-w/2-1.86,1.45,1.8,0)
  # A vertical bronze plaque on the historic main pier.
  box(w/2+.34,-.397,1.74,.23,.035,1.35,gate_metal)
  inscription('Historic east gate plaque','京\n都\n工\n芸\n繊\n維\n大\n学',pt,w/2+.34,-.423,2.25,.145,theta,gate_stone)
 elif kind=='small':
  for ss in [-1,1]:box(ss*(w/2+.18),0,1.08,.36,.4,2.16,gate_stone)
  for ss in [-1,1]:lattice(mx,pt,ss*w/2,1.2,1.55,math.radians(85 if ss<0 else 95),False)
 else:
  for ss in [-1,1]:
   box(ss*(w/2+.32),0,1.22,.64,.70,2.44,gate_stone)
   box(ss*(w/2+2.1),0,.64,3,.35,1.28,concrete)
   lattice(mx,pt,ss*w/2,w/2,1.95,math.radians(82 if ss<0 else 98),False)
  if kind=='northwest':
   # Curved railings and a gradual access ramp seen in the official gate photograph.
   for ss in [-1,1]:
    prev=None
    for j in range(25):
     a=j/24*math.pi/2;u=ss*(2.7+1.1*math.sin(a));v=.8+3.6*(1-math.cos(a));z=.91
     if prev:mx.beam(prev,pt(u,v,z),.032,frames)
     if j%4==0:mx.beam(pt(u,v,.1),pt(u,v,z),.023,frames)
     prev=pt(u,v,z)
   mx.face([pt(-2.5,.3,.04),pt(2.5,.3,.04),pt(3.5,4.5,.18),pt(-3.5,4.5,.18)],concrete)
 ob=mx.finish();ob['access_id']=spec['id'];ob['source']=spec['source'];ob['location_accuracy']='OSM gate node where available; otherwise plan trace. Dimensions estimated except historic gate 5.4 m clear span.'
 ob['survey_center_xy']=spec['xy'];ob['clear_width_m']=w

# Historic pentagonal guardroom, separately editable, with tile piers and actual windows.
mx=Mesh('Gatehouse | 東門・旧門衛所',accesscol);pt,box=frame(mx,1.28,-119.36,math.pi/4)
outline=[(-11.0,.6),(-6.4,.6),(-5.2,1.8),(-5.2,5.9),(-11.0,5.9)];h=3.18
for i,(a,c) in enumerate(zip(outline,outline[1:]+outline[:1])):
 wa,wb=pt(*a,0),pt(*c,0);wall,pnt=facade_frame(mx,wa[:2],wb[:2]);ln=math.dist(a,c);ww=min(1.65,ln*.57)
 if i in [0,1,2]:
  for ss in [-1,1]:wall(ln/2+ss*(ww/2+(ln-ww)/4),.13,h/2,(ln-ww)/2,.26,h,gate_tiles)
  low=.12 if i==1 else 1.08
  wall(ln/2,.13,low/2,ww,.26,low,gate_tiles);wall(ln/2,.13,2.87,ww,.26,.62,gate_tiles)
  wall(ln/2,.08,(low+2.6)/2,ww,.016,2.6-low,glass)
  for u in [ln/2-ww/2,ln/2,ln/2+ww/2]:wall(u,-.025,(low+2.6)/2,.055,.09,2.6-low,frames)
  for z in [low,1.86,2.6]:wall(ln/2,-.025,z,ww,.09,.045,frames)
 else:wall(ln/2,.13,h/2,ln,.26,h,gate_tiles)
 wall(ln/2,-.13,3.27,ln+.30,.95,.20,concrete)
mx.polygon([pt(*v,0)[:2] for v in outline],3.32,roof)
ob=mx.finish();ob['access_id']='historic-guardhouse';ob['source']='Cultural Heritage Online 153575: pentagonal RC guardroom, 30 m2; KIT 2025 photograph';ob['dimensions']='plan proportions estimated from published photographs; no measured drawing'

# Small modern booth just north of Plaza KIT, absent from the old footprint catalog.
mx=Mesh('Gatehouse | 中央西門受付',accesscol)
mx.box((-11.2,18.8,1.5),(3.6,3.2,3.0),cream);mx.box((-11.2,18.8,3.10),(4.1,3.7,.2),grey)
for yy in [17.7,19.3]:
 mx.box((-9.375,yy,1.9),(.03,1.3,1.1),glass)
 for z in [1.33,2.47]:mx.box((-9.35,yy,z),(.09,1.35,.06),frames)
ob=mx.finish();ob['access_id']='central-west-booth';ob['source']='KIT EMC 2023 access map points to reception at the north end of Plaza KIT; size estimated'

# Move the university tower into the first planted island beyond the gate.
# Position is a plan/photo registration estimate (~5 m), not a surveyed monument node.
tx,ty=47.0,27.3;th=17.0;theta=-math.pi/2
mx=Mesh('Monument | 大学の塔「時を越えて」',accesscol);pt,box=frame(mx,tx,ty,theta)
box(0,0,.14,2.8,1.7,.28,gate_stone)
colors=[(.16,.025,.30),(.035,.09,.48),(.025,.36,.32),(.30,.62,.025),(.9,.67,.015),(.92,.16,.012),(.55,.018,.06)]
for j in range(64):
 u=j/63*6;k=min(5,int(u));f=u-k;color=tuple(colors[k][q]*(1-f)+colors[k+1][q]*f for q in range(3));mat=material('Tower enamel band %02d'%j,color,.36,.12)
 z=.34+(j+.5)*(th-.34)/64
 for xx in [-.48,.48]:
  for vv in [-.315,.315]:box(xx,vv,z,.83,.055,(th-.34)/64-.013,mat)
for u in [-.99,0,.99]:box(u,0,th/2+.17,.075,.69,th-.34,white)
# Curved outer white shells have horizontal panel joints, as in the university photo.
for ss in [-1,1]:
 for j in range(32):
  z0=.33+j*(th-.33)/32;z1=z0+(th-.33)/32-.015
  for k in range(16):
   a=-math.pi/2+k*math.pi/16;b=-math.pi/2+(k+1)*math.pi/16
   u0=ss*(.98+.26*math.cos(a));v0=.34*math.sin(a);u1=ss*(.98+.26*math.cos(b));v1=.34*math.sin(b)
   mx.face([pt(u0,v0,z0),pt(u1,v1,z0),pt(u1,v1,z1),pt(u0,v0,z1)],white)
box(0,0,th+.03,2.04,.70,.08,white)
ob=mx.finish();ob['access_id']='university-tower';ob['survey_center_xy']=[tx,ty];ob['source']='University campus_tou.jpg, Iwasaki 2025 gate photo, official 2025/2019 site plans';ob['accuracy']='position photo/map estimate ±5 m; height and cross-section estimated; former v4 position (24,23) replaced';ob['estimated_height_m']=th

# An approach forecourt connects both central gates across the public street.
site.box((7.4,27.1,.066),(19.4,9,.034),roadmat)
for j in range(8):site.box((7.4,23.7+j*.90,.093),(10.0,.43,.022),paint)
site.box((29.5,27.3,.08),(19,13,.055),concrete)
island=[(38.7,20.2),(58.0,20.2),(61.3,23.5),(61.3,30.7),(58,34.0),(39,34),(36.5,31),(36.5,23)]
site.polygon(island,.14,earth)
for a,c in zip(island,island[1:]+island[:1]):site.beam((*a,.18),(*c,.18),.14,gate_stone,6)
# Low shrubs leave the paired colour panels visible from the street.
rng=random.Random(501)
for i in range(44):
 x=rng.uniform(38.6,59);y=rng.uniform(21,33)
 if abs(x-tx)<1.6 and abs(y-ty)<2:continue
 for j in range(14):
  a=rng.random()*math.tau;z=rng.uniform(.28,.95);c=Vector((x+math.cos(a)*.8,y+math.sin(a)*.65,z));ax=Vector((.22,0,.12));by=Vector((0,.18,0))
  site.face([c-ax,c+by,c+ax,c-by],leaves[i%4])
# Low removable barriers seen in the 2025 plan photograph, separated by gaps.
mx=Mesh('Forecourt | Low removable bicycle barriers',accesscol)
for yy in [24.8,29.8]:
 mx.box((31.0,yy,.30),(.12,3.6,.44),gate_metal)
 for off in [-1.5,1.5]:mx.box((31.0,yy+off,.08),(.70,.30,.13),gate_metal)
mx.finish()

# Boundary fences make each gate part of a perimeter, with deliberate openings.
mx=Mesh('Campus perimeter | kerbs, fence rails and gate gaps',accesscol)
for poly in data['boundaries']:
 for a,c in zip(poly,poly[1:]+poly[:1]):
  ln=math.dist(a,c)
  if ln<.05:continue
  n=max(1,int(ln/2.5));pitch=ln/n
  for j in range(n):
   t0=j/n;t1=(j+1)/n;p0=(a[0]*(1-t0)+c[0]*t0,a[1]*(1-t0)+c[1]*t0);p1=(a[0]*(1-t1)+c[0]*t1,a[1]*(1-t1)+c[1]*t1);mid=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2)
   if any(math.dist(mid,g['xy'])<g['width']/2+6.0 for g in gate_specs):continue
   if 3<mid[0]<18 and 90<mid[1]<185:continue # parking driveways remain open
   ang=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
   mx.box((*mid,.24),(pitch,.25,.48),concrete,ang)
   for z in [.65,1.72]:mx.beam((*p0,z),(*p1,z),.023,gate_metal,5)
   mx.beam((*p0,.3),(*p0,1.8),.035,gate_metal,6)
   for k in range(1,10):
    u=k/10;px=p0[0]*(1-u)+p1[0]*u;py=p0[1]*(1-u)+p1[1]*u;mx.beam((px,py,.48),(px,py,1.73),.009,gate_metal,4)
mx.finish()

access_views=[
 dict(name='中央東門と大学の塔',camera=[-1,24.5,2.2],target=[47,27.3,7.0],lens=30),
 dict(name='中央両門の配置',camera=[-6,-52,67],target=[12,28,2],lens=39),
 dict(name='東門と旧門衛所',camera=[30,-156,9],target=[-3,-119,2.4],lens=43),
 dict(name='西北門',camera=[-266,109,4.0],target=[-279,127,1.0],lens=35),
 dict(name='馬橋門',camera=[245,-45,7],target=[219,-14,1.9],lens=42),
 dict(name='図書館入口',camera=[91,24,6],target=[104,53.3,2.0],lens=39),
 dict(name='東1号館の北側入口',camera=[104,29,2.4],target=[99,14,2.1],lens=28),
]
survey=dict(version=5,origin_lonlat=data['origin_lonlat'],gates=gate_specs,
 tower=dict(xy=[tx,ty],previous_xy=[24,23],height_estimated_m=th,position_uncertainty_m=5,
 evidence='official plans place it in the first east forecourt island; west-facing paired panels from official and Iwasaki photographs'),
 entrances=entry_records,custom_orientation_corrections={'museum':'east','center_hall':'north','plaza_KIT':'north'},
 limitations='Entrance side and relative offset observed in maps; metre coordinates projected onto OSM footprints. Ramp dimensions and all gate dimensions except historic gate clear span are estimates. Unlisted building entries remain inherited estimates. No claim of exhaustive field survey.')
(R/'data'/'access-survey.json').write_text(json.dumps(survey,ensure_ascii=False,indent=2),encoding='utf8')
(R/'data'/'access-views.json').write_text(json.dumps(access_views,ensure_ascii=False,indent=2),encoding='utf8')
print('V5_ACCESS_ASSEMBLED',len(gate_specs),'gates',len(entry_records),'mapped entries',flush=True)
