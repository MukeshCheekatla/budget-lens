# AP Budget 2026-27 — Batch 1 Extraction

**State:** Andhra Pradesh  
**Fiscal Year:** 2026-27  
**Batch:** Batch 1  
**Processed:** 2026-03-15  
**Branch:** `ap-budget-2026-27-batch1`

---

## Files Processed

| Volume | PDF | Rows Extracted | Output CSV |
|--------|-----|---------------|------------|
| Vol I-1 | Annual Statement of Receipts & Expenditure | 677 | `extracted/vol_I_1_annual_statement_new.csv` |
| Vol III-3 | Demands for Grants (Dept Detail) | 5,741 | `extracted/vol_III_3_demands.csv` |
| Vol III-4 | Demands for Grants (Dept Detail) | 2,953 | `extracted/vol_III_4_demands.csv` |
| Vol III-5 | Demands for Grants (Dept Detail) | 2,977 | `extracted/vol_III_5_demands.csv` |
| Vol IX | Supplementary Estimates | 198 | `extracted/vol_IX_supplementary.csv` |

**Total new rows extracted: ~12,546**  
**Normalized output: 32,546 rows** (includes previously processed volumes)

---

## Normalization

- **Input:** 5 new CSVs + previously extracted master
- **Output:** `normalized/normalized_budget_rows.csv` — 32,546 rows x 19 columns
- **Processing:** Forward-fill hierarchy, CoGA code mapping, rupee string to float conversion
- **Unit:** All amounts in Rupees (Lakhs)

---

## Validation Status

**Overall Verdict: FAIL** (2 critical blocking issues)

### Critical Issues (Blocking)

| ID | Issue | Affected Rows | Fix Required |
|----|-------|---------------|--------------|
| C-01 | `budget_estimate` NULL in 57% of data-type rows | 11,681/20,479 | Re-extract Vol III with corrected column alignment |
| C-02 | Scheme name recognizability only 31.7% | 18,174/26,599 | Expand keyword list; clean 421 artifact rows |

### Warnings (Non-blocking)

| ID | Issue |
|----|-------|
| W-01 | 120 header-bleed rows (object head names as scheme_name) |
| W-02 | 162 digit-only scheme names (amount values bleeding into name column) |
| W-03 | 830 grand-total rows tagged as `row_type='data'` |
| W-04 | `demand_no` format mixed (Roman numerals + Arabic) |
| W-05 | MH 3604 shows -Rs 22,003 Cr — verify sign against source PDF |
| W-06 | `master_file_code` only 3.2% populated |

### QA Verdict: NOT USEFUL

**Confidence Score: 70.5/100** (two critical issues override)

| Dimension | Score | Status |
|-----------|-------|--------|
| Structural Integrity | 85 | PASS |
| Department Code Validity | 85 | PASS |
| Scheme Name Validity | 50 | WARN |
| Unit Consistency | 70 | PASS |
| Amount Plausibility | 40 | WARN |
| Logical Consistency | 90 | PASS |
| Cross-check Totals | 85 | PASS |

---

## What Is Working

- Zero invalid CoGA major head codes (all in 0001-9999 range)
- All 8 key major heads confirmed present (Education 2202, Health 2210, Agriculture 2401, Irrigation 2701, Roads 3054, SC/ST 2225, Interest 2049, Power 2801)
- All key AP departments confirmed present
- Zero duplicate rows on primary key `(major_head, scheme_key, source_pdf, row_index)`
- Internal normalization accuracy: **0.00% deviation** between normalized and master for Vol I
- Vol I total expenditure Rs 3,49,208 Cr — 18.8% above announced Rs 2,94,000 Cr (attributable to Public Account flows MH 8xxx, not an extraction error)

---

## Resubmission Criteria

1. BE null rate in data rows reduced to **<30%** (from current 57%)
2. Scheme name recognizability raised to **>40%** (from current 31.7%)

---

## Next Steps

- [ ] Apply corrections from gap report (being handled in parallel)
- [ ] Re-extract Vol III with corrected column alignment
- [ ] Final reconciliation against source PDF grand totals
- [ ] Load corrected CSV to PostgreSQL
- [ ] Generate FastAPI backend routes
- [ ] Publish summary reports and civic tech dashboard content

---

## Reports

- `reports/validation_report.json` — per-file validation results
- `reports/qa_review_report.json` — QA review with confidence scores
- `reports/gap_report_summary.md` — structural audit findings
- `column_map.json` — column layout for all 5 volumes
- `processing_queue.json` — batch processing manifest
