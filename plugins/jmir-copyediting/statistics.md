# JMIR Guidelines for Reporting Statistics

Complete reference for formatting and reporting all statistical values in JMIR manuscripts. Based on JMIR Guidelines for Reporting Statistics and AMA Manual of Style (11th ed).

---

## §1. Omission of Leading Zero

### Rule
- **Omit** the leading zero for values that **cannot exceed 1.0**:
  - *P* values: `P=.03`, `P<.001`
  - α (alpha) values: `α=.05`
  - β (beta) values: `β=.20`
- **Retain** the leading zero for **all other** statistical values:
  - Cohen *d*: `d=0.29`
  - Cronbach α: `Cronbach α=0.78`
  - Correlation *r*: `r=0.92`
  - Hedges *g*: `g=0.45`
  - Odds ratio: `OR 0.85`
  - Any value that can exceed 1.0

---

## §2. P Values

### 2.1 Formatting
- *P* is always **italic** and **capitalized**: *P*
- No leading zero: `P=.03` (NOT `P=0.03`)
- No spaces around the operator: `P=.03`, `P<.001` (NOT `P = .03`)

### 2.2 Rounding Rules
| Condition | Rule | Example |
|-----------|------|---------|
| P ≥ .01 | Round to **2 decimal places** | `P=.04`, `P=.78` |
| P < .01 | Round to **3 decimal places** | `P=.003`, `P=.008` |
| P = 0 or P < .0001 | Report as `P<.001` | `P<.001` |
| P = 1 | Report as `P>.99` | `P>.99` |

### 2.3 Significance Preservation
- **NEVER** round P values in a way that changes statistical significance.
- `P=.046` → do NOT round to `P=.05` (this changes significance interpretation).
- `P=.037` → round to `P=.04` (this is acceptable — significance is preserved).
- `P=.045` → do NOT round to `P=.05`.

### 2.4 Asterisks for Significance
- Do NOT use asterisks (*, **, ***) to denote significance levels in tables.
- **Exceptions**: Systematic reviews or odds ratio (OR) tables may use asterisks.
- Report exact P values instead.

### 2.5 P Values in Footnotes
- Do NOT use `P≤.001` in footnotes. Provide exact P values where possible.
- If the exact value is below the threshold, use `P<.001`.

---

## §3. Spacing Around Equality and Inequality Signs

- Do **NOT** insert spaces before or after `=`, `<`, `>`, `≤`, `≥` in statistical expressions.
- Examples: `n=12`, `P<.001`, `t15=2.68`, `F2,45=3.21`, `r=0.92`
- Note: JMIR typesetting scripts automatically remove these spaces, so copyeditors do not need to invest time correcting this.
- **Exception**: Spaces ARE used in complex standalone equations: `y = C - c`

---

## §4. N and n (Sample Sizes)

### 4.1 Conventions
- **N** (capital, italic): total sample size or population.
- **n** (lowercase, italic): subsample or subgroup size.

### 4.2 Reporting Format
- Format: `n/N, %` or `n/N (%)`.
- Examples: `15/30, 50%` or `15/30 (50%)`
- Always report the **denominator** (N).
- In parentheses, n/N values precede the percentage: `(15/30, 50%)`.

### 4.3 In Tables
- Column header format: `Participants, n (%)` — do NOT use "No. of Participants".
- Percent sign appears ONLY in header, not in cell body.
- If percentages are given without n values, query authors to provide them.

---

## §5. Percentages and Decimal Places

### 5.1 Rounding Rules
| Sample Size (N) | Decimal Places | Example |
|-----------------|---------------|---------|
| N < 100 | 1 decimal place | `15/30 (50.0%)` → `50%` (see §5.2) |
| N ≥ 100 | 2 decimal places | `59/100 (59.00%)` → `59%` (see §5.2) |
| N ≥ 1000 | 2 decimal places allowed but not required | Ensure consistency |

### 5.2 Whole Percentages
- Do NOT write `.0` for whole percentages: `64%` (NOT `64.0%`).

### 5.3 Percentages in Running Text
- JMIR requires n/N values alongside percentages: `Of the 80% (40/50) of participants...`
- Use the percent sign without a space: `58%`
- Repeat percent sign in ranges: `24%-29%` (NOT `24-29%`)

---

