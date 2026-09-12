"""KIT Matsugasaki east/west campus. Public footprints + photo-informed exteriors."""
import bpy, math, json, random, os, sys
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
os.environ['OPTIX_CACHE_PATH']=str(R/'build'/'cache')
bpy.ops.wm.open_mainfile(filepath=str(R/'build'/'kit_building_3_v3.blend'))
s=bpy.context.scene
data=json.loads((R/'data'/'campus-catalog.json').read_text(encoding='utf8'))
random.seed(724)

# Retain detailed historic model, remove its oversized stand-alone ground/background.
for o in list(bpy.data.objects):
 if o.name.startswith('Continuous asphalt ground') or any(c.name.startswith('F ') for c in o.users_collection):bpy.data.objects.remove(o,do_unlink=True)
oldcols=list(s.collection.children)
historic=bpy.data.collections.new('01 | 3号館 - Detailed historic building');s.collection.children.link(historic)
for c in oldcols:s.collection.children.unlink(c);historic.children.link(c)
scale=67.085/59.793158059900534
angle=math.radians(92.324)
T=Matrix.Translation(Vector((-31.56,-71.875,.05)))@Matrix.Rotation(angle,4,'Z')@Matrix.Diagonal((scale,scale,scale,1))
for o in list(historic.all_objects):o.matrix_world=T@o.matrix_world
def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
buildcols=collection('02 | 西部構内 - West campus buildings')
eastcols=collection('03 | 東部構内 - East campus buildings')
sitecol=collection('04 | Roads, gates, courts, grounds')
treecol=collection('05 | Campus trees and planting')
labels=collection('06 | Building labels - optional');labels.hide_render=True;labels.hide_viewport=True
camcol=collection('07 | Campus cameras')

