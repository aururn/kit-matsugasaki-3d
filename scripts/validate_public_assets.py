"""Verify the release models are self-contained and include required notices."""
from pathlib import Path
import bpy, json

root = Path(__file__).resolve().parent.parent
reports = []
for name in ['kit_matsugasaki_campus_v5.blend', 'kit_building_studies_v5.blend']:
    bpy.ops.wm.open_mainfile(filepath=str(root/'build'/name))
    errors = []
    images = [i for i in bpy.data.images if i.source == 'FILE']
    for im in images:
        if not im.packed_file:
            errors.append('Unpacked image: '+im.name)
        if not im.filepath.startswith('//'):
            errors.append('Nonportable image path: '+im.name)
    fonts = [f for f in bpy.data.fonts if f.filepath != '<builtin>']
    for font in fonts:
        if not font.packed_file or 'NotoSansCJKjp-Regular.otf' not in font.filepath:
            errors.append('Unexpected/unpacked font: '+font.name)
    if bpy.data.libraries:
        errors.append('External linked Blender libraries remain')
    required = ['PUBLIC | LICENSES/NotoSansCJK-OFL.txt', 'PUBLIC | LICENSES/ODbL-1.0.txt',
                'PUBLIC | SOURCES.md', 'PUBLIC | data/campus-catalog.json', 'PUBLIC | data/site-survey.json']
    errors.extend('Missing notice/data: '+n for n in required if not bpy.data.texts.get(n))
    for text in bpy.data.texts:
        if 'C:\\Users\\' in text.as_string() or 'C:/Users/' in text.as_string():
            errors.append('Local user path in text: '+text.name)
    reports.append(dict(file=name, packed_images=len(images), packed_fonts=len(fonts),
                        libraries=len(bpy.data.libraries), errors=errors, passed=not errors))
out=root/'reports/public-assets-validation.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(reports,ensure_ascii=True,indent=2))
assert all(r['passed'] for r in reports), reports
