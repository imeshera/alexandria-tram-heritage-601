# Fusion build scripts: Raml heritage car 601

These scripts build the Fusion design **Alexandria Heritage Tram 601** from a parameter table. Units are Fusion's
internal cm. Frame: 1:1, X runs from the end-A dash, Y is up from the top of rail, +Z is the side shown in the main
broadside (transphoto 1920902).

## Running a script: the exec loader

Every script defines `run(_context: str)` and finds its helpers, lettering SVGs and render folder relative to its
own `__file__`, so the repo can live anywhere. Run a script through this small loader (paste it into a Fusion
script created under **Utilities → Scripts and Add-Ins → +**, or send it through any bridge that runs Python inside
Fusion), with the path pointing at your clone:

```python
def run(_context: str):
    path = '<repo>/fusion/scripts/<script>.py'          # e.g. ~/src/alexandria-tram-heritage-601/fusion/scripts/build_body.py
    ns = {'__name__': 'fusion_script', '__file__': path}
    exec(compile(open(path).read(), path, 'exec'), ns)
    ns['run'](_context)                                   # _context = the script's options string ('' for defaults)
```

`__file__` must be passed: the scripts compute `ROOT = os.path.dirname(os.path.abspath(__file__))` and exec their
helpers (`common.py`, through `common601.py`) from there.

All geometry reads the document's user parameters. After changing a parameter, re-run the scripts that depend on it.
Each build script wipes and rebuilds its own component, so re-running is safe.

**Fusion project.** `common.py` holds `PROJECT = 'Eshera-Personal'` and `FOLDER = 'Alexandria Tram Model 4 - Raml Heritage 601'`. `create_doc.py`
saves the new design into that folder (created if missing), and the save guards refuse to save a document that is not
in `PROJECT`. Change both constants to use your own project.

## Build order

| # | Script | Context | Builds |
|---|---|---|---|
| 1 | `create_doc.py` | | Creates and saves the design (Hybrid intent) in the model folder |
| 2 | `apply_params.py` | | Creates or updates the 60 user parameters from `params.py`, each with its source and confidence |
| 3 | `build_body.py` | | Side walls with segmental-arch windows (lower and upper colour bodies), bulkheads, floor, arched roof cut to the bowed plan and hollowed over the saloon |
| 4 | `build_ends.py` | | Both 5-facet bowed cab ends: dash, posts, glass, sashes, beading and lining, apron, coupler, headlight, destination board and route box, steps, gates, grab handles |
| 5 | `build_details.py` | | Waist and bottom rails, panel beading and lining, window sashes and glass, solebars; underframe equipment |
| 6 | `build_bogies.py` | | Equalizer-bar bogie with two nose-suspended motors, two instances |
| 7 | `build_roof.py` | | Two lattice towers, diamond pantographs, cables, arrester, roof battens, walkway |
| 8 | `build_interior.py` | | Cherry ceiling with walnut carlines, curtains, lamps, framed photos, bulkhead doors, controllers and brake columns; 22 walkover benches (2+1) as instanced components |
| 9 | `build_appearance.py` | `''` or `parts` | Livery and materials. `parts` skips the slow per-face shell pass (≈12 s instead of ≈3 min); use it after interior, bogie or roof rebuilds. Run in its own call, then check (see BUILD-LOG) |
| 10 | `build_lettering.py` | | CoreText SVG decals per livery from `tools/lettering/svg/601_*` |
| 11 | `canvases.py` | `''` or `hide` | Broadside underlay (needs the derived image, see below) |
| 12 | `save.py` | version message | Guarded save |
| — | `view.py` | `iso`, `isoL`, `isoB`, `left`, `right`, `front`, `rear`, `top`, `interior`, `platform`, `roof`, `bogie`, `front34`, `end_b`, `fit` | Camera presets |
| — | `cam.py` | `ex,ey,ez,tx,ty,tz[,angle]` | Ad-hoc perspective camera for checks |
| — | `render.py` | preset list or `all` | Viewport captures to `docs/renders/<date>_<livery>_<view>.png` |

`common601.py` execs `common.py` (the shared helpers: `comp()`, `wipe()`, the `TB` TemporaryBRep collector,
`base()`, `ev_fn()`, `find_project()`, `model_folder()`) and adds the 601 specifics: `DOC`, the bowed-end plan
polygon `end_poly()` / `facets()`, `mirror_x()` and the guarded `save()`.

## Switches (user parameters)

| Parameter | Values |
|---|---|
| `livery` | 1 light blue / cream, c. 2007–2019 (default) · 2 red / cream after the 2020 restoration · 3 yellow works car, 2002 |
| `panto_a_up`, `panto_b_up` | Pantograph height above folded (the 2024 broadside: A raised 1.4 m, B folded); re-run `build_roof.py` |
| `car_no` | Fleet number |

After changing `livery`, re-run `build_appearance.py` and `build_lettering.py` (the decals differ per livery).

## Photo underlay

`canvases.py` expects `references/images/derived/derived_601_broadside_100pxm.jpg`, which is not in the repo
(it is derived from a copyrighted photo). Download transphoto 1920902 (see `references/SOURCES.md`) to
`references/images/car601/tp_1920902.jpg` and run `python3 references/notes/photogrammetry/underlay_601.py`.