def material(name,color,rough=.65,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
def masonry(name,a,b):
 m=material(name,a,.8);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 uv=n.new('ShaderNodeTexCoord');brick=n.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.23;brick.inputs['Row Height'].default_value=.075
 brick.inputs['Color1'].default_value=(*a,1);brick.inputs['Color2'].default_value=(*b,1);brick.inputs['Mortar'].default_value=(.2,.2,.18,1);brick.inputs['Mortar Size'].default_value=.002
 l.new(uv.outputs['UV'],brick.inputs[0]);l.new(brick.outputs['Color'],p.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006;bump.inputs['Strength'].default_value=.3;l.new(brick.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal']);return m
red=masonry('Campus red brown small ceramic tiles',(.28,.12,.07),(.305,.139,.083))
brown=masonry('Campus dark brown ceramic tiles',(.22,.14,.105),(.24,.16,.12))
warm=masonry('Campus pale buff ceramic tiles',(.44,.34,.245),(.47,.37,.27))
cream=material('Campus warm painted concrete',(.62,.61,.54),.86)
white=material('Campus white metal cladding',(.74,.76,.72),.48)
grey=material('Campus grey metal roof',(.16,.19,.19),.6,.2)
roof=material('Campus roof waterproofing',(.25,.27,.26),.93)
dark=material('Campus dark interior recess',(.045,.055,.05),.9)
frames=material('Campus anodised aluminium',(.32,.36,.35),.32,.5)
glass=material('Campus glazing',(.56,.66,.69),.09,0)
glass.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.85
glass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.45
glasses=[glass,material('Campus shaded glass',(.105,.15,.17),.22,.35),material('Campus pale blind glazing',(.29,.34,.33),.25,.2)]
timber=material('Dark stained timber',(.12,.06,.028),.78)
concrete=material('Campus stone kerbs and paving',(.42,.44,.41),.89)
pathmat=material('Campus pedestrian paving',(.39,.34,.28),.92)
roadmat=material('Campus asphalt',(.115,.13,.13),.95)
earth=material('Ground sand',(.44,.35,.23),.98)
grass=material('Campus lawn',(.17,.22,.085),.97)
green=material('Tennis court green',(.09,.22,.15),.9)
water=material('Pool water',(.045,.35,.47),.12,.2)
paint=material('White line markings',(.82,.82,.70),.8)
bark=material('Tree bark',(.12,.078,.04),.92)
leaves=[material('Campus foliage '+str(i),c,.83) for i,c in enumerate([(.08,.16,.035),(.16,.23,.065),(.12,.20,.035),(.19,.26,.09)])]
brickhistoric=bpy.data.materials.get('01 Scratched ochre ceramic tile | metric running bond')

class Mesh:
 def __init__(self,name,col):self.name=name;self.col=col;self.v=[];self.f=[];self.mi=[];self.mats=[]
 def face(self,pts,mat):
  if mat not in self.mats:self.mats.append(mat)
  idx=len(self.v);self.v.extend(pts);self.f.append(tuple(range(idx,idx+len(pts))));self.mi.append(self.mats.index(mat))
 def box(self,loc,dims,mat,angle=0):
  x,y,z=[v/2 for v in dims];cs=math.cos(angle);sn=math.sin(angle)
  pts=[(loc[0]+a*cs-b*sn,loc[1]+a*sn+b*cs,loc[2]+c) for a,b,c in [(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]]
  for f in [(2,6,4,0),(5,7,3,1),(4,5,1,0),(3,7,6,2),(1,3,2,0),(6,7,5,4)]:self.face([pts[i] for i in f],mat)
 def beam(self,a,b,r,mat,sides=8):
  a=Vector(a);b=Vector(b);axis=(b-a).normalized();u=axis.cross(Vector((0,0,1)))
  if u.length<.1:u=axis.cross(Vector((0,1,0)))
  u.normalize();v=axis.cross(u)
  pa=[a+r*(math.cos(t*math.tau/sides)*u+math.sin(t*math.tau/sides)*v) for t in range(sides)]
  pb=[b+(p-a) for p in pa]
  self.face(pa[::-1],mat);self.face(pb,mat)
  for i in range(sides):j=(i+1)%sides;self.face([pa[i],pa[j],pb[j],pb[i]],mat)
 def polygon(self,pts,z,mat):
  vs=[Vector((p[0],p[1],z)) for p in pts]
  for tri in tessellate_polygon([vs]):self.face([vs[i] for i in tri] if isinstance(tri[0],int) else tri,mat)
 def finish(self):
  me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
  for m in self.mats:me.materials.append(m)
  for p,i in zip(me.polygons,self.mi):p.material_index=i
  uv=me.uv_layers.new(name='Metric facade projection')
  for p in me.polygons:
   axis=max(range(3),key=lambda k:abs(p.normal[k]))
   for li in p.loop_indices:
    v=me.vertices[me.loops[li].vertex_index].co
    uv.data[li].uv=(v.y,v.z) if axis==0 else (v.x,v.z) if axis==1 else (v.x,v.y)
  o=bpy.data.objects.new(self.name,me);self.col.objects.link(o);return o

def signed_area(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def label(name,loc,size=2):
 font=bpy.data.curves.new(name,'FONT');font.body=name;font.size=size;font.align_x='CENTER';font.extrude=.005
 o=bpy.data.objects.new(name,font);labels.objects.link(o);o.location=loc;return o

exec((R/'scripts'/'architectural_details.py').read_text(encoding='utf8'))
exec((R/'scripts'/'access_details.py').read_text(encoding='utf8'))

def building(b):
 name=b['name'];style=b['style'];pts=b['points'];h=b['height'];floors=b['floors']
 if pts[0]==pts[-1]:pts=pts[:-1]
 if signed_area(pts)<0:pts=pts[::-1]
 mx=Mesh(name,eastcols if b['representative'][0]>0 else buildcols)
 m={'brown':brown,'eastlab':brown,'lab15':warm,'library':brown,'building1':red,'museum':brown,'lab':warm,'research13':warm,'cream':cream,'kithouse':brown,'hall60':white,'heritage':cream,'historic_extension':brickhistoric,'industrial':cream,'shed':cream,'dlab':white,'plaza':grey,'pavilion':white,'gym':cream,'auditorium':warm}.get(style,cream)
 spacing=4.1 if style not in ['library','building1','brown','eastlab'] else 5.3
 if style in ['hall60','dlab','kithouse','plaza','research13']:spacing=2.5
 spacing=profiles[name]['spacing']
 x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
 edges=list(zip(pts,pts[1:]+pts[:1]));lengths=[math.dist(a,b) for a,b in edges]
 # Entrance on a major southern edge, so access faces pedestrian routes.
 candidates=[i for i,(a,b) in enumerate(edges) if lengths[i]>5 and abs(b[0]-a[0])>abs(b[1]-a[1]) and b[0]>a[0]]
 mapped=map_entries(b,edges)
 dooridx=next((i for i in mapped), max(candidates,key=lambda i:lengths[i]) if candidates else max(range(len(edges)),key=lambda i:lengths[i]))
 for ei,(a,c) in enumerate(edges):
  length=lengths[ei]
  if length<.02:continue
  theta=math.atan2(c[1]-a[1],c[0]-a[0]);cs=math.cos(theta);sn=math.sin(theta)
  def boxloc(u,v,z,w,d,hh,mat):mx.box((a[0]+u*cs-v*sn,a[1]+u*sn+v*cs,z),(w,d,hh),mat,theta)
  def point(u,v,z):return (a[0]+u*cs-v*sn,a[1]+u*sn+v*cs,z)
  n=max(1,int(length/spacing));pitch=length/n
  if (length<3.5 and ei not in mapped) or style=='auditorium':
   boxloc(length/2,.16,h/2,length,.32,h,m)
  else:
   for f in range(floors):
    fh=(h-.6)/floors;floor=f*fh
    wallmat=timber if style=='heritage' and f==0 else m
    basepitch=length/n
    cells=entry_cells(length,n,mapped.get(ei,[])) if f==0 and name in access_manifest else [((j+.5)*basepitch,basepitch,None) for j in range(n)]
    for j,(u,pitch,entry) in enumerate(cells):
     door=f==0 and (entry is not None if name in access_manifest else ei==dooridx and j==n//2)
     if pitch<.65:
      boxloc(u,.16,floor+fh/2,pitch,.32,fh,wallmat);continue
     ww=min(pitch*.72,4.1);low=floor+1.04;high=floor+min(fh-.46,3.0)
     if style=='lab15':ww=min(1.35,pitch*.45) if f else pitch*.75;low=floor+1.0;high=floor+fh-.45
     if style=='eastlab':ww=pitch-.35;low=floor+1.30;high=floor+fh-.60
     if style in ['hall60','dlab','kithouse','plaza','research13']:ww=pitch-.18;low=floor+.32;high=floor+fh-.23
     if style in ['shed','industrial']:low=floor+1.7;high=min(h-.5,low+.8)
     if style=='gym':low=h-3.1;high=h-1.5
     if name=='University Library':ww=min(pitch-.55,4.8);low=floor+.85;high=floor+fh-.35
     if name.startswith('2S '):ww=min(pitch*.65,3.0);low=floor+1.0;high=floor+fh-.55
     if door:ww=min(entry.get('width',2.6) if entry else 2.45,pitch-.18);low=.12;high=min(2.65,fh-.12)
     if name in ['University Hall','1 Main teaching building'] and ei==dooridx and abs(u-primary_entry_u(b,ei,length))<7 and f<(2 if name=='University Hall' else 1):
      boxloc(u-pitch/2+.3,.28,floor+fh/2,.60,.75,fh,m)
      boxloc(u,.55,floor+fh-.2,pitch,1.1,.40,concrete)
      boxloc(u,3.5,floor+fh/2,pitch,.025,fh-.2,glass)
      for k in range(4):boxloc(u,1.0+k*.7,floor+fh-.45,pitch,.15,.18,concrete)
      tally(b,'open arcade bay');continue
     if style=='hall60' and f==1:
      boxloc(u,.12,floor+fh/2,pitch,.3,fh,m)
      # Fine metal vertical screen around upper volume.
      for k in range(6):boxloc(u-pitch/2+(k+.5)*pitch/6,-.14,floor+fh/2,.035,.09,fh-.12,white)
      continue
     if style=='museum' and ei!=dooridx and j%3!=1:
      boxloc(u,.16,floor+fh/2,pitch,.32,fh,m);continue
     high=max(low+.35,high)
     for side in [-1,1]:boxloc(u+side*(ww/2+(pitch-ww)/4),.16,floor+fh/2,(pitch-ww)/2,.32,fh,wallmat)
     if low>floor:boxloc(u,.16,(floor+low)/2,ww,.32,low-floor,wallmat)
     boxloc(u,.16,(high+floor+fh)/2,ww,.32,max(.02,floor+fh-high),wallmat)
     # True void in masonry, glass at 10 cm and dark room backing at 0.8 m.
     if not door:boxloc(u,.84,(low+high)/2,ww,.06,high-low,dark)
     boxloc(u,.12,(low+high)/2,ww-.09,.012,high-low-.07,glass)
     for xx in [-ww/2,ww/2]:boxloc(u+xx,.06,(low+high)/2,.055,.1,high-low,frames)
     for zz in [low,high]:boxloc(u,.06,zz,ww,.10,.055,frames)
     if not door:
      boxloc(u,.035,low+(high-low)*.73,ww,.08,.04,frames)
      boxloc(u,-.10,low-.06,ww+.1,.38,.10,concrete)
      # Individual sash divisions are generated by refined_window.
      if style in ['lab15','eastlab']:
       for v in range(6):boxloc(u,-.008,high-.04-v*.045,ww-.07,.055,.02,grey)
      if style=='heritage':
       for xx in [-ww/2-.08,ww/2+.08]:boxloc(u+xx,-.035,(low+high)/2,.12,.18,high-low+.25,timber)
       for zz in [low-.12,high+.12]:boxloc(u,-.035,zz,ww+.28,.18,.13,timber)
       if f==0:
        for ss in [-1,1]:
         xx=u+ss*(ww/2+.23)
         boxloc(xx,-.10,(low+high)/2,.28,.10,high-low,timber)
         for zz in range(10):boxloc(xx,-.17,low+(zz+.5)*(high-low)/10,.29,.04,.045,timber)
     else:
      for xx in [-.10,.10]:boxloc(u+xx,-.055,1.25,.025,.08,.40,frames)
      boxloc(u,-.9,.075,ww+1.25,2.05,.14,concrete)
      boxloc(u,-.7,high+.35,ww+1.0,1.7,.16,grey)
      for xx in [-ww*.45,ww*.45]:mx.beam(point(u+xx,0,high-.4),point(u+xx,-1.45,high+.23),.03,frames)
     refined_window(mx,boxloc,point,b,u,ww,low,high,door,ei,j,f)
   boxloc(length/2,.16,h-.3,length,.32,.60,m)
  refined_edge(mx,boxloc,point,b,length,ei,dooridx,n,length/n,h)
  for entry in mapped.get(ei,[]):entry_approach(mx,boxloc,point,b,entry)
  # Narrow coping, foundation, shadow ledges and pipe detail.
  boxloc(length/2,.12,h+.07,length+.04,.48,.14,grey)
  for u0,u1 in foundation_segments(length,mapped.get(ei,[])):boxloc((u0+u1)/2,.08,.20,u1-u0,.40,.35,concrete)
  if style in ['lab','cream','brown','research13','lab15']:
   for f in range(1,floors):boxloc(length/2,-.055,(h-.6)/floors*f-.09,length,.16,.15,m)
  if style=='lab15':
   for zz in [h]+[(h-.6)/floors*f for f in range(1,floors)]:boxloc(length/2,-.35,zz,length,.95,.28,white)
  if style=='eastlab':boxloc(length/2,-.65,h+.06,length,1.45,.16,grey)
  if style=='heritage':
   for u in [0,length]:boxloc(u,-.04,h/2,.19,.22,h,timber)
   for zz in [h*.5,h-.10]:boxloc(length/2,-.04,zz,length,.22,.16,timber)
  if length>8:
   for u in [1.1,length-1.1]:
    mx.beam(point(u,-.14,.2),point(u,-.14,h-.25),.045,grey)
    for z in [2,h*.55,h-.6]:boxloc(u,-.10,z,.18,.17,.025,frames)
  if style in ['lab','brown'] and length>18:
   # Service AC condensers; keep them out of opening centres.
   for j in range(1,n,3):
    if any(abs(j*pitch-e['u'])<e['width']/2+1 for e in mapped.get(ei,[])):continue
    boxloc(j*pitch,-.38,1.0,.78,.60,.58,cream)
    for z in [.83,.95,1.07,1.19]:boxloc(j*pitch,-.69,z,.66,.02,.025,frames)
  if style in ['brown','lab'] and length>25 and ei%3==0:
   # Visible seismic frames, a common distinctive feature documented by KIT.
   for j in range(0,n-1,2):
    u=j*pitch+.3;v=min(length-.3,(j+2)*pitch-.3)
    for f in range(min(3,floors)):
     if f==0 and mapped.get(ei):continue
     z0=f*(h-.6)/floors+.4;z1=(f+1)*(h-.6)/floors-.35
     mx.beam(point(u,-.72,z0),point(v,-.72,z1),.12,concrete)
     mx.beam(point(u,-.72,z1),point(v,-.72,z0),.12,concrete)
 mx.polygon(pts,h-.10,roof)
 cx,cy=b['representative']
 if style not in ['shed','heritage','gym','auditorium','hall60']:
  mx.box((cx,cy,h+.65),(min(4,x1-x0-1),min(3,y1-y0-1),1.5),cream)
  mx.box((cx,cy,h+1.45),(min(4.2,x1-x0-.8),min(3.2,y1-y0-.8),.12),grey)
  for dx in [-1,1]:mx.box((cx+dx*.9,cy,h+1.65),(.5,.6,.3),grey)
 if style=='building1':stair_tower(mx,b,x1,y0,h)
 if style in ['gym','heritage','industrial']:
  ridge=h+(3.4 if style=='gym' else 2.1)
  roofmat=grey
  mx.face([(x0-.6,y0-.6,h),(x1+.6,y0-.6,h),(x1+.6,(y0+y1)/2,ridge),(x0-.6,(y0+y1)/2,ridge)],roofmat)
  mx.face([(x0-.6,(y0+y1)/2,ridge),(x1+.6,(y0+y1)/2,ridge),(x1+.6,y1+.6,h),(x0-.6,y1+.6,h)],roofmat)
  for xx in [x0,x1]:mx.face([(xx,y0,h),(xx,y1,h),(xx,(y0+y1)/2,ridge)],m)
  if style=='heritage':
   for xx in [x0,x1]:
    for yy in [y0,y1]:mx.box((xx,yy,h/2),(.19,.19,h),timber)
   for z in [h*.5,h-.15]:
    mx.box(((x0+x1)/2,y0-.03,z),(x1-x0,.18,.18),timber);mx.box(((x0+x1)/2,y1+.03,z),(x1-x0,.18,.18),timber)
 if style=='kithouse':
  for xx in [x0+.4+i*.47 for i in range(int((x1-x0)/.47))]:
   mx.box((xx,y0-.30,h*.74),(.20,.16,h*.44),warm)
   mx.box((xx,y1+.30,h*.74),(.20,.16,h*.44),warm)
  mx.box(((x0+x1)/2,y0-1.8,h*.5),(x1-x0+1,3.8,.15),concrete)
  for xx in range(int(x0)+1,int(x1),5):mx.beam((xx,y0-3.1,0),(xx,y0-3.1,h*.5),.07,white)
 if style=='hall60':mx.box((x0+4,y0+2,h+2.0),(.65,1.0,6.0),grey)
 if style=='auditorium':
  # Broad stepped roof plane, with glazed entrance lobby.
  mx.box((cx,cy,h+.35),(min(24,x1-x0-2),min(17,y1-y0-2),.8),grey)
  mx.box(((x0+x1)/2,y0-.22,2.05),(min(18,x1-x0-2),.15,3.8),glass)
  for xx in range(int(x0+1),int(x1-1),2):mx.box((xx,y0-.32,2.05),(.09,.14,3.8),frames)
 if style=='museum':
  mx.box((cx,y0-.7,h-1.8),(7.0,1.8,2.7),glass)
  for xx in [-3.5,0,3.5]:mx.box((cx+xx,y0-1.64,h-1.8),(.10,.12,2.7),frames)
 roof_detail(mx,b,pts,h)
 if name=='University Hall':
  a,c=edges[dooridx];wall,pnt=facade_frame(mx,a,c);ln=math.dist(a,c);su=primary_entry_u(b,dooridx,ln);rise=(h-.6)/floors
  for j in range(19):
   z=(j+1)*rise/19;wall(su,-7.22+(j+.5)*.38,z/2,8,.39,z,red)
  for side in [-1,1]:
   mx.beam(pnt(su+side*3.95,-7.15,.95),pnt(su+side*3.95,-.05,rise+.95),.035,frames)
   for j in range(0,19,3):
    v=-7.22+(j+.5)*.38;z=(j+1)*rise/19;mx.beam(pnt(su+side*3.95,v,z),pnt(su+side*3.95,v,z+.95),.025,frames)
  for ei,(a,c) in enumerate(edges):
   wall,pnt=facade_frame(mx,a,c);ln=math.dist(a,c);n=max(1,int(ln/spacing));pitch=ln/n
   # Tile bands remain on masonry piers and the upper spandrel, never across voids.
   wall(ln/2,-.018,2*rise+.25,ln,.025,.10,white)
   for j in range(n+1):
    for z in [1.0,2.4,4.8,6.1,9.1]:wall(j*pitch,-.018,z,.48,.026,.10,white)
  tally(b,'broad tiled entrance stair and contrasting tile bands')
 ob=mx.finish();ob['source_osm_way']=b['osm_id'] or 'official map trace';ob['building_name']=name;ob['evidence']=b['evidence'];ob['estimated_floors']=floors
 label(name,(cx,cy,h+3),1.6)
 return ob

exec((R/'scripts'/'landmarks.py').read_text(encoding='utf8'))
exec((R/'scripts'/'individual_buildings.py').read_text(encoding='utf8'))
for b in data['catalog']:
 ob=custom_landmark(b)
 if ob is None:ob=building(b)
 if isinstance(ob,bpy.types.Object):
  ob['detail_version']=5;building_sign(b,ob);custom_refinements(b,ob);correct_custom_orientation(b,ob)
write_detail_catalog()
print('Campus architecture assembled',len(data['catalog']),flush=True)

# Landscape follows geographic features and road centre lines.
site=Mesh('Campus ground, paths and sports grounds',sitecol)
site.box((-5,0,-.52),(680,600,1),concrete)
for p in data['boundaries']:site.polygon(p,.005,pathmat)
for road in data['roads']:site.polygon(road['points'],.045,roadmat if road['kind']=='road' else concrete)
for f in data['features']:
 t=f['tags'];p=f['points']
 if 'highway' in t:continue
 kind=t.get('leisure',t.get('amenity',t.get('landuse',t.get('natural',''))))
 m={'pitch':earth,'swimming_pool':water,'parking':roadmat,'grass':grass,'wood':grass}.get(kind)
 if t.get('sport')=='tennis':m=green
 if m:site.polygon(p,.07,m)
 if kind=='pitch' and t.get('sport')!='tennis':
  # Multi-purpose ground with a football pitch and separate baseball diamond.
  xmin=min(v[0] for v in p);xmax=max(v[0] for v in p);ymin=min(v[1] for v in p);ymax=max(v[1] for v in p)
  cx=(xmin+xmax)/2;cy=(ymin+ymax)/2;hw=min(49,(xmax-xmin)*.4);hh=min(31,(ymax-ymin)*.36)
  for y in [-hh,0,hh]:site.box((cx,cy+y,.10),(hw*2,.11,.018),paint)
  for x in [-hw,hw]:
   site.box((cx+x,cy,.10),(.11,hh*2,.018),paint)
   site.beam((cx+x,cy-3.66,.1),(cx+x,cy-3.66,2.55),.05,paint);site.beam((cx+x,cy+3.66,.1),(cx+x,cy+3.66,2.55),.05,paint);site.beam((cx+x,cy-3.66,2.55),(cx+x,cy+3.66,2.55),.05,paint)
  for j in range(64):
   a=j*math.tau/64;b=(j+1)*math.tau/64;site.beam((cx+9.15*math.cos(a),cy+9.15*math.sin(a),.105),(cx+9.15*math.cos(b),cy+9.15*math.sin(b),.105),.04,paint)
 if kind=='swimming_pool':
  xmin=min(v[0] for v in p);xmax=max(v[0] for v in p);ymin=min(v[1] for v in p);ymax=max(v[1] for v in p)
  for y in [ymin,ymax]:site.box(((xmin+xmax)/2,y,.11),(xmax-xmin+.8,.55,.2),concrete)
  for x in [xmin,xmax]:site.box((x,(ymin+ymax)/2,.11),(.55,ymax-ymin,.2),concrete)
  for j in range(1,6):site.beam((xmin+(xmax-xmin)*j/6,ymin,.13),(xmin+(xmax-xmin)*j/6,ymax,.13),.035,paint)
 if t.get('sport')=='tennis':
  xmin=min(v[0] for v in p);xmax=max(v[0] for v in p);ymin=min(v[1] for v in p);ymax=max(v[1] for v in p)
  for j in range(3):
   cx=xmin+(j+.5)*(xmax-xmin)/3;cy=(ymin+ymax)/2
   for xx in [-5.5,5.5]:site.box((cx+xx,cy,.09),(.065,23.7,.018),paint)
   for yy in [-11.85,11.85,-6.4,6.4]:site.box((cx,cy+yy,.09),(11,.065,.018),paint)
   site.beam((cx-6.4,cy,.05),(cx-6.4,cy,1.05),.055,frames);site.beam((cx+6.4,cy,.05),(cx+6.4,cy,1.05),.055,frames)
   for z in [.18,.38,.58,.78,.98]:site.beam((cx-6.3,cy,z),(cx+6.3,cy,z),.012,grey)
 for a,b in zip(p,p[1:]):
  if kind in ['pitch','swimming_pool']:
   ln=math.dist(a,b)
   for j in range(int(ln/4)+1):
    u=j/max(1,int(ln/4));x=a[0]*(1-u)+b[0]*u;y=a[1]*(1-u)+b[1]*u
    site.beam((x,y,.1),(x,y,3.1),.038,frames)
   for z in [.4,1.7,3.1]:site.beam((a[0],a[1],z),(b[0],b[1],z),.015,frames)
# Surveyed gates and monument are editable, separately named meshes.
exec((R/'scripts'/'site_access.py').read_text(encoding='utf8'))
# Parking stripes and modest parked vehicles on mapped parking areas.
carcolors=[material('Parked car '+str(i),c,.3,.25) for i,c in enumerate([(.55,.58,.58),(.08,.12,.17),(.7,.7,.67),(.20,.035,.025)])]
for f in data['features']:
 if f['tags'].get('amenity')!='parking':continue
 p=f['points'];xmin=min(v[0] for v in p);xmax=max(v[0] for v in p);ymin=min(v[1] for v in p);ymax=max(v[1] for v in p)
 for j in range(max(0,int((ymax-ymin)/2.7)-1)):
  yy=ymin+2+j*2.7;xx=xmin+3.0
  site.box((xx,yy-1.3,.095),(5,.07,.015),paint)
  if j%3!=0:
   site.box((xx,yy,.62),(4.3,1.72,1.1),carcolors[j%4]);site.box((xx-.1,yy,1.36),(2.4,1.55,.52),carcolors[j%4]);site.box((xx-.1,yy-.79,1.39),(2.1,.035,.35),glass);site.box((xx-.1,yy+.79,1.39),(2.1,.035,.35),glass)
   for dx in [-1.35,1.3]:
    for dy in [-.88,.88]:site.box((xx+dx,yy+dy,.35),(.60,.15,.57),dark)
# Bicycle shelters around classroom approaches.
for x,y,n in [(-13,45,7),(-122,26,8),(-212,-34,7),(53,-21,6),(10,57,5)]:
 for i in range(n+1):site.beam((x+i*1.7,y,0),(x+i*1.7,y,2.6),.04,frames)
 site.box((x+n*.85,y-1.1,2.61),(n*1.7+.7,2.9,.09),grey)
 for i in range(n):
  xx=x+i*1.7+.7
  for yy in [y-.3,y-1.35]:
   for j in range(20):
    a=j*math.tau/20;b=(j+1)*math.tau/20;site.beam((xx+.32*math.cos(a),yy,.36+.32*math.sin(a)),(xx+.32*math.cos(b),yy,.36+.32*math.sin(b)),.018,dark)
  site.beam((xx,y-1.35,.36),(xx,y-.7,.80),.018,frames);site.beam((xx,y-.7,.80),(xx,y-.3,.36),.018,frames)
site.finish()

# Fast linked tree meshes with real leaf polygons; no opaque balls.
def tree_mesh(seed):
 rng=random.Random(seed);m=Mesh('Deciduous tree asset '+str(seed),treecol)
 m.beam((0,0,0),(0,0,5.7),.16,bark)
 for i in range(12):
  a=i*2.4;end=Vector((math.cos(a)*rng.uniform(1,2.6),math.sin(a)*rng.uniform(1,2.6),rng.uniform(4.3,7.5)))
  m.beam((0,0,3.3),end,.065,bark)
  for j in range(190):
   c=end+Vector((rng.uniform(-1.4,1.4),rng.uniform(-1.4,1.4),rng.uniform(-1.1,1.1)))
   ax=Vector((rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-.5,.5))).normalized()*.16
   by=ax.cross(Vector((0,0,1))).normalized()*.075
   m.face([c-ax,c+by,c+ax,c-by],leaves[rng.randrange(4)])
 ob=m.finish();ob.hide_render=True;ob.hide_viewport=True;return ob.data
assets=[tree_mesh(i) for i in range(4)]
def inside(pt,poly):
 x,y=pt;yes=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:yes=not yes
 return yes
def near_building(x,y):
 for b in data['catalog']:
  p=b['points'];xx=[v[0] for v in p];yy=[v[1] for v in p]
  if min(xx)-3<x<max(xx)+3 and min(yy)-3<y<max(yy)+3:return True
 return -94<x<-20 and -118<y<-28
def place_tree(x,y,k):
 if near_building(x,y) or in_access_clearance(x,y):return
 if not any(inside((x,y),p) for p in data['boundaries']):return
 if any(inside((x,y),p['points']) for p in data['roads']):return
 if any(f['tags'].get('leisure') in ['pitch','swimming_pool'] and inside((x,y),f['points']) for f in data['features']):return
 o=bpy.data.objects.new('Campus tree %03d'%k,assets[k%4]);treecol.objects.link(o);o.location=(x,y,.06);v=random.uniform(.8,1.4);o.scale=(v,v,v);o.rotation_euler.z=random.random()*math.tau
k=0
for x in range(-275,230,11):
 for y in [-130,126]:place_tree(x,y,k);k+=1
for y in range(-115,170,11):
 for x in [-278,-11,14,229]:place_tree(x,y,k);k+=1
for x in range(-258,205,15):
 for y in [-33,17,39]:place_tree(x,y,k);k+=1
print('Landscape assembled',flush=True)

def camera(name,loc,target,lens=46,ortho=None):
 c=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,c);camcol.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();c.lens=lens;c.clip_end=2000
 if ortho:c.type='ORTHO';c.ortho_scale=ortho
 return o
hero=camera('Campus 01 | East and West overview',(490,-580,530),(-25,25,0),48)
west=camera('Campus 02 | West campus',(-350,-410,330),(-145,0,0),49)
east=camera('Campus 03 | East campus',(300,-320,250),(113,65,0),49)
plan=camera('Campus 04 | Geographic plan',(-25,28,800),(-25,28,0),45,610)
gate=camera('Campus 05 | Main gates',(31,-56,5),(-32,37,10),28)
food=camera('Campus 06 | KIT HOUSE',(-244,-84,19),(-218,-64,5),22)
hallcam=camera('Campus 07 | 60th Anniversary Hall',(-6,29,9),(32,-4,4.5),40)
center=camera('Campus 08 | Center Hall',(-80,-41,21),(-43,-12,6),24)
access_cameras=[camera('Access | '+v['name'],v['camera'],v['target'],v.get('lens',40)) for v in access_views]
s.camera=hero;s.render.engine='CYCLES';s.cycles.samples=96;s.cycles.use_denoising=True;s.cycles.max_bounces=7
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 s.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
except Exception:pass
s.render.resolution_x=2400;s.render.resolution_y=1700;s.render.resolution_percentage=65 if '--preview' in sys.argv else 100
s.view_settings.exposure=.3
s['Detail version']='5: mapped entrances, gates and tower; access-survey.json records evidence and estimates'
(R/'data'/'campus-catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.clip_end=2000;area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.color_type='MATERIAL'
s['Scope']='KIT Matsugasaki west and east campus, including northern heritage parcel.'
s['Evidence']='OSM geographic footprints; official KIT 2026 campus map; photo-informed prominent buildings. Heights and unseen facades estimated.'
s['Attribution']='© OpenStreetMap contributors. Geographic derived data: ODbL 1.0. Textures: Poly Haven CC0.'
for fn in ['access-survey.json','SOURCES.md','README.md']:
 t=bpy.data.texts.new('V5 | '+fn);t.write((R/('data' if fn.endswith('.json') else '.')/fn).read_text(encoding='utf8'))
txt=bpy.data.texts.new('READ ME - Campus v5');txt.write('MATSUGASAKI EAST + WEST CAMPUS\nOpen camera Campus 01 for full overview. Optional building labels in collection 06 (hidden in renders).\nAll buildings are editable meshes with named collections. Historic 3 building retains fine details.\nSource catalog is campus-catalog.json beside this file. OSM footprints matched to official map; many heights and invisible facades remain estimated.\nOSM attribution: https://www.openstreetmap.org/copyright\n')
exec((R/'scripts'/'pack_public_assets.py').read_text(encoding='utf8'));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'build'/'kit_matsugasaki_campus_v5.blend'))
views=[(hero,'campus-overview'),(west,'campus-west'),(east,'campus-east'),(plan,'campus-plan'),(gate,'campus-gates')]
views.extend([(food,'kit-house-detail'),(hallcam,'hall60-detail'),(center,'center-hall-detail')])
if '--preview' in sys.argv:views=views[:1];s.cycles.samples=32
if '--build-only' in sys.argv:views=[]
for cam,fn in views:s.camera=cam;s.render.filepath=str(R/'build'/(fn+'.png'));bpy.ops.render.render(write_still=True)
s.camera=hero
bpy.ops.wm.save_as_mainfile(filepath=str(R/'build'/'kit_matsugasaki_campus_v5.blend'))
(R/'reports'/'campus-build-info.json').write_text(json.dumps({'catalog_entries':len(data['catalog']),'objects':len(s.objects),'vertices':sum(len(o.data.vertices) for o in s.objects if o.type=='MESH'),'historic_xy_scale':scale,'scope':s['Scope']},indent=2),encoding='utf8')
print('CAMPUS_V5_BUILD_COMPLETE',flush=True)
