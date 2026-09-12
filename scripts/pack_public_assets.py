"""Embed attribution and use portable paths. Executed in the builder namespace."""
from pathlib import Path
import bpy

public_root = Path(__file__).resolve().parent.parent
for public_name in ['README.md', 'SOURCES.md', 'LICENSES/README.md',
                    'LICENSES/NotoSansCJK-OFL.txt', 'LICENSES/ODbL-1.0.txt',
                    'data/campus-catalog.json', 'data/site-survey.json']:
    block = bpy.data.texts.get('PUBLIC | '+public_name) or bpy.data.texts.new('PUBLIC | '+public_name)
    block.clear()
    block.write((public_root/public_name).read_text(encoding='utf8'))
for im in list(bpy.data.images):
    if im.source == 'FILE':
        asset_name = Path(im.filepath.replace('\\','/')).name
        public_image = bpy.data.images.load(str(public_root/'assets/textures'/asset_name), check_existing=False)
        public_image.colorspace_settings.name = im.colorspace_settings.name
        public_image.alpha_mode = im.alpha_mode
        image_name = im.name
        im.user_remap(public_image)
        bpy.data.images.remove(im)
        public_image.name = image_name
        public_image.pack()
for font in bpy.data.fonts:
    if font.filepath != '<builtin>':
        if not font.packed_file:
            font.pack()
        font.filepath = str(public_root/'assets/fonts'/Path(font.filepath.replace('\\','/')).name)
for sc in bpy.data.scenes:
    sc.render.filepath = '//render.png'
bpy.ops.file.make_paths_relative()
