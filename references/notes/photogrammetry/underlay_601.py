# underlay_601.py - metric left-side (+z) elevation of car 601 at 100 px/m from the transphoto 1920902 broadside
# (near-orthogonal, linear scale 11.25 mm/px; see car601.py). Writes
# references/images/derived/derived_601_broadside_100pxm.jpg; the model origin (end-A dash centre, top of rail)
# lands at px (67.5, 666). Run: python3 underlay_601.py
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '../../images/')
S = 11.25 / 10.0
im = Image.open(IMG + 'car601/tp_1920902.jpg').convert('RGB')
out = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)
os.makedirs(IMG + 'derived', exist_ok=True)
out.save(IMG + 'derived/derived_601_broadside_100pxm.jpg', quality=92)
print(out.size, 'origin px', 60 * S, 592 * S)
