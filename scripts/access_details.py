"""Entrances traced from KIT's public accessibility plans, not a south-wall rule.
Side and fractional position are observations; widths, rises and hardware are estimates.
Executed by build_campus.py after architectural_details.py.
"""
access_rows = {
 '15 Teaching building':[('W',.07,'ramp')],
 '14 Teaching building':[('E',.95,'flat')],
 '16 New Materials Innovation Lab':[('N',.40,'ramp')],
 'Practice workshop':[('S',.39,'flat'),('S',.86,'flat')],
 'North lecture hall':[('S',.52,'flat')],
 'Isotope Center':[('S',.60,'flat')],
 '2N Teaching building north':[('N',.55,'flat'),('W',.55,'flat')],
 '2S Teaching building south':[('S',.53,'ramp'),('W',.62,'flat')],
 '1 Main teaching building':[('S',.51,'ramp'),('E',.72,'flat')],
 '12 Teaching building':[('N',.65,'ramp')],
 '11 Teaching building':[('E',.53,'flat'),('W',.53,'flat')],
 '13 Research building':[('E',.35,'ramp'),('E',.08,'flat'),('W',.08,'flat')],
 '10 Teaching building':[('S',.55,'ramp')],
 'Environmental Science Center':[('N',.2,'flat')],
 'Environmental laboratory annex':[('N',.7,'flat')],
 '17N North wing':[('E',.88,'ramp')],
 '17S South wing':[('E',.55,'ramp')],
 'West lecture rooms':[('E',.55,'flat')],
 '18 Teaching building':[('S',.75,'flat')],
 '19 Teaching building':[('S',.60,'ramp')],
 'West experimental building':[('E',.86,'flat')],
 '7 Teaching building':[('N',.70,'ramp')],
 '8 Teaching building':[('W',.56,'ramp'),('E',.56,'flat')],
 '9 Teaching building':[('W',.70,'flat')],
 '6 Teaching building':[('E',.65,'flat'),('S',.15,'loading')],
 '4 Teaching building west extension':[('N',.57,'flat'),('S',.73,'flat')],
 '5 Teaching building west extension':[('N',.62,'ramp')],
 'Information Infrastructure Center':[('N',.50,'ramp'),('S',.78,'flat')],
 'University Hall':[('N',.72,'stair'),('S',.35,'ramp')],
 'University Library':[('S',.28,'ramp')],
 'E3 East Building 3':[('S',.38,'ramp')],
 'E4 East Building 4':[('S',.57,'ramp')],
 'E1 East Building 1':[('N',.60,'ramp'),('N',.15,'flat')],
 'E2 East Building 2':[('N',.5,'ramp'),('E',.50,'flat')],
 'Health and Accessibility Center':[('W',.55,'ramp')],
 'Library east annex':[('E',.62,'flat')],
 'Gymnasium':[('W',.45,'ramp'),('S',.30,'flat')],
 'Martial arts and training hall':[('N',.27,'ramp'),('S',.55,'flat')],
 'East lecture room':[('W',.51,'flat')],
 'Cultural club facilities':[('W',.63,'ramp')],
 'Pool changing rooms':[('E',.60,'flat')],
 'Sports equipment store A':[('W',.5,'flat')],
 'Sports equipment store B':[('W',.5,'flat')],
 'Sports equipment store C':[('W',.5,'flat')],
 'KYOTO Design Lab':[('W',.5,'flat'),('S',.84,'flat')],
 'East gate guardhouse':[('W',.55,'flat')],
 'Kosen Kaikan':[('W',.5,'flat')],
 'KIT Club':[('N',.5,'flat')],
}
access_manifest={name:[dict(side=side,fraction=t,approach=kind,width=3.2 if kind=='loading' else 2.6,
 source='KIT masterplan 2025 p31 accessibility map; 2019 large-scale accessibility map printed p72',
 position_accuracy='facade and relative position traced; exact offset and dimensions estimated')
 for side,t,kind in rows] for name,rows in access_rows.items()}
access_manifest['6 Teaching building'][1]['source']='KIT EMC access map 2023 p2: shared 8-105 loading access at southern 6/8 junction'
mapped_entry_cache={}
entry_records=[]

def map_entries(b,edges):
 if b['name'] in mapped_entry_cache:return mapped_entry_cache[b['name']]
 entries=access_manifest.get(b['name'],[]);result={};p=b['points']
 x0=min(x for x,y in p);x1=max(x for x,y in p);y0=min(y for x,y in p);y1=max(y for x,y in p)
 for ix,e in enumerate(entries):
  side=e['side'];t=e['fraction'];target={'N':(x0+(x1-x0)*t,y1),'S':(x0+(x1-x0)*t,y0),'E':(x1,y0+(y1-y0)*t),'W':(x0,y0+(y1-y0)*t)}[side]
  normal={'N':(0,1),'S':(0,-1),'E':(1,0),'W':(-1,0)}[side];choices=[]
  for ei,(a,c) in enumerate(edges):
   ln=math.dist(a,c)
   if ln<2.9:continue
   tx,ty=(c[0]-a[0])/ln,(c[1]-a[1])/ln
   dot=ty*normal[0]-tx*normal[1]
   if dot<.55:continue
   u=max(1.45,min(ln-1.45,(target[0]-a[0])*tx+(target[1]-a[1])*ty));pt=(a[0]+tx*u,a[1]+ty*u)
   choices.append((math.dist(pt,target)+(1-dot)*8,ei,u,pt,(ty,-tx)))
  if not choices:raise ValueError('No valid entrance edge: '+b['name']+str(e))
  _,ei,u,pt,norm=min(choices)
  row=dict(e,threshold_z=(b['height']-.6)/b['floors']+.12 if e['approach']=='stair' else .12,u=u,xy=pt,normal=norm,id=b['name']+' entry '+str(ix+1),edge=ei)
  result.setdefault(ei,[]).append(row);entry_records.append(dict(building=b['name'],**row))
 mapped_entry_cache[b['name']]=result;return result

