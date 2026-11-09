import csv, json, collections, os, re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HERE=os.path.dirname(__file__); DATA=os.path.normpath(os.path.join(HERE,"..","data"))
CHI=ZoneInfo("America/Chicago")
def ldate(v):
    if v in (None,""): return None
    try: ms=int(float(v))
    except: return None
    return datetime.fromtimestamp(ms/1000, tz=timezone.utc).astimezone(CHI).date()
rows=list(csv.DictReader(open(os.path.join(DATA,"nashville_historic_zoning_raw.csv"))))
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)
p("ROWS",len(rows))
p("OBJECTID unique",len(set(r["OBJECTID"] for r in rows)))
for col in ["CASE_TYPE","CASE_TYPE_DESC","SUB_TYPE","SUB_TYPE_DESC","STATUS_CODE","PermitStatus","Decision"]:
    c=collections.Counter((r[col] or "") for r in rows)
    p(f"COUNTER {col} n_unique={len(c)}")
    for k,v in c.most_common(100): p(f"  {k!r}: {v}")
# sentinel dates
for col in ["DATE_ACCEPTED","DATE_ISSUED","HCDECISION_DATE","HCSCHMEET_DATE"]:
    vals=[r[col] for r in rows if r[col] not in (None,"")]
    ds=[ldate(v) for v in vals]
    p(f"DATES {col} present={len(vals)} missing={len(rows)-len(vals)} min={min(ds) if ds else None} max={max(ds) if ds else None}")
    p(f"  sentinel check: year<1990={sum(1 for d in ds if d and d.year<1990)} year 1970={sum(1 for d in ds if d and d.year==1970)} raw 0/negative={sum(1 for v in vals if float(v)<=0)}")
    hc=collections.Counter(datetime.fromtimestamp(int(float(v))/1000, tz=timezone.utc).hour for v in vals)
    p(f"  UTC hour census {dict(sorted(hc.items()))}")
# gaps polarity sample
both=[r for r in rows if r["DATE_ACCEPTED"] and r["DATE_ISSUED"]]
gaps=[(ldate(r["DATE_ISSUED"])-ldate(r["DATE_ACCEPTED"])).days for r in both]
p("BOTH DATES",len(both),"negative",sum(1 for g in gaps if g<0),"zero",sum(1 for g in gaps if g==0),"positive",sum(1 for g in gaps if g>0))
p("POLARITY SAMPLE matched (both dates, first 3):",[(r["CASE_NUMBER"],str(ldate(r["DATE_ACCEPTED"])),str(ldate(r["DATE_ISSUED"])),(ldate(r["DATE_ISSUED"])-ldate(r["DATE_ACCEPTED"])).days) for r in both[:3]])
excl=[r for r in rows if not (r["DATE_ACCEPTED"] and r["DATE_ISSUED"])]
p("POLARITY SAMPLE excluded (missing a date, first 3):",[(r["CASE_NUMBER"],r["DATE_ACCEPTED"],r["DATE_ISSUED"],r["PermitStatus"],r["Decision"]) for r in excl[:3]])
p("MISSING accepted only-missing",sum(1 for r in rows if not r["DATE_ACCEPTED"]),"issued-missing",sum(1 for r in rows if not r["DATE_ISSUED"]))
# unit agreement note
p("UNIT AGREEMENT: every rate numerator and denominator are permit records (rows) in the stated population; no parcel/person units mixed. Approval share denominator stated explicitly wherever used.")
p("UNKNOWN EXCLUSION: missing/blank Decision and PermitStatus counted as their own blank category and excluded only from decided-only denominators, which are printed.")
# address / APN / ZIP-from-address concentration helpers
p("APN blank",sum(1 for r in rows if not (r["APN"] or "").strip()),"ADDRESS blank",sum(1 for r in rows if not (r["ADDRESS"] or "").strip()))
zips=collections.Counter()
for r in rows:
    m=re.search(r"\b(\d{5})\b\s*$",(r["ADDRESS"] or "").strip())
    zips[m.group(1) if m else "NO_ZIP_IN_ADDRESS"]+=1
p("ZIP parsed from ADDRESS tail",zips.most_common(20))
streets=collections.Counter()
for r in rows:
    a=(r["ADDRESS"] or "").strip()
    streets[re.sub(r"^\d+\s+","",a).upper() if a else "BLANK"]+=1
p("STREET (address minus house number) top20",streets.most_common(20))
# status x decision
xt=collections.Counter((r["PermitStatus"],r["Decision"]) for r in rows)
p("PermitStatus x Decision",dict(sorted(xt.items(), key=lambda x: str(x[0]))))
open(os.path.join(DATA,"audit_output.txt"),"w").write("\n".join(out)+"\n")
