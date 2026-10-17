# Raml heritage car 601: identification and choice

*Compiled 2026-10-17. Raw research with every source URL: `research-raw.md`. Dimension sheet and photogrammetry:
`car601-dimensions.md`. Reference photo list: `../SOURCES.md` and `../manifests/*.csv`.*

## The four reference trams

The project started from four photographs of Alexandria trams. Each was identified by type before choosing what
to model; each type is now its own model repository.

| Reference photo | What it is | Model |
|---|---|---|
| 1. Ochre-and-cream **894** | **Düwag GT6** six-axle articulated car, ex-Copenhagen **KS 894**, in Alexandria since 1972 with its number unchanged. Still in service in 2024 on city route 4, then in green and white | [alexandria-tram-gt6-894](https://github.com/imeshera/alexandria-tram-gt6-894) |
| 2. Red-and-cream **601** | The **Raml heritage car**: a four-axle wooden motor car (Oerlikon 1925 or Belgian 1931; sources disagree). **Light blue and cream until about 2019**, red and cream after the restoration (heritage service from 6 Oct 2020) | [alexandria-tram-heritage-601](https://github.com/imeshera/alexandria-tram-heritage-601) |
| 3. Yellow two-car set with a blue stripe | City two-car set, identified as **Ganz-MÁVAG 1201–1230 (1985/86)** (the lookalike Kinki Sharyo 117–130 of 1982 was ruled out on livery and readable fleet numbers). One cab per car, trolley poles | [alexandria-tram-city-1211-1212](https://github.com/imeshera/alexandria-tram-city-1211-1212) |
| 4. Green-and-white **856** | **Another ex-Copenhagen Düwag GT6** (KS 856, delivered 1963, Alexandria 1971), seen from its **rear end**. The "curved two-pane windscreen with open door" is the GT6's rear window and rear-corner door; the side digits that read like "١٠٧" are ٨٥٦ in Naskh | Same type as 894 |

Confidence key used throughout the notes:
- **S**: stated by a source.
- **S?**: sourced, but generic, analog or conflicting.
- **V**: measured from dated photos (photogrammetry).
- **E**: engineering estimate.

## 1. Type summary: Raml heritage car 601 (reference photo 2)

- **Build:** four-axle wooden motor car, double-ended, with a lattice tower carrying a diamond pantograph.
- **Builder, conflicting:** Oerlikon 1925, rebuilt from the 501–517 series (UTM, en.wiki); or Belgian, 1931 (Egyptian press, and the car's own apron reads "بدء دخول الخدمة ١٩٣١").
- **Liveries:**
  - Light blue / cream with a black apron and a dark-red route board (2007–2012 photos).
  - Red / cream with a blue-grey apron after the 2020 restoration.
- **Interior:** varnished wooden slat walkover seats.
- **Status:** out of service since the Raml closure (1 Apr 2026); museum-designated.
- **Dimensions, published:** none. Estimate before photogrammetry (E): about 12.5–13.5 m long, 2.3–2.4 m wide, bogie centres 6.5–7.5 m, wheels 760–840 mm.
- **Dimensions, measured:** 13.24 m over the dashes, 2.40 m wide, roof 3.29 m, bogie centres 7.96 m apart, 11 + 2
  arched windows per side; absolute scale ±7 %. See `car601-dimensions.md`.

## 2. Why 601

Car 601 is the "very old style" Alexandria tram: a 1920s/30s wooden body, double-ended, with open platforms and a
lattice pantograph tower, and it was **light blue and cream until about 2019**, matching the "light blue, very old
style" brief. It is a one-off and has the weakest data of the reference trams (no published dimension at all), so
it needed its own photogrammetry pass from the 2024 transphoto broadside.

**Modelled car:** **601**, Fusion design **"Alexandria Heritage Tram 601"**. The livery is switchable through the
`livery` user parameter:

| Value | Scheme | Period / evidence |
|---|---|---|
| 1 (default) | Light blue / cream, black apron with "بدء دخول الخدمة ١٩٣١", dark-red destination board "VICTORIA 2 النصر" | c. 2007–2019 (2012 Commons, 2007 Parris) |
| 2 | Red / cream, blue-grey apron, red board "محطة الرمل" with route ٢ | After the 2020 restoration (transphoto 2110423, 2168484; UTM 2023) |
| 3 | Yellow works car | 2002 (Tram Travels) |

## Related models

The Alexandria vehicle models are published as separate repositories, each self-contained:

| Repository | Vehicle |
|---|---|
| [alexandria-tram-raml-221-223](https://github.com/imeshera/alexandria-tram-raml-221-223) | Kinki Sharyo Raml three-car set 221–223 |
| [alexandria-tram-raml-dd-224](https://github.com/imeshera/alexandria-tram-raml-dd-224) | Raml double-deck car 224 and its set |
| [alexandria-tram-gt6-894](https://github.com/imeshera/alexandria-tram-gt6-894) | Ex-Copenhagen Düwag GT6 894 (city network) |
| [alexandria-tram-heritage-601](https://github.com/imeshera/alexandria-tram-heritage-601) | Raml heritage car 601 (four-axle wooden motor car) |
| [alexandria-tram-city-1211-1212](https://github.com/imeshera/alexandria-tram-city-1211-1212) | Ganz-MÁVAG city two-car set 1211+1212 |
| [alexandria-lada-taxi](https://github.com/imeshera/alexandria-lada-taxi) | Alexandria Lada taxi |
