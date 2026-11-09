import csv, json, collections, os, re, statistics
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HERE=os.path.dirname(__file__); PKG=os.path.normpath(os.path.join(HERE,"..")); DATA=os.path.join(PKG,"data")
CHI=ZoneInfo("America/Chicago")
def ld(v):
    if v in (None,""): return None
    return datetime.fromtimestamp(int(float(v))/1000, tz=timezone.utc).astimezone(CHI).date()
rows=list(csv.DictReader(open(os.path.join(DATA,"nashville_historic_zoning_raw.csv"))))
def pct(n,d): return round(100*n/d,1) if d else None
def summ(gaps):
    if not gaps: return {"gap_n":0,"median_days":None,"mean_days":None,"p90_days":None,"same_day_pct":None,"over_30_pct":None,"over_90_pct":None,"max_days":None}
    s=sorted(gaps)
    p90=s[min(len(s)-1, int(0.9*len(s)))]  # nearest-rank-ish index used consistently; verifier uses same convention check tolerance
    return {"gap_n":len(gaps),"median_days":statistics.median(gaps),"mean_days":round(statistics.mean(gaps),1),"p90_days":p90,"same_day_n":sum(1 for g in gaps if g==0),"same_day_pct":pct(sum(1 for g in gaps if g==0),len(gaps)),"over_30_n":sum(1 for g in gaps if g>30),"over_30_pct":pct(sum(1 for g in gaps if g>30),len(gaps)),"over_90_pct":pct(sum(1 for g in gaps if g>90),len(gaps)),"max_days":max(gaps)}
both=[r for r in rows if ld(r["DATE_ACCEPTED"]) and ld(r["DATE_ISSUED"])]
gaps=[(ld(r["DATE_ISSUED"])-ld(r["DATE_ACCEPTED"])).days for r in both]
neg=[g for g in gaps if g<0]; nonneg=[g for g in gaps if g>=0]
dec=collections.Counter(r["Decision"] for r in rows); ps=collections.Counter(r["PermitStatus"] for r in rows); sc=collections.Counter(r["STATUS_CODE"] for r in rows)
sub=collections.Counter(r["SUB_TYPE_DESC"] for r in rows)
by_sub={}
for k in sub:
    g=[(ld(r["DATE_ISSUED"])-ld(r["DATE_ACCEPTED"])).days for r in rows if r["SUB_TYPE_DESC"]==k and r["DATE_ISSUED"]]
    g=[x for x in g if x>=0]
    by_sub[k]={"n":sub[k],"dated":len(g),**summ(g),"approved_admin_n":sum(1 for r in rows if r["SUB_TYPE_DESC"]==k and r["Decision"] in ("Approved","Administratively Approved"))}
by_dec={}
for k in dec:
    g=[(ld(r["DATE_ISSUED"])-ld(r["DATE_ACCEPTED"])).days for r in rows if r["Decision"]==k and r["DATE_ISSUED"]]
    by_dec[k]={"n":dec[k],"dated":len([x for x in g if x>=0]),**summ([x for x in g if x>=0])}
by_year={}
for r in rows:
    y=str(ld(r["DATE_ACCEPTED"]).year); by_year.setdefault(y,[]).append(r)
year_panel={y:{"n":len(v),"dated":sum(1 for r in v if r["DATE_ISSUED"]),"median_days":statistics.median([(ld(r["DATE_ISSUED"])-ld(r["DATE_ACCEPTED"])).days for r in v if r["DATE_ISSUED"]]) if any(r["DATE_ISSUED"] for r in v) else None,"approved_admin_pct":pct(sum(1 for r in v if r["Decision"] in ("Approved","Administratively Approved")),len(v))} for y,v in sorted(by_year.items())}
zips=collections.Counter()
for r in rows:
    m=re.search(r"\b(\d{5})\b\s*$",(r["ADDRESS"] or "").strip()); zips[m.group(1) if m else "NO_ZIP_IN_ADDRESS"]+=1
