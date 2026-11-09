# Second implementation (pandas) + live server count; independent of build_stats.py
import pandas as pd, json, os, urllib.request, urllib.parse
PKG=os.path.normpath(os.path.join(os.path.dirname(__file__),".."))
S=json.load(open(os.path.join(PKG,"stats.json")))
df=pd.read_csv(os.path.join(PKG,"data","nashville_historic_zoning_raw.csv"))
chi="America/Chicago"
acc=pd.to_datetime(df["DATE_ACCEPTED"], unit="ms", utc=True).dt.tz_convert(chi).dt.date
iss=pd.to_datetime(df["DATE_ISSUED"], unit="ms", utc=True).dt.tz_convert(chi).dt.date
gap=(iss-acc).apply(lambda x: x.days if pd.notna(x) else None)
checks=[]
def chk(name, got, want): checks.append({"check":name,"got":got,"want":want,"pass":bool(got==want)})
chk("rows", len(df), S["rows"])
chk("server_count_live", json.load(urllib.request.urlopen("https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Metropolitan_Historic_Zoning_Commission_Permits_view/FeatureServer/0/query?"+urllib.parse.urlencode({"where":"1=1","returnCountOnly":"true","f":"json"}), timeout=60))["count"], S["server_count"])
chk("with_issued", int(iss.notna().sum()), S["with_issued_date_n"])
g=gap.dropna(); g=g[g>=0]
chk("gap_n", len(g), S["gap"]["nonneg_n"]); chk("gap_negative", int((gap.dropna()<0).sum()), S["gap"]["negative_n"])
chk("median", float(g.median()), float(S["gap"]["median_days"])); chk("same_day_n", int((g==0).sum()), S["gap"]["same_day_n"])
chk("same_day_pct", round(100*(g==0).mean(),1), S["gap"]["same_day_pct"]); chk("over_30_n", int((g>30).sum()), S["gap"]["over_30_n"])
chk("median_if_positive", float(g[g>0].median()), float(S["gap"]["median_days_if_positive"]))
dec=df["Decision"].value_counts(dropna=False).to_dict()
chk("approved_admin_n", int(dec.get("Approved",0)+dec.get("Administratively Approved",0)), S["approved_admin_n"])
chk("disapproved_n", int(dec.get("Disapproved",0)), S["disapproved_n"])
chk("disapproved_with_issued", int(((df["Decision"]=="Disapproved")&iss.notna()).sum()), S["disapproved_with_issued_date_n"])
chk("issued_status_n", int((df["PermitStatus"]=="Issued").sum()), S["issued_status_n"])
chk("subtype_top_n", int(df["SUB_TYPE_DESC"].value_counts().iloc[0]), S["subtype_counter"]["Historic New Construction"])
z=df["ADDRESS"].fillna("").str.extract(r"(\d{5})\s*$")[0].value_counts()
chk("zip_37206_n", int(z.get("37206",0)), S["zip_37206_n"])
chk("accepted_min", str(acc.min()), S["accepted_range"][0]); chk("accepted_max", str(acc.max()), S["accepted_range"][1])
res={"checks":checks,"pass":sum(1 for c in checks if c["pass"]),"total":len(checks)}
json.dump(res, open(os.path.join(PKG,"data","verify_independent_output.json"),"w"), indent=2)
print(res["pass"],"/",res["total"]); [print("FAIL",c) for c in checks if not c["pass"]]
