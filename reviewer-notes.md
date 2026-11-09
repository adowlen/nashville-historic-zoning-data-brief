# Reviewer notes - Nashville Historic Zoning Commission Permits brief (2026-11-09)

## Thesis recorded before analysis (Standards Section 13.1)
"Nashville's historic-zoning permits form a small, slow decision lane distinct from ordinary permits: most are eventually approved, but acceptance-to-issuance takes weeks rather than days, and cases concentrate in a few case/sub types and neighborhoods."

## Thesis revision (after the audit, before drafting)
The "slow lane / weeks" clause failed: the dated median is 0 days and 59.8 percent of dated cases issued the same day. The approval clause also failed in its simple form: the Decision field's recorded distribution breaks between acceptance cohorts (1.4 percent approved as recorded for 2011-2020; 90.1 percent for 2021-2026), and 4,602 Disapproved cases carry issued dates. Revised thesis, which the findings are ordered to serve: "The historic-zoning lane is mostly fast on paper - most dated cases issue the same day, and the cases that take at least a day wait a median of 17 days - but its Decision field contradicts its issuance dates across the early series, so the approval share can only be reported on the post-2020 base, and cases concentrate heavily in ZIP 37206."

## Claims most likely to be challenged
- The Decision-era reading (1.4% vs 90.1%): a reader may hold the underlying case-management export or a codebook showing what "Disapproved" meant in the legacy system. The brief claims only what the register records, prints the issued-date cross-check (4,602 cases), and names the missing field definitions in Methods and Who can act.
- The same-day share (59.8%): accepted/issued dates may be entered together administratively. The brief carries this as the strongest alternative explanation in "What this might mean" and makes no service-speed claim.
- ZIP concentration: ZIP is parsed from the ADDRESS tail, not a service field; 112 cases carry no ZIP there and 11 end in 00000. Method printed in the brief.
- Series comparisons: three different registers, windows, and bases; every comparison prints its base and carries a not-like-for-like label.

## Incomplete checks
- No official Decision/PermitStatus definitions exist in the layer metadata; none could be checked beyond the metadata archived in the package. Recorded as an incomplete check, and the brief's approval reporting is restricted accordingly.
- No exposure base (historic-district building work that never entered this process) exists in the layer; no such rate is computed.

## Surprises
- Median gap of 0 days against a "commission review" expectation; the slow tail is real but narrow (10.3 percent of dated cases over 30 days).
- The Decision field's era break is near-total: 0.0 percent recorded approved in every acceptance year 2011-2019.
- Repeat properties: 9,171 cases on 4,352 parcels.

## Blocking defects
None. Hero image is intentionally not in this package: the parent generates the illustration and composites it with code/hero_composite.py after QA (hero-headline.txt carries the approved headline). That is the standing build split, not a package defect.
