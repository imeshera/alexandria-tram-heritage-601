# Build log: Raml heritage car 601

Decisions, measurements and gotchas, newest last. Dimension sheet: `references/notes/car601-dimensions.md`.

## Fusion API gotchas carried over from the GT6 894 build
These were found on the first model (GT6 894) and apply to the shared helpers in `common.py`:
- `TemporaryBRepManager` union of many same-named parts inside `TB.commit` made a script time out (the transaction
  rolled back). Committing parts as separate bodies takes 0.2 s. Merging is off by default; `base()` name matching
  handles Fusion's "(1)" suffixes.
- `OrientedBoundingBox3D.create` needs width ⟂ length. `TB.box` orthogonalises the width axis.
- Deleting the only occurrence of a new component deletes the component. Keep it and reuse it as instance 1.
- Setting a face appearance can reorder `body.faces`: loop by index and repeat until a pass changes nothing.
- Editing the colour of an in-use appearance spawns same-named duplicates. Write a colour only when it differs.
- `Sketch.move` ignores imported SVG curves: turn extruded decal bodies with a free-move feature instead.
  `common.wipe` also deletes move features.
- After a camera change the first `saveAsImageFile` capture can come out blank; render scripts capture twice.

## 2026-10-17: Research, photogrammetry and Fusion build v1
- **Context:** car 601 is reference photo 2 of the four reference trams (see `references/notes/heritage-dossier.md`); it was built second, after the GT6 894.
- **Research gap filled:** transphoto lists 16 more photos of 601 (2022–25), listed in `references/manifests/car601.csv`. The key ones:
  - **1920902**, a near-orthogonal long-lens broadside: window pitch 77.7 px at both ends, so a linear scale works.
  - **1702830**, the interior.
  - **2110423 and 1915990**, head-on views.
- No published dimension of 601 was found. The builder is still unresolved (Oerlikon 1925 vs "Belgian 1931").
- **Scale:** three soft anchors agree within about 5 %, giving 11.25 mm/px ± 7 %.
  - Tower deck 4.5 m (Kinki SD analog: the Raml wire was raised for the double-deckers).
  - Wheel rims ≈ 0.83 m.
  - Head-on width/dash ratio.
  - **Gotcha:** the gauge was unusable. In every head-on shot the rails are hidden or strongly oblique under the car, and the focal length is unknown.
- **Gotcha: front width.** The first ratio used the cream waist rail plus the red as the dash height and gave 2.2 m. The front red dash and the side red panels are different bands. Matching glass heights and red heights both give 2.40 m.
- **Layout from the broadside:**
  - 11 arched windows of 0.69 m at 0.874 m pitch, plus a narrow 0.34 m window at each end;
  - open platforms of 1.26 m with entrances on all four corners;
  - bogie centres 2.64 m from each end (wheelbase 1.52 m);
  - towers at 3.03 / 9.99 m (deck 4.47 m).
  - The end is a 5-facet bow: corner, intermediate (14°), centre (big window), intermediate, corner.
- **Fusion:** created **Alexandria Heritage Tram 601** (Hybrid). It is saved into its model folder through `model_folder()`, which looks the project up by name in the active hub.
  - **Gotcha:** right after `saveAs`, `doc.dataFile.parentProject` raises InternalValidationError until the upload finishes. The save guard is therefore only used for later saves.
- **Build approach:** the shell is built as separate colour bodies, so the livery needs no face splitting.
  - Lower panel wall, upper window wall, dash / waist band / header / posts per facet.
  - Only inward faces are re-painted, as varnished wood.
- **Gotcha: overlapping profile edges.** A window bottom on the wall's outer edge merges the window into the outline, so the window isn't a hole. The upper wall now starts at the waist (1.75 m) and the windows at the sill (1.84 m).
- **Extrude direction:** `extrude()` takes the sign from the sketch normal (`xDirection × yDirection`), not trial and error. XZ-plane sketches extrude along −Y.
- **Gotcha in the appearance script:** the side bodies are named "Side upper L/R" and didn't match the "Side upper" key, so they stayed default Steel Satin. The script now strips the L/R suffix.
- **Lettering:** `make_svgs_601.sh` makes the decal SVGs.
  - Dash numbers sit on the angled intermediate facets.
  - The board texts are on the board's intermediate facets.
  - The route numeral is on the route box.
  - The apron "١٩٣١" and "بدء دخول الخدمة" are livery 1 only.
  - The red-era side legend is livery 2 only. It is painted widely spaced (2.5 m long, 0.13 m letters), so the SVG has 12 spaces between words.
