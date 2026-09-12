"""Per-building silhouettes and construction, based on the cited photographs."""
def finish_individual(mx,b,description):
 ob=mx.finish();ob['building_name']=b['name'];ob['source_osm_way']=b['osm_id'] or 'official map trace';ob['evidence']=description
 ob['detail_version']=4;label(b['name'],(*b['representative'],b['height']+3),1.6)
 tally(b,description);return ob

def museum_individual(b):
 mx=Mesh(b['name'],buildcols);pts=b['points'];x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts);h=b['height']
 width=x1-x0;cx=(x0+x1)/2;entry=width*.36
 # Exhibition enclosure with sparse narrow lights on the side and rear walls.
 for a,c in [((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:
  boxloc,point=facade_frame(mx,a,c);ln=math.dist(a,c);n=max(2,int(ln/5.0));pitch=ln/n
  for j in range(n):
   u=(j+.5)*pitch;ww=.45 if j%2==0 else 1.6;low=1.4 if j%2==0 else h-3.8;high=h-2.1
   for ss in [-1,1]:boxloc(u+ss*(ww/2+(pitch-ww)/4),.18,h/2,(pitch-ww)/2,.36,h,brown)
   boxloc(u,.18,low/2,ww,.36,low,brown);boxloc(u,.18,(h+high)/2,ww,.36,h-high,brown)
   boxloc(u,.22,(low+high)/2,ww-.06,.012,high-low,glass)
   for xx in [-ww/2,ww/2]:boxloc(u+xx,.025,(low+high)/2,.05,.16,high-low,frames)
   boxloc(u,-.10,high+.10,ww+.22,.45,.16,concrete)
  for u in [ln*.28,ln*.74]:boxloc(u,-.16,h/2,.48,.60,h+.25,concrete)
  boxloc(ln/2,0,h+.12,ln,.6,.18,grey)
 # The centre of the front is a real deep void, with a picture window above.
 left=(width-entry)/2
 for ss in [-1,1]:
  xx=cx+ss*(entry/2+left/2);mx.box((xx,y0+.25,h/2),(left,.50,h),brown)
  mx.box((xx,y0-.04,h+.14),(left+.05,.7,.20),grey)
  sx=cx+ss*(entry/2+left*.30)
  # Deeply inset narrow slit; use a framed recess on the already blank pier.
  mx.box((sx,y0-.018,3.7),(.34,.03,1.7),dark)
  mx.box((sx,y0-.03,3.7),(.12,.018,1.60),glass)
  mx.box((sx,y0-.10,4.61),(.58,.45,.14),concrete)
 mx.box((cx,y0+.3,h-.38),(entry,.60,.76),brown)
 for ss in [-1,1]:mx.box((cx+ss*(entry/2-.15),y0+1.6,4.05),(.30,3.4,8.1),brown)
 curtain(mx,(cx-entry/2,y0+3.2),(cx+entry/2,y0+3.2),.20,3.5,1.2,True)
 curtain(mx,(cx-entry/2,y0+3.2),(cx+entry/2,y0+3.2),4.2,7.4,1.4)
 mx.box((cx,y0+1.6,3.85),(entry,3.5,.38),concrete)
 for i in range(6):mx.box((cx-entry/2+(i+.5)*entry/6,y0+1.55,7.60),(.16,3.6,.28),grey)
 # Projected metal picture-window box, with return cheeks and sheet seams.
 z0,z1=8.0,h-.8;yy=y0-1.05
 curtain(mx,(cx-entry/2,yy),(cx+entry/2,yy),z0,z1,max(1,entry/3))
 for zz in [z0-.12,z1+.12]:mx.box((cx,yy+.40,zz),(entry+.55,1.2,.25),white)
 for ss in [-1,1]:
  mx.box((cx+ss*(entry/2+.14),yy+.40,(z0+z1)/2),(.28,1.2,z1-z0+.5),white)
  for z in [z0+.65,z0+1.3]:mx.box((cx+ss*(entry/2+.285),yy+.4,z),(.015,1.18,.014),grey)
 mx.box((cx,(y0+y1)/2,h-.10),(width,y1-y0,.2),roof)
 mx.box((cx,y0-1.9,.11),(entry+1.1,4.0,.22),concrete)
 roof_detail(mx,b,pts,h)
 return finish_individual(mx,b,'museum: deep entrance, picture-window box, slit recesses, side fins')

def plaza_individual(b):
 mx=Mesh(b['name'],buildcols);pts=b['points'];x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts);h=b['height'];cx=(x0+x1)/2
 if pts[0]==pts[-1]:pts=pts[:-1]
 if signed_area(pts)<0:pts=pts[::-1]
 mx.polygon(pts,h-.1,roof)
 for a,c in zip(pts,pts[1:]+pts[:1]):
  boxloc,point=facade_frame(mx,a,c);ln=math.dist(a,c)
  curtain(mx,a,c,.2,h-.25,1.25,True)
  n=max(1,int(ln/.22));pitch=ln/n
  # Bent mesh screen: individual rails and perforation grid, with clear entrance.
  for j in range(n):
   u=(j+.5)*pitch;front=c[0]>a[0] and abs(c[0]-a[0])>abs(c[1]-a[1]);low=3.10 if front and abs(u-ln/2)<1.55 else .25
   for du,v in [(-pitch*.4,-.18),(0,-.31),(pitch*.4,-.18)]:boxloc(u+du,v,(low+h+.25)/2,.018,.018,h+.25-low,white)
   for k in range(int((h+.25-low)/.095)):
    zz=low+k*.095;mx.beam(point(u-pitch*.4,-.18,zz),point(u,-.31,zz),.006,white,4);mx.beam(point(u,-.31,zz),point(u+pitch*.4,-.18,zz),.006,white,4)
 mx.box((cx,y0-1.5,3.12),(min(12,x1-x0),3.8,.13),white)
 for xx in [cx-4.8,cx+4.8]:mx.box((xx,y0-3,1.53),(.38,.5,3.06),concrete)
 mx.box((x0+2.2,y0-.2,1.52),(3.6,.30,3.0),concrete)
 for xx in range(5):
  for z in [1,2]:mx.beam((x0+.6+xx*.68,y0-.36,z),(x0+.6+xx*.68,y0-.37,z),.032,grey,8)
 tally(b,'folded screen bays',sum(max(1,int(math.dist(a,c)/.22)) for a,c in zip(pts,pts[1:]+pts[:1])))
 return finish_individual(mx,b,'plaza: folded perforated screen, concrete portico and thin roof')

def stair_tower(mx,b,x1,y0,h):
 tx=x1-7;ty=y0+8;zh=h+2.8;w=5.3;d=7
 # Corner glazing occupies the front and east faces; masonry closes the other two.
 mx.box((tx-w/2+.3,ty,zh/2),(.6,d,zh),red)
 mx.box((tx,ty+d/2-.3,zh/2),(w,.6,zh),red)
 for xx in [tx-w/2+.5,tx+w/2-.45]:mx.box((xx,ty-d/2+.2,zh/2),(.50,.40,zh),red)
 mx.box((tx,ty,zh-1.45),(w,d,2.9),red)
 curtain(mx,(tx-w/2+.8,ty-d/2),(tx+w/2-.3,ty-d/2),.3,h-.2,1.65)
 curtain(mx,(tx+w/2,ty-d/2+.4),(tx+w/2,ty+d/2-.5),.3,h-.2,2.0)
 for f in range(1,b['floors']):
  z=f*(h-.6)/b['floors'];mx.box((tx,ty,z),(w-.8,d-.8,.20),concrete)
  curtain(mx,(tx-w/2+.8,ty-d/2-.025),(tx+w/2-.3,ty-d/2-.025),z-.04,z+.04,4)
  # Sloping flights visible through the tower, not an opaque glass sticker.
  for i in range(12):mx.box((tx-.65,ty-2.4+i*.35,z+(i+1)*.14),(1.45,.35,.12),concrete)
 mx.box((tx,ty,zh+.08),(w+.15,d+.15,.12),grey)
 for j in range(5):mx.box((tx-.7+j*.35,ty-d/2-.022,zh-1.1),(.10,.025,.65),dark)
 tally(b,'corner-glazed stair tower with landings')

def custom_refinements(b,ob):
 mx=Mesh(b['name']+' | construction details',ob.users_collection[0]);name=b['name'];pts=b['points'];h=b['height']
 if name=='KIT HOUSE':
  # Roof glazing cap strips, end flashings and wire handrail around the open stair.
  for j in range(4):
   xa=-239.1+j*10.05;ridge=xa+10.05*.55
   mx.beam((ridge,-71.8,10.76),(ridge,-44.8,10.76),.07,white)
   for y in [-71.8,-44.8]:mx.beam((xa,y,7.57),(ridge,y,10.75),.06,white)
  for yy in [-84.8+i*.55 for i in range(22)]:
   z=.42+(yy+84.8)/11.6*3.18
   mx.beam((-220.2,yy,z),(-220.2,yy,z+1.0),.014,white)
  tally(b,'rooflight flashings and stair balusters')
 elif name=='60th Anniversary Hall':
  for x in range(19,53,3):mx.box((x,-18.412,6.0),(.012,.015,4.2),grey)
  for y in range(-15,7,3):mx.box((16.885,y,6.0),(.015,.012,4.2),grey)
  for yy in [-16,6]:mx.beam((17.0,yy,.2),(17.0,yy,3.7),.035,grey)
  for yy in [-14,-10,-6,-2,2]:mx.box((18.08,yy,2.5),(.055,3.9,.055),frames)
  tally(b,'cladding joints and lobby transoms')
 elif b['style']=='auditorium':
  x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);cx=(x0+x1)/2
  for j in range(5):mx.box((cx,y0-6.7+j*.32,.035+j*.035),(12,.38,.07),concrete)
  for x in [cx-.1,cx+.1]:mx.beam((x,y0-4.06,1.0),(x,y0-4.06,1.5),.025,frames)
  tally(b,'entry stair and door hardware')
 if mx.v:
  detail=mx.finish();detail['belongs_to_building']=name;detail['detail_version']=4

original_custom_landmark=custom_landmark
def custom_landmark(b):
 if b['style']=='museum':return museum_individual(b)
 if b['name']=='Plaza KIT':return plaza_individual(b)
 return original_custom_landmark(b)
