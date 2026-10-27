import argparse
import os
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps

# Only change the generated site; source images stay untouched.
parser = argparse.ArgumentParser(description='Optimize images in a generated Jekyll site.')
parser.add_argument('site', nargs='?', default='_site')
root = Path(parser.parse_args().site).resolve()
repo = Path(__file__).resolve().parents[1]
if root == repo or root.is_relative_to(repo / 'content'):
    raise SystemExit('Refusing to optimize source files; pass a generated site directory')
if not root.is_dir():
    raise SystemExit('Built site not found')
total_before = total_after = changed = skipped = 0
for path in sorted(root.rglob('*')):
    if path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp', '.avif'}:
        continue
    before = path.stat().st_size
    total_before += before
    with Image.open(path) as source:
        if getattr(source, 'is_animated', False):
            skipped += 1
            total_after += before
            continue
        image_format = source.format
        image = ImageOps.exif_transpose(source)
        original_size = image.size
        image.thumbnail((2200, 2200), Image.Resampling.LANCZOS)
        options = {}
        if image.info.get('icc_profile'):
            options['icc_profile'] = image.info['icc_profile']
        if image.getexif():
            options['exif'] = image.getexif().tobytes()
        if image_format == 'JPEG':
            options.update(quality=82, optimize=True, progressive=True)
        elif image_format == 'PNG':
            options.update(optimize=True)
        elif image_format == 'WEBP':
            options.update(quality=82, method=6)
        elif image_format == 'AVIF':
            options.update(quality=82, speed=6)
        output = BytesIO()
        image.save(output, format=image_format, **options)
        data = output.getvalue()
    # Avoid growing already-efficient images unless resizing is needed.
    if len(data) < before or image.size != original_size:
        path.write_bytes(data)
        changed += 1
    total_after += path.stat().st_size
summary = (f'Image optimization: {changed} files updated; '
           f'{skipped} multi-frame images preserved. '
           f'{total_before / 1024**2:.1f} MiB → '
           f'{total_after / 1024**2:.1f} MiB. '
           'Maximum single-frame image edge: 2200 px.')
print(summary)
if os.environ.get('GITHUB_STEP_SUMMARY'):
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as report:
        report.write(summary + '\n')
