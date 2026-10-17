#!/bin/zsh
# Lettering SVGs (mm) for heritage car 601, made with the CoreText tool (tools/lettering/text2svg.swift).
# Usage: ./make_svgs_601.sh <path-to-compiled-text2svg>
#   compile: swiftc -O text2svg.swift -o text2svg   (macOS; run from tools/lettering)
# _R = plain, _L = mirrored (for planes whose sketch x runs against the reading direction).
set -e
T=${1:-./text2svg}
G="            "          # the side legend is painted widely spaced (2.5 m long, 0.13 m letters)
cd "$(dirname "$0")"
for flip in 0 1; do
  s=$([ $flip = 0 ] && echo R || echo L)
  $T svg/601_num_$s.svg      "Helvetica-Bold"  100 $flip "601"
  $T svg/601_numar_$s.svg    "GeezaPro-Bold"   100 $flip "٦٠١"
  $T svg/601_victoria_$s.svg "Georgia-Bold"    100 $flip "VICTORIA"
  $T svg/601_nasr_$s.svg     "DecoType Naskh"  100 $flip "النصر"
  $T svg/601_route2_$s.svg   "Georgia-Bold"    100 $flip "2"
  $T svg/601_routear2_$s.svg "GeezaPro-Bold"   100 $flip "٢"
  $T svg/601_raml_$s.svg     "DecoType Naskh"  100 $flip "محطة الرمل"
  $T svg/601_since_$s.svg    "DecoType Naskh"  100 $flip "بدء دخول الخدمة"
  $T svg/601_1931_$s.svg     "DecoType Naskh"  100 $flip "١٩٣١"
  $T svg/601_apta_$s.svg     "DecoType Naskh"  100 $flip "الهيئة${G}العامة${G}لنقل${G}الركاب${G}بالإسكندرية"
done