- **Overlay check** (left view, broadside at 45 %): window grid, platforms, roof and cornice line, tower positions and the legend position all match. The underlay is hidden for renders.

## 2026-10-17: Refinement, liveries, renders
- **Lettering bug (it also affected the GT6 894 lettering script, fixed there the same day):** the ink box was measured from `sketch.sketchPoints`, and that includes the sketch origin.
  - The box therefore grew by the font ascent, so decals came out at 50–93 % of the requested height. The Naskh numerals were the worst.
  - The 601 script now takes the box from the curves' bounding boxes, and every decal comes out at exactly the requested height.
  - The 894 document was not rebuilt. Its dash numbers are about 7 % small and its Naskh texts smaller still. Fix: port the 3-line change and re-run `build_lettering.py` on 894.
- **Interior:** cherry-varnished ceiling with walnut carlines (the 2022 photo shows dark varnish, not oak), inverted-U chrome handles on the walkover backs, framed photographs on the coves, and a drum controller with notch plate and reverser key. The bell cord was dropped because the photo shows none.
- **Camera gotcha:** going from an orthographic preset straight to an interior eye renders blank, and so did a few interior eyes near the bulkhead. `view.py` now applies special cameras twice, with a refresh in between.
- **Appearance gotcha:** after an interior rebuild one `parts` pass left every interior body at the default Steel Satin. A second run painted them. Always check with a read-only appearance census after a rebuild.
- `build_appearance.py parts` skips the slow per-face pass on the shell (about 12 s instead of about 3 min). Use it after interior, bogie or roof rebuilds.
- **Liveries:** all three schemes were rendered. In livery 2 the dash lining is the cream inset line, the apron blue-grey, and the board red with "محطة الرمل" and a white "٢"; it matches transphoto 2110423 and 2168484. Livery 3 is the 2002 yellow works car.
  - The appearance pass takes about 40 s when Fusion is idle. Earlier passes that ran behind timed-out remote calls left the Ends component unpainted. Progress now goes to `appearance601.log` in the system temp directory.
- **Open items:**
  - The absolute scale is ±7 %.
  - The 2002 centre side door (yellow era) is not modelled.
  - Tower B carried a bow collector in 2012; the model has a diamond pantograph on both towers.
  - The front-window layout differs slightly between the two ends in the photos; the model uses one symmetric layout.

## 2026-10-17: Parameter evaluation check (found on the city set)
- On the Ganz city car, `unitsManager.evaluateExpression('half_w')` returned a stale value after `body_w` was edited
  mid-session, so bodies were silently built at the old width. 601 also had parameters edited mid-session; its
  broadside overlay still matched, but after a parameter change close and reopen the document before rebuilding,
  or read plain names from `userParameters` as the city scripts do.
- **Painting in the same call as a build can fail to persist** (seen here and on the city set): paint in a separate
  call, then run a read-only appearance census.

## 2026-10-17: Split into its own repository
- The model was developed inside a combined Alexandria-trams workspace, together with the other reference trams
  (see "Related models" in `references/notes/heritage-dossier.md`). This repository carries only this model's
  scripts, notes, renders, manifests and exports, plus a copy of the shared helper `common.py`.
- **Paths:** scripts no longer use absolute paths. The exec loader passes `__file__`; each script resolves
  `ROOT = os.path.dirname(os.path.abspath(__file__))` and finds its helpers, the lettering SVGs
  (`tools/lettering/svg/`), the render folder (`docs/renders/`) and the derived underlay
  (`references/images/derived/`, gitignored) relative to it. Progress logs go to the system temp directory.
- **Fusion organisation:** the designs now live in project **Eshera-Personal**, folder **Alexandria Tram Model 4 - Raml Heritage 601**. `create_doc.py`
  saves into that folder (created if missing), and the save guards check `PROJECT = 'Eshera-Personal'`.
- **Exports** in `models/` were made from the final Fusion designs: `Alexandria Heritage Tram 601.f3d` and `.step`.
- Reference photos are not redistributed; `references/SOURCES.md` lists each with author, licence and URL.
