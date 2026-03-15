# AP Budget 2026-27 Gap Report Summary

**Generated:** 2026-03-16  
**State:** Andhra Pradesh  
**Fiscal Year:** 2026-27  
**Batch:** Batch 1 (Vol I-1, III-3/4/5, IX)

## Structural Audit Findings

### Missing Values
- `budget_estimate` NULL in **57.0%** of data-type rows (11,681 of 20,479)
- `demand_no` NULL in **64.9%** of rows (expected for summary volumes)
- `department_name` NULL in **9.2%** of rows
- `master_file_code` populated in only **3.2%** of rows

### Unmapped / Invalid Codes
- **200 invalid CoGA codes** in vol_I_1 (Roman numerals: I, A, (a) extracted as codes)
- **200 invalid CoGA codes** in vol_III_3 (object head labels like "011 Pay" extracted as codes)
- **200 invalid CoGA codes** in vol_III_4 and vol_III_5 (same issue)
- **200 invalid CoGA codes** in master_budget ("Total" labels in code column)

### Orphaned / Bleed Rows
- **120 header-bleed rows**: object head names appearing as scheme_name values
- **162 digit-only scheme names**: amount values bleeding into scheme_name column
- **259 scheme names <=2 chars**: sub-item indicators extracted as scheme names
- **830 grand-total rows** incorrectly tagged as `row_type='data'`

### Duplicates
- normalized_budget_rows: 31,537 apparent duplicates (96.9%) — false positives due to narrow dedup key; actual issue is missing `source_pdf` + `demand_no` in key
- vol_III_3: 3,478 duplicates (60.6%) on (object_head_code, BE, demand_no, dept)
- vol_III_4: 2,088 duplicates (70.7%)
- vol_III_5: 2,030 duplicates (68.2%)
- master_budget: 18,728 duplicates (93.5%) on (code, BE)

### Total Mismatches
- Vol I total expenditure: Rs 3,49,208 Cr vs public announced Rs 2,94,000 Cr (+18.8%)
- Deviation attributable to Public Account flows (MH 8xxx) — not an extraction error
- Internal normalization accuracy: **0.00% deviation** between normalized and master for Vol I

## Corrections Required

| Priority | Issue | Action |
|----------|-------|--------|
| P1 | BE null 57% in data rows | Re-extract Vol III with corrected column alignment |
| P2 | Scheme name artifacts | Remove digit-only, <=2char, and object-head bleed rows |
| P3 | Grand-total rows as 'data' | Reclassify rows where BE > 5,00,00,000 Lakhs |
| P4 | demand_no format mixed | Standardize to integer (convert Roman numerals) |
| P5 | MH 3604 negative -Rs 22,003 Cr | Verify sign against source PDF |
| P6 | master code column 3.2% populated | Re-extract Vol I preserving code field |

## Resubmission Criteria
1. BE null rate in data rows reduced to **<30%**
2. Scheme name recognizability raised to **>40%**
