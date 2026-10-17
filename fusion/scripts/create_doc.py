# One-off: creates "Alexandria Heritage Tram 601" (Hybrid intent) in the model folder of project Eshera-Personal
# (looked up by name in the active hub, never app.data.activeProject).
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    DOC = g['DOC']; app = adsk.core.Application.get()
    if [d for d in app.documents if d.name == DOC or d.name.startswith(DOC + ' v')]:
        print('already open'); return
    folder = g['model_folder'](app)
    for i in range(folder.dataFiles.count):
        if folder.dataFiles.item(i).name == DOC:
            print('exists in project; open it instead'); return
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    des = adsk.fusion.Design.cast(app.activeProduct)
    des.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    doc.saveAs(DOC, folder, 'Raml heritage car 601 (four-axle wooden motor car, Alexandria)', '')
    print('created', doc.name)   # dataFile is not ready until the upload finishes
