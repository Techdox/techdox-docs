"""Temporal screenshots must change only the existing right-edge cursor."""
import json, sys
from pathlib import Path
from PIL import Image, ImageChops
root=Path(sys.argv[1]); results=[]
for row in json.loads((root/'captures.json').read_text()):
    frames=[Image.open(root/f"{row['prefix']}-{k}.png").convert('RGB') for k in range(8)]
    boxes=[ImageChops.difference(frames[0],f).getbbox() for f in frames[1:]]
    changed=[b for b in boxes if b]
    width,height=frames[0].size
    c=row['cursor']; region=(int(c['x']),int(c['y']),min(width,int(c['x']+c['width']+1)),min(height,int(c['y']+c['height']+1)))
    if row['motion']=='reduce':
        assert not changed, f"reduced motion changed: {row['prefix']} {boxes}"
    else:
        assert changed, f"cursor never blinked: {row['prefix']}"
        assert all(b[0]>=region[0]-1 and b[2]<=region[2]+1 and b[1]>=region[1]-1 and b[3]<=region[3]+1 for b in changed), f"letters changed: {row['prefix']} {boxes}"
    # Cursor is blue and visible in at least one frame, including reduced motion.
    blue=0
    for frame in frames:
        rgb=frame.crop(region).tobytes()
        blue=max(blue,sum(1 for r,g,b in zip(rgb[0::3],rgb[1::3],rgb[2::3]) if b>180 and b>r*1.3 and g>80))
    assert blue>2, f"cursor never visible: {row['prefix']}"
    results.append({**row,'diffBounds':boxes,'cursorBluePixels':blue,'passed':True})
(root/'pixel-results.json').write_text(json.dumps(results,indent=2))
print(f'Temporal pixel checks: {len(results)} logo/theme/motion cases passed; letters unchanged; reduced motion static and visible')
