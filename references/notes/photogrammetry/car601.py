# car601.py - photogrammetry for Raml heritage car 601 (reproduces car601-dimensions.md).
# Main source: transphoto 1920902 (M. Lazarov, El Raml terminal, 28 Feb 2024), a long-lens, near-orthogonal
# broadside (window pitch 77.7 px at both ends of the car -> perspective negligible, so a linear scale is used).
# Picks are original-image px read off grid overlays (grid.py, 3-4x zoom, 10 px grid).
#
# SCALE (no sourced dimension exists for 601). Three soft anchors that agree within ~5 %:
#   A. Pantograph-tower deck at ~4.5 m above rail: the Raml towers lift the pans to the wire raised for the
#      4.8 m double-deckers; the Kinki SD cars' deck is 4.5 +/- 0.2 m (alexandria-tram-raml-221-223, references/notes).
#      601 deck at y=195, rail at y=592 -> 397 px -> 11.3 mm/px.
#   B. Wheel diameter: wheel rims visible behind both inner axleboxes, radius ~37 px. Typical 1920s/30s
#      bogie-tram wheels are 800-860 mm -> 10.8-11.6 mm/px.
#   C. Front width: two head-on photos give width/dash-height = 2.68 (tp 2110423) and 2.72 (tp 1915990);
#      with the broadside dash height (80 px) and the Raml clearance (Kinki 2.42 m, new cars 2.65 m "wider
#      than the old") a 2.40-2.45 m body gives 11.1-11.3 mm/px.
# Adopted: 11.25 mm/px (+/- 7 %). Gauge (1435 mm) could not be used: the rails are hidden or strongly oblique
# under the car in every head-on shot, and the focal length is unknown.
S = 11.25          # mm/px
RAIL = 592         # rail-head y in the broadside
END_A, END_B = 60, 1237   # dash centres (end A = image left). Apron noses at 22 / 1258.

def h(y): return (RAIL - y) * S / 1000.0
def x(px): return (px - END_A) * S / 1000.0

heights = {'roof crown': 300, 'roof edge (top of cornice)': 315, 'eave board bottom': 331,
           'window head (arch top)': 342, 'glass bottom / sill': 428, 'waist rail bottom': 436,
           'red panel bottom': 508, 'bottom rail bottom': 516, 'solebar bottom': 537,
           'platform floor': 515, 'upper step': 528, 'lower step': 550, 'tower deck': 195,
           'folded pantograph top': 165}
lengths = {'body over dashes (centres)': (END_A, END_B), 'saloon (outer end posts)': (172, 1128),
           'platform A (dash -> end post)': (END_A, 172), 'entrance A opening': (90, 172),
           'first narrow window': (187, 217), 'window 1 (big)': (232, 293), 'window 11 (big)': (1009, 1072),
           'last narrow window': (1088, 1118), 'tower A legs (roof)': (227, 432), 'tower A deck': (243, 401),
           'tower B legs (roof)': (827, 1075), 'tower B deck': (819, 1069),
           'bogie A axleboxes': (230, 360), 'bogie B axleboxes': (940, 1080),
           'air reservoir': (680, 810), 'resistor/grid box': (585, 640)}

if __name__ == '__main__':
    print('scale %.2f mm/px' % S)
    for k, y in heights.items(): print(f'{k:28s} {h(y):5.2f} m')
    for k, (a, b) in lengths.items(): print(f'{k:28s} {x(a):6.2f} - {x(b):6.2f} m  ({(b - a) * S / 1000:4.2f})')
    print('window pitch %.3f m' % ((1009 - 232) / 10 * S / 1000))
    print('bogie centres %.2f / %.2f m, spacing %.2f, wheelbase %.2f' % (x(295), x(1010), (1010 - 295) * S / 1000, 135 * S / 1000))
    print('wheel diameter %.2f m' % (74 * S / 1000))
    # front (tp 2110423, head-on, 8.4 mm/px from the 0.94 m dash): dash 300 px, headlight centre 54 px below sill,
    # ring 35 px; glass 1.94-2.96 m; destination board 3.12-3.34 m; Western number 1.51 m, 0.135 m tall
    f = 0.94 / 112
    print('front width %.2f m, headlight %.2f m (ring %.2f), numbers %.2f m' % (300 * f, 1.80 - 54 * f, 35 * f, 1.80 - 34 * f))