top_zip=zips.most_common(10)
addr=collections.Counter(r["ADDRESS"] for r in rows if (r["ADDRESS"] or "").strip())
apns=collections.Counter(r["APN"] for r in rows if (r["APN"] or "").strip())
stats={
 "dataset":"Nashville Metropolitan Historic Zoning Commission Permits (Metropolitan_Historic_Zoning_Commission_Permits_view, layer 0)",
 "snapshot_date":"2026-11-09","rows":len(rows),"unit":"one row = one historic-zoning commission permit case as served by the view",
 "server_count":9171,
 "accepted_range":[str(min(ld(r["DATE_ACCEPTED"]) for r in rows)),str(max(ld(r["DATE_ACCEPTED"]) for r in rows))],
 "issued_range":[str(min(ld(r["DATE_ISSUED"]) for r in rows if r["DATE_ISSUED"])),str(max(ld(r["DATE_ISSUED"]) for r in rows if r["DATE_ISSUED"]))],
 "case_type_counter":dict(collections.Counter(r["CASE_TYPE_DESC"] for r in rows)),
 "subtype_counter":dict(sub.most_common()),"status_code_counter":dict(sc.most_common()),
 "permit_status_counter":{k:v for k,v in ps.most_common()},"permit_status_blank_n":ps.get("",0),
 "decision_counter":dict(dec.most_common()),
 "approved_admin_n":dec.get("Approved",0)+dec.get("Administratively Approved",0),
 "approved_admin_pct_of_all":pct(dec.get("Approved",0)+dec.get("Administratively Approved",0),len(rows)),
 "disapproved_n":dec.get("Disapproved",0),"disapproved_pct_of_all":pct(dec.get("Disapproved",0),len(rows)),
 "with_issued_date_n":len(both),"with_issued_date_pct":pct(len(both),len(rows)),"without_issued_date_n":len(rows)-len(both),
 "disapproved_with_issued_date_n":sum(1 for r in rows if r["Decision"]=="Disapproved" and r["DATE_ISSUED"]),
 "issued_status_n":ps.get("Issued",0),"issued_status_and_disapproved_n":sum(1 for r in rows if r["PermitStatus"]=="Issued" and r["Decision"]=="Disapproved"),
 "gap":{"both_dates":len(both),"negative_n":len(neg),"nonneg_n":len(nonneg),**summ(nonneg),
        "median_days_if_positive":statistics.median([g for g in nonneg if g>0]) if any(g>0 for g in nonneg) else None,"positive_n":sum(1 for g in nonneg if g>0)},
 "by_subtype":by_sub,"by_decision":by_dec,"by_year_accepted":year_panel,
 "zip_counter_top10":top_zip,"zip_37206_n":zips.get("37206",0),"zip_37206_pct":pct(zips.get("37206",0),len(rows)),
 "zip_top3_n":sum(v for _,v in top_zip[:3]),"zip_top3_pct":pct(sum(v for _,v in top_zip[:3]),len(rows)),
 "address_blank_n":sum(1 for r in rows if not (r["ADDRESS"] or "").strip()),"apn_blank_n":sum(1 for r in rows if not (r["APN"] or "").strip()),
 "distinct_apn":len(apns),"distinct_address":len(addr),
 "top_address":[list(x) for x in addr.most_common(5)],"top_apn":[list(x) for x in apns.most_common(5)],
 "derived_per_year":round(len(rows)/15,1),
 "decision_by_era":{"accepted_2011_2020":{"n":sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year<=2020),"approved_admin_n":sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year<=2020 and r["Decision"] in ("Approved","Administratively Approved")),"approved_admin_pct":pct(sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year<=2020 and r["Decision"] in ("Approved","Administratively Approved")),sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year<=2020))},
   "accepted_2021_2026":{"n":sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year>=2021),"approved_admin_n":sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year>=2021 and r["Decision"] in ("Approved","Administratively Approved")),"approved_admin_pct":pct(sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year>=2021 and r["Decision"] in ("Approved","Administratively Approved")),sum(1 for r in rows if ld(r["DATE_ACCEPTED"]).year>=2021))}},
 "comparison_published":{"building_permits_issued_2026_11_03":{"median_days":29.0,"basis":"29,650 issued building permits with valid entered-to-issued gaps, rolling 3 years to 2026-11-02","repo":"https://github.com/adowlen/nashville-building-permits-data-brief"},
   "trade_permits_2026_11_07":{"same_day_pct":87.1,"basis":"107,210 dated trade permits with non-negative gaps, 2023-10-12 to 2026-10-16 entries","repo":"https://github.com/adowlen/nashville-trade-permits-data-brief"},
   "building_permit_applications_2026_11_04":{"median_pending_age_days":330,"basis":"6,036 not-yet-issued applications as of 2026-11-03","repo":"https://github.com/adowlen/nashville-building-permit-applications-data-brief"}},
}
json.dump(stats, open(os.path.join(PKG,"stats.json"),"w"), indent=2)
with open(os.path.join(DATA,"subtype_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["sub_type_desc","n","dated","median_days","same_day_pct","over_30_pct","approved_admin_n"])
    for k,v in by_sub.items(): w.writerow([k,v["n"],v["dated"],v["median_days"],v["same_day_pct"],v["over_30_pct"],v["approved_admin_n"]])
with open(os.path.join(DATA,"zip_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["zip","n"]); w.writerows(zips.most_common())
with open(os.path.join(DATA,"year_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["year_accepted","n","dated","median_days","approved_admin_pct"])
    for y,v in year_panel.items(): w.writerow([y,v["n"],v["dated"],v["median_days"],v["approved_admin_pct"]])
print(json.dumps({k:stats[k] for k in ["rows","approved_admin_pct_of_all","disapproved_pct_of_all","with_issued_date_pct","disapproved_with_issued_date_n"]},indent=1)); print(stats["gap"])
