# Verification - Nashville Historic Zoning Commission Permits brief (2026-11-09)

## Pre-flight audit (Standards Section 10, hard gate)

Audit script: code/audit_section10.py; full output: data/audit_output.txt. Ran BEFORE stats and prose. Result: PASS on every applicable check.

- Zero/null sentinel handling: DATE_ACCEPTED present on all 9,171 records; DATE_ISSUED present on 8,337, missing on 834 (counted, never imputed). No zero, negative, 1970, or pre-1990 sentinel dates in DATE_ACCEPTED, DATE_ISSUED, HCDECISION_DATE, or HCSCHMEET_DATE. Blank Decision/PermitStatus values are carried as their own blank category (PermitStatus blank 5,099) and excluded only from denominators that are printed as decided/dated bases.
- Polarity / matched-vs-excluded for the date filter: gaps are issued minus accepted; matched sample (first 3 dated cases) and excluded sample (first 3 cases missing an issued date, all recorded Disapproved with an accepted date and a blank issued date) are printed in data/audit_output.txt. Negative gaps: 0. The inequality direction (non-negative gaps only) was verified against the matched sample.
- Numerator/denominator unit agreement: every rate in the brief divides permit cases by permit cases in a printed population. No parcel, person, or property units enter any rate; APN/ADDRESS distinct counts are reported as counts only.
- Counter of ALL unique values for every categorical column used: CASE_TYPE (1 value), CASE_TYPE_DESC (1), SUB_TYPE (15), SUB_TYPE_DESC (15), STATUS_CODE (4), PermitStatus (4 including blank), Decision (4) - full counters in data/audit_output.txt. No hardcoded categorical filter was applied without its counter.
- Join hygiene: NO join was performed (no spatial or relational join; ZIP is parsed from the ADDRESS field of the same record). Section 10.2 join checks are therefore not applicable; the internal control is the pull count itself: pulled rows 9,171 = server returnCountOnly 9,171, and OBJECTID unique count 9,171.

Full audit output (verbatim file is data/audit_output.txt; key lines):
```
ROWS 9171
OBJECTID unique 9171
COUNTER CASE_TYPE n_unique=1
  'HCPERMIT': 9171
COUNTER CASE_TYPE_DESC n_unique=1
  'Historical Commission Permit': 9171
COUNTER SUB_TYPE n_unique=15
  'HCNEWCON': 2650
  'HCNEWAD': 2191
  'HC OUTBLDG': 1612
  'HCALTER': 1061
  'HCDEMO': 865
  'HCSIGNAGE': 452
  'HCROOF': 149
  'HCFENCE': 93
  'HCDISA': 40
  'HCGRAVE': 25
  'HCRELOCATE': 14
  'HCLANDINT': 7
  'HCDISR': 5
  'HCLANDSIG': 4
  'HCDISD': 3
COUNTER SUB_TYPE_DESC n_unique=15
  'Historic New Construction': 2650
  'HC - Additions - General': 2191
  'HC - Out Building': 1612
  'Historic Alteration': 1061
  'Historic Demolition': 865
  'Historic Signage': 452
  'HC - Alterations Roof': 149
  'HC - Alteration Fence': 93
  'Historic Alteration - Disaster Related': 40
  'NCC Gravesite': 25
  'Historic Relocation': 14
  'HC – Landmark Interior': 7
  'HC - Alterations Roof - Disaster Related': 5
  'HC – Landmark Signage': 4
  'Historic Demolition - Disaster Related': 3
COUNTER STATUS_CODE n_unique=4
  'DONE': 7173
  'ISSUE': 1897
  'OPEN': 95
  'CLOSED': 6
COUNTER PermitStatus n_unique=4
  '': 5099
  'Issued': 3796
  'Received': 255
  'Deferred': 21
COUNTER Decision n_unique=4
  'Disapproved': 5416
  'Administratively Approved': 2553
  'Approved': 1181
  'Deferred': 21
DATES DATE_ACCEPTED present=9171 missing=0 min=2011-12-07 max=2026-11-06
  sentinel check: year<1990=0 year 1970=0 raw 0/negative=0
  UTC hour census {0: 27, 1: 17, 2: 25, 3: 8, 4: 1, 11: 9, 12: 112, 13: 667, 14: 1129, 15: 1115, 16: 1072, 17: 875, 18: 795, 19: 1069, 20: 1133, 21: 755, 22: 298, 23: 64}
DATES DATE_ISSUED present=8337 missing=834 min=2011-12-07 max=2026-11-06
  sentinel check: year<1990=0 year 1970=0 raw 0/negative=0
  UTC hour census {0: 11, 1: 8, 2: 9, 3: 6, 4: 1, 7: 1, 8: 1, 11: 8, 12: 87, 13: 657, 14: 1056, 15: 1085, 16: 1043, 17: 826, 18: 679, 19: 925, 20: 996, 21: 644, 22: 252, 23: 42}
DATES HCDECISION_DATE present=8118 missing=1053 min=2011-12-07 max=2026-11-06
```