## §6. Mean, Standard Deviation, Standard Error, and Range

### 6.1 Formatting
| Statistic | Format | Example |
|-----------|--------|---------|
| Mean and SD | `mean (SD)` | `45.3 (12.7)` |
| Mean and SE | `mean (SE)` | `45.3 (2.1)` |
| Mean and range | `mean (range min-max)` | `45.3 (range 20-68)` |

### 6.2 In Tables
- Group mean/SD in a single cell: `mean (SD)`.
- Column header should specify: `Score, mean (SD)`.

---

## §7. Odds Ratio and Confidence Interval

### 7.1 Formatting
- Format: `OR value (95% CI lower-upper)`
- Example: `OR 2.45 (95% CI 1.23-4.89)`
- In tables: `OR (95% CI)` in column header.
- Retain leading zero for OR values: `OR 0.85` (NOT `OR .85`).

### 7.2 Other Ratio/Risk Measures
- Same formatting applies to: hazard ratio (HR), relative risk (RR), risk ratio, rate ratio.
- Example: `HR 1.32 (95% CI 1.05-1.67)`

---

## §8. Interquartile Range (IQR)

- Format: `median (IQR value-value)` or `median (Q1-Q3)`.
- Example: `median 45 (IQR 32-58)`
- IQR does NOT need expansion (on the no-expansion list).

---

## §9. Chi-Square Test

- Use the symbol χ² (Greek chi, superscript 2).
- Italic: *χ²*
- Include degrees of freedom as subscript: χ²₁ or in text as `χ²1`
- Format: `χ²1=4.56`, `P=.03`
- The word form is "chi-square test" (hyphenated, lowercase).

---

## §10. t Test

- Two words, no hyphen: **t test** (NOT "t-test").
- *t* is **italic** and lowercase.
- Include degrees of freedom as subscript: *t*₁₅ or in text as `t15`.
- Format: `t15=2.68`, `P=.01`
- No possessive: it is NOT "Student's t test" — use `t test`.

---

## §11. F Test

- *F* is **italic** and capitalized.
- Include degrees of freedom (numerator, denominator) as subscripts: F₂,₄₅ or in text as `F2,45`.
- Format: `F2,45=3.21`, `P=.049`

---

## §12. Effect Size

### 12.1 Cohen d
- *d* is **italic** and lowercase.
- **No possessive**: `Cohen d` (NOT "Cohen's d").
- Retain leading zero: `Cohen d=0.29` (NOT `Cohen d=.29`).
- Format: `d=0.29`

### 12.2 Hedges g
- *g* is **italic** and lowercase.
- **No possessive**: `Hedges g` (NOT "Hedges' g").
- Retain leading zero: `g=0.45`.

### 12.3 Eta-squared (η²)
- η² is italic: *η²*
- Retain leading zero: `η²=0.12`

---

## §13. Cronbach Alpha

- **No possessive**: `Cronbach α` (NOT "Cronbach's alpha" or "Cronbach's α").
- α is the Greek letter alpha (not italic in this context).
- Retain leading zero: `Cronbach α=0.78` (NOT `.78`).
- Note: When Cronbach α is used as a statistical test value, the leading zero is retained because α in this context refers to the reliability coefficient (which can range from 0 to 1 and is different from the α significance level).

---

## §14. Beta Level (β)

- β is the Greek letter beta.
- When referring to the **significance level** (probability of Type II error): omit leading zero: `β=.20`
- When referring to **regression coefficients** (standardized β): retain leading zero if the context is a regression coefficient that can exceed 1: `β=0.45`
- Context determines the rule — significance-level β omits the zero; regression β retains it.

---

## §15. Spearman Rank Correlation

- Use ρ (Greek rho) or *r*ₛ (italic r with subscript s).
- Format: `ρ=0.67` or `rs=0.67`
- Retain leading zero (correlation can range from –1 to +1, so it CAN equal 1).
- **No possessive**: `Spearman rank correlation` (NOT "Spearman's").

---

## §16. Kappa Statistic (κ)

- κ is the Greek letter kappa (italic).
- Retain leading zero: `κ=0.82`
- Format: `κ=0.82 (95% CI 0.71-0.93)`
- **No possessive**: `Cohen κ` or just `κ` (NOT "Cohen's kappa").

---

## §17. Correlation Coefficient (r)

