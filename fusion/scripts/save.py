# Guarded save of the 601 document: _context = version message.
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    print('saved' if g['save'](_context or 'checkpoint') else 'save returned False')
