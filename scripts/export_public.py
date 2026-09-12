"""Package existing v5 models without regenerating geometry.

blender --background --factory-startup --disable-autoexec --python-exit-code 1
        --python scripts/export_public.py -- /path/to/existing-v5-models
"""
from pathlib import Path
import bpy, sys

R = Path(__file__).resolve().parent.parent
source = Path(sys.argv[sys.argv.index('--')+1]).resolve()
(R/'build').mkdir(exist_ok=True)
for filename in ['kit_matsugasaki_campus_v5.blend', 'kit_building_studies_v5.blend']:
    destination = R/'build'/filename
    if source/filename == destination:
        raise ValueError('Use a separate source directory to preserve the originals.')
    bpy.ops.wm.open_mainfile(filepath=str(source/filename))
    old_fonts = [f for f in bpy.data.fonts if f.filepath != '<builtin>']
    public_font = bpy.data.fonts.load(str(R/'assets/fonts/NotoSansCJKjp-Regular.otf'))
    for font in old_fonts:
        font.user_remap(public_font)
        bpy.data.fonts.remove(font)
    for filename_doc in ['README.md','SOURCES.md']:
        block = bpy.data.texts.get('V5 | '+filename_doc)
        if block:
            block.clear()
            block.write((R/filename_doc).read_text(encoding='utf8'))
    exec((R/'scripts/pack_public_assets.py').read_text(encoding='utf8'))
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(destination))
    print('PUBLIC_MODEL_EXPORTED', destination.name, flush=True)