- *r* is **italic** and lowercase.
- Retain leading zero: `r=0.92`
- For Pearson correlation: `r=0.92`, `P<.001`
- R² (coefficient of determination): *R²*=0.85

---

## §18. Greek Letters in Statistics

### General Rules
- Greek letters used as statistical symbols follow AMA conventions.
- Common statistical Greek letters: α (alpha), β (beta), χ² (chi-square), η² (eta-squared), κ (kappa), ρ (rho), σ (sigma).
- Do NOT use the English word when the Greek symbol is available (eg, use `α` not "alpha" in formulas).
- In running text, spelling out is acceptable: "the Cronbach alpha was .78."

### Leading Zero Rules for Greek Letters
| Symbol | Context | Leading Zero? | Example |
|--------|---------|--------------|---------|
| α | Significance level | Omit | `α=.05` |
| α | Cronbach reliability | Retain | `Cronbach α=0.78` |
| β | Significance level (Type II error) | Omit | `β=.20` |
| β | Regression coefficient | Retain | `β=0.45` |
| κ | Agreement statistic | Retain | `κ=0.82` |
| ρ | Correlation | Retain | `ρ=0.67` |

---

## §19. Eponymous Tests — No Possessives

Remove possessives from ALL eponymous statistical test and measure names:

| ❌ Incorrect | ✅ Correct |
|-------------|-----------|
| Student's t test | t test |
| Cohen's d | Cohen d |
| Cohen's kappa | Cohen κ |
| Hedges' g | Hedges g |
| Cronbach's alpha | Cronbach α or Cronbach alpha |
| Spearman's rho | Spearman ρ or Spearman rank correlation |
| Pearson's r | Pearson r |
| Fisher's exact test | Fisher exact test |
| Mann-Whitney's U | Mann-Whitney U test |
| Wilcoxon's test | Wilcoxon test |
| Bonferroni's correction | Bonferroni correction |
| Tukey's test | Tukey test |
| Levene's test | Levene test |

---

## §20. Currency

- Use standard currency symbols: $ (USD), € (EUR), £ (GBP), ¥ (JPY/CNY).
- Place the symbol before the number with no space: `$500`, `€1200`.
- Specify the currency if not obvious from context: `US $500`, `CA $300`.
- Large amounts: `$2.5 million` (NOT `$2,500,000` in running text).

---

## §21. Complex Equations

- For complex standalone equations/formulas, spaces ARE used around operators: `y = C - c`
- This is the exception to the general no-space rule for equality signs.
- Equations should be centered and numbered if referenced in text.
- Variables should be italicized.
- Use standard mathematical notation.

---

## §22. "Trending Towards Significance"

- Do NOT use the phrase "trending towards significance" or similar hedging language.
- Report exact P values and let the reader interpret.
- If P is between .05 and .10, report the exact value: `P=.07`.
- Use language like "did not reach statistical significance" or "was not statistically significant" if needed.

---

## §23. Correlation Tables

- Correlation values and P values should appear in **separate rows** in correlation tables (not in the same cell).
- Do not combine `r=0.45, P<.001` in a single cell — use two rows.

---

## §24. Quick Reference: Italicization of Statistical Symbols

| Symbol | Italic? | Example |
|--------|---------|---------|
| *P* | Yes | *P*=.03 |
| *t* | Yes | *t*15=2.68 |
| *F* | Yes | *F*2,45=3.21 |
| *r* | Yes | *r*=0.92 |
| *R²* | Yes | *R²*=0.85 |
| *d* | Yes | Cohen *d*=0.29 |
| *g* | Yes | Hedges *g*=0.45 |
| *U* | Yes | Mann-Whitney *U* |
| *n* / *N* | Yes | *n*=50, *N*=200 |
| *z* | Yes | *z*=1.96 |
| *χ²* | Yes | *χ²*1=4.56 |
| *η²* | Yes | *η²*=0.12 |
| *κ* | Yes | *κ*=0.82 |
| *ρ* | Yes | *ρ*=0.67 |
| α (significance) | No | α=.05 |
| β (significance) | No | β=.20 |
| OR | No | OR 2.45 |
| CI | No | 95% CI |
| HR, RR | No | HR 1.32 |
| SD, SE, SEM | No | mean (SD) |
| IQR | No | IQR 32-58 |

