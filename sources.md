# Sources

## Primary source for every figure in this brief

1. **Metropolitan Historic Zoning Commission Permits (Metropolitan_Historic_Zoning_Commission_Permits_view), Metropolitan Government of Nashville and Davidson County, Nashville Open Data Portal.** ArcGIS FeatureServer layer 0, services2.arcgis.com/HdTo6HJqh92wn4D8. Snapshot pulled November 9, 2026: 9,171 records, verified at pull time against the server's own returnCountOnly count (9,171). Layer metadata archived in this package at data/source-metadata-layer.json; the layer's data was last edited November 7, 2026 per the service listing (editingInfo.dataLastEditDate).
   - Service: https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Metropolitan_Historic_Zoning_Commission_Permits_view/FeatureServer/0
   - Fields used: CASE_TYPE_DESC, SUB_TYPE_DESC, DATE_ACCEPTED, DATE_ISSUED, PermitStatus, Decision, STATUS_CODE, APN, ADDRESS, CASE_NUMBER. The layer metadata names the fields but does not define the Decision or PermitStatus values; the brief records that absence and does not assign definitions the metadata does not carry.

## Comparison sources (published Machine Readable briefs only)

2. **Nashville Building Permits Issued (Machine Readable, November 3, 2026)** - median 29 days among 29,650 issued permits with valid gaps. Repository: https://github.com/adowlen/nashville-building-permits-data-brief
3. **Nashville Trade Permits (Machine Readable, November 7, 2026)** - 87.1 percent same-day among 107,210 dated permits. Repository: https://github.com/adowlen/nashville-trade-permits-data-brief
4. **Nashville Building Permit Applications (Machine Readable, November 4, 2026)** - median pending age 330 days among 6,036 not-yet-issued applications. Repository: https://github.com/adowlen/nashville-building-permit-applications-data-brief

## Repository and license

Full code, charts, panels, and verification notes: https://github.com/adowlen/nashville-historic-zoning-data-brief
Brief text and data products: CC BY 4.0 (LICENSE in the package). The underlying records are published by Metro Nashville as government open data.
