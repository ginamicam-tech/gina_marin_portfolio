#!/usr/bin/env python3
"""Regenerate flat artwork crops and square thumbnails from reviewed pixel bounds."""
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
for item in json.loads((ROOT / 'scripts/artwork-crops.json').read_text()):
    with Image.open(ROOT / item['source'].lstrip('/')) as source:
        artwork = ImageOps.exif_transpose(source).convert('RGB').crop(item['crop'])
    output = ROOT / item['output'].lstrip('/')
    output.parent.mkdir(parents=True, exist_ok=True)
    artwork.save(output, quality=95, subsampling=0)
    square = Image.new('RGB', (1400, 1400), '#f5f3ef')
    artwork.thumbnail((1228, 1228), Image.Resampling.LANCZOS)
    x, y = (1400 - artwork.width) // 2, (1400 - artwork.height) // 2
    square.paste(artwork, (x, y))
    ImageDraw.Draw(square).rectangle(
        (x - 1, y - 1, x + artwork.width, y + artwork.height),
        outline='#c8c5bf', width=1)
    square.save(ROOT / item['thumbnail'].lstrip('/'), quality=92, subsampling=0)
