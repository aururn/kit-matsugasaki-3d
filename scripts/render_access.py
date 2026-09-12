"""Render the saved campus from the surveyed access cameras without hiding neighbours."""
import bpy,sys,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
(R/'build').mkdir(exist_ok=True)
(R/'reports').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'build'/'kit_matsugasaki_campus_v5.blend'))
s=bpy.context.scene
s.cycles.device='CPU'
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences
 prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 if any(d.use for d in prefs.devices):s.cycles.device='GPU'
except Exception:pass
s.render.engine='CYCLES';s.cycles.samples=40 if '--preview' in sys.argv else 96;s.cycles.use_denoising=True
s.render.resolution_x=1600;s.render.resolution_y=1100;s.render.resolution_percentage=60 if '--preview' in sys.argv else 100
s.view_settings.exposure=.35
slugs=['central-east-tower','central-gates-plan','historic-east-gate','northwest-gate','mabashi-gate','library-entry','east1-north-entry']
views=json.loads((R/'data'/'access-views.json').read_text(encoding='utf8'))
selected=sys.argv[sys.argv.index('--only')+1].split(',') if '--only' in sys.argv else slugs
for v,slug in zip(views,slugs):
 if slug not in selected:continue
 s.camera=bpy.data.objects['Access | '+v['name']];s.render.filepath=str(R/'build'/('access-'+slug+('-preview' if '--preview' in sys.argv else '')+'.png'))
 bpy.ops.render.render(write_still=True)
if '--overview' in sys.argv:
 s.camera=bpy.data.objects['Campus 01 | East and West overview'];s.render.filepath=str(R/'build'/'campus-overview.png');bpy.ops.render.render(write_still=True)
