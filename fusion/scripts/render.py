# Saves viewport images of the 601 design to docs/renders/<date>_<livery>_<name>.png.
# _context: comma-separated view.py presets, or 'all'.
import adsk.core, adsk.fusion, datetime
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '..', '..', 'docs', 'renders', '')

def run(_context: str):
    import os; os.makedirs(OUT, exist_ok=True)
    v = {'__file__': os.path.join(ROOT, 'view.py')}; exec(open(v['__file__']).read(), v)
    app = adsk.core.Application.get()
    names = (_context or 'iso').strip()
    if names == 'all':
        names = 'iso,isoL,left,right,front,rear'
    tag = datetime.date.today().isoformat()
    for n in names.split(','):
        v['run'](n)
        des = adsk.fusion.Design.cast(app.activeProduct)
        lv = {1: 'blue', 2: 'red', 3: 'yellow'}.get(int(round(des.userParameters.itemByName('livery').value)), 'x')
        app.activeViewport.refresh()
        f = OUT + '%s_%s_%s.png' % (tag, lv, n)
        h = 1000 if n in ('left', 'right', 'iso', 'isoL', 'isoB', 'top') else 1600 if n in ('front34', 'end_b', 'front', 'rear') else 1400
        app.activeViewport.saveAsImageFile(f, 2400, h)     # first capture after a camera change can be blank
        app.activeViewport.saveAsImageFile(f, 2400, h)
        print('saved', f)
