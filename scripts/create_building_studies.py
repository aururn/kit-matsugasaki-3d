"""One Blender scene per building, sharing the actual campus meshes."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'build'/'kit_matsugasaki_campus_v5.blend'))
entry_survey=json.loads((R/'data'/'access-survey.json').read_text(encoding='utf8'))
campus=bpy.context.scene;campus.name='00 | Matsugasaki full campus'
base_lights=[o for o in campus.objects if o.type=='LIGHT']
catalog=json.loads((R/'data'/'campus-catalog.json').read_text(encoding='utf8'))['catalog']
groundmesh=bpy.data.meshes.new('Study floor');groundmesh.from_pydata([(-1500,-1500,-.04),(1500,-1500,-.04),(1500,1500,-.04),(-1500,1500,-.04)],[],[(0,1,2,3)])
floor=bpy.data.objects.new('Shared study floor',groundmesh)
floor_mat=bpy.data.materials.new('Study floor neutral');floor_mat.diffuse_color=(.4,.42,.4,1);groundmesh.materials.append(floor_mat)
records=[]
for b in catalog:
 name=b['name'];obs=[o for o in campus.objects if o.type!='FONT' and (o.get('building_name')==name or o.get('belongs_to_building')==name)]
 if not obs:continue
 scene=bpy.data.scenes.new('Building | '+name);scene.world=campus.world;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
 scene.render.resolution_x=2000;scene.render.resolution_y=1500;scene.view_settings.view_transform=campus.view_settings.view_transform;scene.view_settings.exposure=.55
 for ob in obs+base_lights+[floor]:scene.collection.objects.link(ob)
 verts=[o.matrix_world@Vector(v) for o in obs if o.type=='MESH' for v in o.bound_box]
 lo=Vector(tuple(min(v[k] for v in verts) for k in range(3)));hi=Vector(tuple(max(v[k] for v in verts) for k in range(3)));size=hi-lo;target=(lo+hi)/2;target.z=lo.z+size.z*.43
 entry=next((e for e in entry_survey['entrances'] if e['building']==name),None)
 normal=entry['normal'] if entry else {'Museum of Arts and Crafts':(1,0),'Center Hall and learning building':(0,1),'Plaza KIT':(0,1)}.get(name,(0,-1))
 direction=Vector((normal[0]-normal[1]*.50,normal[1]+normal[0]*.50,.30)).normalized();distance=max(15,max(size.x,size.y)*1.8)
 camera=bpy.data.cameras.new('Solo camera | '+name);ob=bpy.data.objects.new(camera.name,camera);scene.collection.objects.link(ob);ob.location=target+direction*distance;ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler();camera.lens=48;camera.clip_end=3000;scene.camera=ob
 scene['Source']='Meshes linked from the v5 campus, not a different simplified model.';scene['Accuracy']=b['detail_profile']['evidence_level']
 records.append({'scene':scene.name,'building':name,'meshes':sum(o.type=='MESH' for o in obs)})
# Retain the detailed historic building as its own scene as well.
historic=next(c for c in campus.collection.children if c.name.startswith('01 |'))
hs=bpy.data.scenes.new('Building | 3 Historic main building');hs.world=campus.world;hs.collection.children.link(historic);hs.collection.objects.link(floor)
hs.camera=next(o for o in historic.all_objects if o.type=='CAMERA' and o.name.startswith('04'))
hs.render.engine='CYCLES';hs.cycles.samples=64
records.append({'scene':hs.name,'building':'3 Historic main building','meshes':sum(o.type=='MESH' for o in historic.all_objects)})
# Access views preserve surrounding buildings so gate/tower placement can be checked.
access_scenes=[]
for cam in [o for o in campus.objects if o.type=='CAMERA' and o.name.startswith('Access |')]:
 sc=bpy.data.scenes.new(cam.name);sc.world=campus.world;sc.camera=cam
 for col in campus.collection.children:sc.collection.children.link(col)
 sc.render.engine='CYCLES';sc.cycles.samples=64;sc.cycles.use_denoising=True;sc.render.resolution_x=1600;sc.render.resolution_y=1100
 sc.view_settings.view_transform=campus.view_settings.view_transform;sc.view_settings.exposure=.35
 sc['Evidence']='See embedded access-survey.json and SOURCES.md. Location is map/photo informed, not a field survey.'
 access_scenes.append(sc.name)
bpy.context.window.scene=bpy.data.scenes.get('Access | 中央東門と大学の塔') or hs
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=3000;area.spaces.active.shading.color_type='MATERIAL'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'build'/'kit_building_studies_v5.blend'))
(R/'reports'/'building-scenes.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print('BUILDING_STUDIES_SAVED',len(records),'ACCESS_SCENES',len(access_scenes))
