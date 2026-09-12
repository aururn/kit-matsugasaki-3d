import bpy,json,math
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'build'/'kit_matsugasaki_campus_v5.blend'))
s=bpy.context.scene;report={};errors=[];notes=[]
survey=json.loads((R/'data'/'access-survey.json').read_text(encoding='utf8'))
data=json.loads((R/'data'/'campus-catalog.json').read_text(encoding='utf8'))
expected={b['name'] for b in data['catalog']}-{'60th Hall annex'}
actual={o.get('building_name') for o in s.objects if o.get('building_name')}
if expected-actual:errors.append('Missing campus buildings '+str(expected-actual))
seen=set();vertices=0
for ob in s.objects:
 if not all(math.isfinite(x) for row in ob.matrix_world for x in row):errors.append('Nonfinite transform '+ob.name)
 if ob.type!='MESH' or ob.data.name in seen:continue
 me=ob.data;seen.add(me.name);vertices+=len(me.vertices)
 a=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',a)
 if not np.isfinite(a).all():errors.append('Nonfinite mesh '+me.name)
 if me.validate(verbose=False):errors.append('Invalid mesh '+me.name)
missing=[i.name for i in bpy.data.images if i.source=='FILE' and not i.packed_file and not Path(bpy.path.abspath(i.filepath)).exists()]
if missing:errors.append('Missing image assets '+str(missing))
for g in survey['gates']:
 ob=next((o for o in s.objects if o.get('access_id')==g['id']),None)
 if ob is None:errors.append('Missing gate '+g['id']);continue
 if math.dist(ob['survey_center_xy'],g['xy'])>.001:errors.append('Gate location mismatch '+g['id'])
tower=next(o for o in s.objects if o.get('access_id')=='university-tower')
if math.dist(tower['survey_center_xy'],survey['tower']['xy'])>.001:errors.append('Tower location mismatch')
entrance_obs={o.get('entrance_id'):o for o in s.objects if o.get('entrance_id')}
door_checks=[]
for e in survey['entrances']:
 if e['id'] not in entrance_obs:errors.append('Missing entrance marker '+e['id']);continue
 if math.dist(entrance_obs[e['id']].location.xy,e['xy'])>.01:errors.append('Entrance marker mismatch '+e['id'])
 ob=next(o for o in s.objects if o.get('building_name')==e['building'])
 # Shoot through an off-centre portion of the door at standing height. Masonry in
 # the threshold means the entry was painted onto a closed facade or obstructed.
 n=Vector((*e['normal'],0));t=Vector((-n.y,n.x,0));base=Vector((*e['xy'],e.get('threshold_z',.12)+1.13))+t*.38
 origin=base+n*.45;inv=ob.matrix_world.inverted();localdir=(inv.to_3x3()@(-n)).normalized()
 hit,loc,norm,fi=ob.ray_cast(inv@origin,localdir,distance=1.25)
 material=ob.data.materials[ob.data.polygons[fi].material_index].name if hit else 'open passage'
 blocked=hit and any(k in material.lower() for k in ['tiles','concrete','painted','brick'])
 if blocked:errors.append('Door ray meets masonry: '+e['id']+' / '+material)
 door_checks.append(dict(id=e['id'],first_surface=material,passed=not blocked))
report.update(campus_parts=len(expected&actual),gate_assemblies=len(survey['gates']),mapped_entrances=len(survey['entrances']),buildings_with_mapped_entrances=len({e['building'] for e in survey['entrances']}),unique_meshes=len(seen),unique_vertices=vertices,missing_images=missing,door_opening_checks=door_checks,errors=errors,passed=not errors,scope='File integrity, map-driven placement and physical facade openings. Not independent field measurement or proof of architectural fidelity.')
(R/'reports'/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='door_opening_checks'},ensure_ascii=True,indent=2))
assert not errors,errors