def primary_entry_u(b,ei,length):
 rows=mapped_entry_cache.get(b['name'],{}).get(ei,[])
 return rows[0]['u'] if rows else length/2

def entry_cells(length,n,entries):
 # Reserve a full structural bay around each observed door; fill the remaining wall
 # with windows. Every ground-floor door has a genuine opening in the masonry.
 pitch=length/n;intervals=[]
 for e in sorted(entries,key=lambda e:e['u']):
  half=max(1.42,e['width']/2+.24)
  intervals.append((max(0,e['u']-half),min(length,e['u']+half),e))
 cells=[];start=0
 def windows(a,c):
  if c-a<.025:return
  count=max(1,round((c-a)/pitch));w=(c-a)/count
  cells.extend((a+(j+.5)*w,w,None) for j in range(count))
 for lo,hi,e in intervals:
  if lo<start-.01:raise ValueError('Overlapping entrance bays '+e['id'])
  windows(start,lo);cells.append(((lo+hi)/2,hi-lo,e));start=hi
 windows(start,length);return cells

def foundation_segments(length,entries):
 last=0;out=[]
 for e in sorted(entries,key=lambda e:e['u']):
  lo=max(last,e['u']-e['width']/2-.03);hi=min(length,e['u']+e['width']/2+.03)
  if lo-last>.01:out.append((last,lo))
  last=hi
 if length-last>.01:out.append((last,length))
 return out

def entry_approach(mx,boxloc,point,b,e):
 u=e['u'];w=e['width']+.8;kind=e['approach']
 if kind=='ramp':
  run=3.8;rise=.14;landing={'University Library':2.4,'E1 East Building 1':3.8,'E2 East Building 2':3.8,'2S Teaching building south':3.4}.get(b['name'],1.0)
  front=-landing-run
  boxloc(u,-landing/2,.08,w,landing,.12,concrete)
  # A real wedge rising toward the threshold, with continuous handrails.
  verts=[point(u-w/2,front,.06),point(u+w/2,front,.06),point(u+w/2,-landing,rise),point(u-w/2,-landing,rise)]
  mx.face(verts,concrete)
  for ss in [-1,1]:
   for v in [front,front+run/2,-landing]:
    z=.06+(v-front)/run*.08;mx.beam(point(u+ss*w/2,v,z),point(u+ss*w/2,v,z+.86),.023,frames)
   mx.beam(point(u+ss*w/2,front,.92),point(u+ss*w/2,-landing,1.0),.033,frames)
 elif kind!='stair':boxloc(u,-1.35,.055,w,2.7,.1,concrete)
 # Detailed glazed doors inside the piloti, whose old geometry only had glass.
 if b['name'] in ['1 Main teaching building','University Hall']:
  base=e['threshold_z']-.12;z=base+2.6;boxloc(u,3.35,base+1.35,e['width'],.035,2.5,glass)
  for du in [-e['width']/2,0,e['width']/2]:boxloc(u+du,3.25,base+1.35,.065,.12,2.5,frames)
  for zz in [base+.13,z]:boxloc(u,3.25,zz,e['width'],.12,.065,frames)
  for du in [-.14,.14]:boxloc(u+du,3.16,base+1.1,.025,.07,.4,frames)
 # Source data is retained on an Empty at the threshold for Blender inspection.
 mark=bpy.data.objects.new('Entrance | '+e['id'],None);buildcols.objects.link(mark)
 mark.location=(*e['xy'],e['threshold_z']);mark.empty_display_type='PLAIN_AXES';mark.empty_display_size=.35
 mark['belongs_to_building']=b['name'];mark['source']=e['source'];mark['accuracy']=e['position_accuracy'];mark['entrance_id']=e['id']

def correct_custom_orientation(b,ob):
 # Custom facade models were previously built facing south for their study camera.
 turns={'Museum of Arts and Crafts':math.pi/2,'Center Hall and learning building':math.pi,'Plaza KIT':math.pi}
 if b['name'] in turns:
  pts=b['points'];cx=(min(p[0] for p in pts)+max(p[0] for p in pts))/2;cy=(min(p[1] for p in pts)+max(p[1] for p in pts))/2
  tr=Matrix.Translation(Vector((cx,cy,0)))@Matrix.Rotation(turns[b['name']],4,'Z')@Matrix.Translation(Vector((-cx,-cy,0)))
  for o in list(s.objects):
   if o==ob or o.get('belongs_to_building')==b['name']:o.matrix_world=tr@o.matrix_world
  ob['entrance_orientation']='Corrected to official accessibility map: '+('east' if b['name'].startswith('Museum') else 'north')
 # Keep the unverified English model labels in the optional label collection.
 for o in list(s.objects):
  if o.type=='FONT' and o.get('belongs_to_building')==b['name']:
   for c in list(o.users_collection):c.objects.unlink(o)
   labels.objects.link(o)

def in_access_clearance(x,y):
 if -14<x<39 and 17<y<39:return True
 if 30<x<70 and 18<y<35:return True
 for e in entry_records:
  p=e['xy'];n=e['normal'];dx=x-p[0];dy=y-p[1]
  if -1<dx*n[0]+dy*n[1]<6 and abs(dx*n[1]-dy*n[0])<3.3:return True
 return False
