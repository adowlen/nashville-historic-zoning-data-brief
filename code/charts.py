import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
PKG=os.path.normpath(os.path.join(os.path.dirname(__file__),"..")); S=json.load(open(os.path.join(PKG,"stats.json")))
CHAR="#232323"; AMBER="#e8a33d"; TEAL="#2a9d8f"; LIGHT="#f2f2f2"
plt.rcParams.update({"text.color":LIGHT,"axes.edgecolor":LIGHT,"axes.labelcolor":LIGHT,"xtick.color":LIGHT,"ytick.color":LIGHT,"figure.facecolor":CHAR,"axes.facecolor":CHAR,"savefig.facecolor":CHAR})
def save(fig,n): fig.tight_layout(); fig.savefig(os.path.join(PKG,"charts",n),dpi=200); plt.close(fig)
items=list(S["subtype_counter"].items())[:10][::-1]
fig,ax=plt.subplots(figsize=(8,4.8)); ax.barh([k for k,_ in items],[v for _,v in items],color=TEAL)
for i,(_,v) in enumerate(items): ax.text(v+60,i,f"{v:,}",va="center",fontsize=9)
ax.set_xlabel("Historic-zoning permit cases accepted 2011-12-07 to 2026-11-06 (all 9,171 cases)"); ax.set_title("Cases by subtype - top 10 of 15 recorded subtypes"); save(fig,"chart_subtypes_top10.png")
bt={k:v for k,v in S["by_subtype"].items() if v["dated"]>=100}
items=sorted(bt.items(), key=lambda x: x[1]["median_days"] if x[1]["median_days"] is not None else -1)[::-1]
fig,ax=plt.subplots(figsize=(8,4.8)); ax.barh([k for k,_ in items],[v["median_days"] for _,v in items],color=AMBER)
for i,(_,v) in enumerate(items): ax.text((v["median_days"] or 0)+0.7,i,f"{v['median_days']}  (dated n={v['dated']:,})",va="center",fontsize=8)
ax.set_xlabel("Median days, DATE_ACCEPTED to DATE_ISSUED (Chicago local dates; dated, non-negative gaps only)"); ax.set_title("Median acceptance-to-issuance time by subtype (subtypes with 100+ dated cases)"); save(fig,"chart_median_by_subtype.png")
labels=["Approved","Administratively Approved","Disapproved","Deferred"]; vals=[S["decision_counter"].get(k,0) for k in labels]
fig,ax=plt.subplots(figsize=(8,4.6)); ax.barh(labels[::-1],vals[::-1],color=TEAL)
for i,v in enumerate(vals[::-1]): ax.text(v+90,i,f"{v:,} ({round(100*v/S['rows'],1)}%)",va="center",fontsize=9)
ax.set_xlabel("Cases (share of all 9,171) - Decision as recorded; see brief: 4,602 Disapproved cases carry an issued date"); ax.set_title("Decision values as recorded in the register"); save(fig,"chart_decision_counter.png")
items=S["zip_counter_top10"][:8][::-1]
fig,ax=plt.subplots(figsize=(8,4.6)); ax.barh([k for k,_ in items],[v for _,v in items],color=AMBER)
for i,(_,v) in enumerate(items): ax.text(v+70,i,f"{v:,}",va="center",fontsize=9)
ax.set_xlabel("Cases (ZIP parsed from the ADDRESS field tail; 112 cases carry no ZIP in ADDRESS)"); ax.set_title("Cases concentrate by ZIP - top 8 ZIP codes"); save(fig,"chart_zip_top8.png")
print("charts done")
