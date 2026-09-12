import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'build'/'kit_building_studies_v5.blend'))
buildings=[s for s in bpy.data.scenes if s.name.startswith('Building |')]
access=[s for s in bpy.data.scenes if s.name.startswith('Access |')]
errors=[]
if len(buildings)!=75:errors.append('Expected 75 building scenes')
if len(access)!=7:errors.append('Expected 7 access scenes')
for s in buildings+access:
 if not s.camera or not any(o.type=='MESH' and not o.hide_render for o in s.objects):errors.append('Empty scene '+s.name)
for s in access:
 if len([o for o in s.objects if o.get('access_id')])<11:errors.append('Access context incomplete '+s.name)
missing_fonts=[f.filepath for f in bpy.data.fonts if f.filepath and f.filepath!='<builtin>' and not f.packed_file and not Path(bpy.path.abspath(f.filepath)).exists()]
if missing_fonts:errors.append('Missing fonts '+str(missing_fonts))
report=dict(building_scenes=len(buildings),access_scenes=len(access),default_scene=bpy.context.scene.name,missing_fonts=missing_fonts,errors=errors,passed=not errors)
(R/'reports'/'studies-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2));assert not errors,errors