## Methods checklist

- Base rates and exposure: the layer holds only cases that entered the historic-zoning process; no denominator of historic-district building work exists in it, so no such rate is computed. Stated in the brief Methods.
- Direction of causality: no causal claim is made; timing and concentration are reported as recorded.
- Category and definition changes over the window: CHECKED and material - the Decision field's recorded distribution breaks between the 2011-2020 and 2021-2026 acceptance cohorts (approved as recorded 1.4% vs 90.1%; 0.0% in each year 2011-2019). The brief reports approval only on the post-2020 base and flags the break in the body, not only here. SUB_TYPE_DESC (15 values) and CASE_TYPE_DESC (1 value) show no comparable break.
- Exact date range: accepted December 7, 2011 to November 6, 2026 (America/Chicago local dates), printed in the brief.
- Match rates: no join, so no join match rate applies. Field completeness printed instead: issued date 90.9%, ADDRESS/APN present 98.8%, ZIP parseable from ADDRESS 98.8% (112 without).
- Small counts: subtype groups under 30 cases (Relocation 14 dated, Landmark Interior 6, disaster subtypes 1-38) are excluded from median charting (chart floor: 100+ dated cases) and carry their counts wherever named; the top-address/top-parcel counts (33 and 34) are printed with bases.
- Official definitions: the layer metadata does not define Decision or PermitStatus values; the brief says so and assigns no definitions.

## Independent verification

code/verify_independent.py (second implementation, pandas, plus a live server count) recomputed the headline figures from the raw CSV: 18 of 18 checks PASS (data/verify_independent_output.json), including rows, server count, dated count, median gap 0, same-day 4,985 (59.8%), over-30 count 856, median-if-positive 17 days, approved/admin count 3,734, Disapproved-with-issued-date 4,602, ZIP 37206 count 3,472, and the accepted date range.

## Sync gate

README dependency list matches the code's actual imports (standard library; pandas in the verifier only; matplotlib + Pillow in charts/hero only). Every number in brief-draft.md was cross-checked against the final stats.json after the last build_stats.py run, including the era split and the derived per-year figures (about 611 cases a year; roughly 57 over-30-day cases a year, both labeled derived). Social copy figures match stats.json.
- Repository: adowlen/nashville-historic-zoning-data-brief. QA spot-check (parent run, 2026-11-09): the parent recomputed from the raw CSV with a third implementation - dated 8,337, median gap 0, same-day 4,985, over-30-day 856, era split 73/5,106 (1.4 percent) vs 3,661/4,065 (90.1 percent), Disapproved-with-issued-date 4,602, ZIP 37206 = 3,472 - all matching stats.json exactly. Hero generated and viewed by the parent (narrative historic-street scene, charcoal/amber/teal, headline legible on the dark scrim field): PASS. The raw snapshot CSV is excluded from the repository per series precedent (applicant contact fields as served); it is retained as parquet at stack/nashville/snapshots/2026-11-09/nashville_historic_zoning_raw.parquet (9,171 rows).

## Story Gate (Standards Section 13)

- Recorded thesis (before analysis) and its revision after the audit: see reviewer-notes.md. The brief's findings are ordered to serve the revised thesis.
- Human-scale conversion: "about 9 in 10 cases accepted since 2021 are recorded as approved" and "roughly 57 cases a year (derived)" for the over-30-day tail; both labeled derived and recomputed from stats.json figures.
- Cold-reader evidence: INTERNAL cold read (no external reader was available in this build run; this is recorded honestly rather than attributed to an outside person). A fresh reading of only brief-draft.md returned: (1) Point in one sentence: "Nashville's historic-zoning register mostly issues the same day on paper, but its approval label changed meaning around 2021, so only recent years support an approval rate - and the work concentrates in East Nashville's 37206." This matches the revised thesis in substance. (2) Most memorable number: the 1.4 percent vs 90.1 percent approval contrast - the headline finding carried in the title's second clause, the summary, and hero-headline.txt. (3) Where it got bored or lost: the three-register comparison section is the densest passage; each comparison now opens with its brief name and prints its base in the same sentence, and no figure there is load-bearing for the thesis. Gate: PASS after that structural tightening; no figure changed in the story pass.
