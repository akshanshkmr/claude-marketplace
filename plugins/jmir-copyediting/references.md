# JMIR Reference Formatting Guidelines

Complete reference for formatting in-text citations and compiling the bibliography using RefCheck (OJS) and the Kriyadocs Reference Editor. Based on JMIR House Style and AMA Manual of Style (11th ed).

---

## Section 1: In-text Citations

### 1.1 Formatting & Syntax
* **Square brackets**: Cite references using square brackets before punctuation marks (eg, `...as noted in several studies [3,4].`).
* **Spaces**: Place a single space before the opening bracket. Do not place a space between the closing bracket and the subsequent punctuation mark (eg, `...described previously [8]; however, ...`).
* **Multiple citations**: Separate multiple citations with a comma and **no space** (eg, `[1,5]`).
* **Ranges**: Use a hyphen for inclusive ranges (eg, `[1-3]`).
* **Clean brackets**: Do not include any text other than citation numbers inside the brackets.
  * **Incorrect**: `[56; see also Multimedia Appendix 2]`
  * **Correct**: `[56] (see also Multimedia Appendix 2)`

### 1.2 Placement
* **In body text**: Place citations before punctuation marks (periods, commas, semicolons, colons).
  * *Example*: `...numbers [13] would not justify...`
  * *Example*: `...words [13]. This is...`
  * *Example*: `...protocol [13], but did not...`
  * *Example*: `...data [13]; however, ...`
  * *Example*: `...noted in several studies (eg, [20,32-34]), highlighting...`
* **In tables**: Citations may be included in tables. When citing a list of publications in a review table, present the citation with the authors' names. If the publication year is included, place it after the citation.
  * *Example*: `Harrison et al [3], 2000` (Inclusion of the year is optional but can be retained if provided).
* **In figures**:
  * All references for a figure must be included in the **figure caption only**, not inside the figure image (since figures are static and cannot be renumbered).
  * If a reference is cited *only* in a figure caption (or if other mentions of it in the text appear only after the figure callout), cite this reference:
    1. In the figure caption on OJS/Kriyadocs.
    2. Alongside the first in-text callout of the figure. Do not retain the figure caption in the manuscript document.
    3. Flag these references for the production editor in the Layout Comments box.
* **Table/figure source data**:
  * If data in a table/figure is from a source already cited in the main text, reuse that reference number in the table/figure caption.
  * If the reference pertains *only* to the table/figure, number it according to the first mention of the table/figure in the text. Add the citation number in the table/figure (at the relevant position) and/or caption to ensure it links to the reference list.

### 1.3 Author Names in Body Text
* **One author**: Use the surname (eg, `Stewart [12] reported...`).
* **Two authors**: Use both surnames (eg, `Smith and Johnston [15] found...` or `Eysenbach and Jadad [16] argued...`).
* **More than two authors**: Always use the first author's surname followed by "`et al`" or "`and colleagues`" (eg, `Burrows et al [27] showed...`).
* **Styling**: Do not italicize and do not place a period after "et al" (eg, `et al [27]`, not `*et al.* [27]`). This rule applies to the main text, tables, and figure captions.

### 1.4 Web Pages and URLs in Body Text
* All URLs in the main text or tables must be **eliminated** or **converted to in-text citations** and included in the reference list.
* *Exception*: URLs inside direct quotes may be retained if they do not disrupt formatting or page margins.

---

## Section 2: Reference Identifiers & Field Codes

### 2.1 Database Identifiers (PMID, DOI, ISBN)
For best results in RefCheck, ensure references have identifiers appended to the end of the citation in the MS Word file.
* **PMID (PubMed Identifier)**: Add manually at the end of journal references.
  * *Correct format*: `PMID:1234567` or `PMID: 1234567` (no brackets/punctuation).
  * *Alternative*: Append a direct Medline link (eg, `http://pubmed.gov/1234567` or `http://www.ncbi.nlm.nih.gov/pubmed/1234567`). Do not use search URLs containing `cmd=Search`.
* **DOI (Digital Object Identifier)**: Check DOIs in PubMed or CrossRef. If a DOI is not recognized by RefCheck, search at [CrossRef](http://crossref.org/) to verify.
* **ISBN (International Standard Book Number)**: For book references, append `ISBN:123456789X` or `ISBN: 123456789X`.

### 2.2 Removal of Reference Manager Field Codes
Before copyediting, remove all hidden links/field codes (from EndNote, Mendeley, Zotero, etc.) which appear with grey backgrounds:
1. Select all text (`Ctrl+A` or `Cmd+A`).
2. Press `Ctrl+Shift+F9` (Windows) or `Cmd+6` (macOS) to unlink all fields.
3. If this fails, copy all text and paste it into a plain text editor (like Notepad), then copy it back into a new MS Word document to strip all field codes.

---

## Section 3: Reference Types & Styling Rules

### 3.1 Journal References
* **Casing**: Article titles must be in **sentence case** (only capitalize the first word and proper nouns).
* **Identifiers**: A PMID or DOI must be provided for all journal references where applicable.
* **Journal abbreviations**: Journal names in RefCheck must use the official abbreviation listed in PubMed. If a journal name is spelled out in full, look up the abbreviation and replace it.
* **Newspaper articles**: Offline newspaper articles follow the same format as journal articles.
* *Example*:
  > Ellimoottil C, An L, Moyer M, Sossong S, Hollander JE. Challenges and opportunities faced by large health systems implementing telehealth. Health Aff (Millwood) 2018 Dec; 37(12):1955-1959
* *Example*:
  > Westberg EE, Miller RA. The basis for using the Internet to support the information needs of primary care. J Am Med Inform Assoc 1999 Jan-Feb; 6(1):6-25

### 3.2 Unpublished Journal Articles
* **Submitted / Under peer-review**:
  * **Never** add submitted, unaccepted articles to the References list.
  * Cite them *only* in the text per AMA style.
  * *Example*: `These findings have recently been corroborated (HE Marman, MD, unpublished data, January 2015).`
  * *Example*: `Similar findings have been noted by Roberts [6] and HE Marman, MD (unpublished data, 2015).`
* **Accepted (In Press)**:
  * Cite accepted articles as "`forthcoming`".
  * In RefCheck/Kriyadocs: Add the word `(forthcoming)` in parentheses in the **Source Title** field after the journal name (eg, `J Med Internet Res (forthcoming)`).
  * If a companion paper in the same journal issue is cited, it must be cited properly as forthcoming; do not use vague phrases like "as the companion paper in this issue shows...".
  * Update any references previously marked as "forthcoming" to their final published details (adding PMID/DOI) if they have been published by the time of copyediting.

### 3.3 Preprints
* **OJS/RefCheck Workflow**:
  * Format preprint references as journal references in RefCheck.
  * Because RefCheck requires a year and page numbers for journal references, use **2021** as a filler year and **0** as a filler page number.
  * Leave a note for the production editor in the Layout Comments:
    > Some references are preprint references (search with CTRL+F for "preprint"). Please delete the filler year "2021" and page number "0" for these references in the XML.
  * In Step 1, verify if the preprint has already been published. If so, query authors to cite the published version.
* **Kriyadocs Workflow**:
  * Select **Preprint** as the reference type.
  * Fill out the mandatory fields: Author, Title (add `[Article in Specify Language]` to end for non-English), Source, URL + accessed date, Issued year.
  * Add PMID, DOI, issued month, or issued day if available.

### 3.4 Retracted References
* **OJS/RefCheck Workflow**:
  * RefCheck does not automatically display retraction notices.
  * Retracted references must explicitly show details of the retraction in **bold** at the end of the reference.
  * *Example*:
    > Morisky DE, Ang A, Krousel-Wood M, Ward HJ. Predictive validity of a medication adherence measure in an outpatient setting. J Clin Hypertens (Greenwich). May 2008;10(5):348-354. **Retracted in: J Clin Hypertens (Greenwich). 2023 Sep;25(9):889. J Clin Hypertens (Greenwich). 2023 Sep;25(9):890. [doi: 10.1111/jch.14718] [Medline: 37594022]**
  * Leave a note for the production editor in the Layout Comments:
    > Ref [X] needs manual tweaking. Please add the following to the end of the reference: "Retracted in: J Clin Hypertens (Greenwich). 2023 Sep;25(9):889. J Clin Hypertens (Greenwich). 2023 Sep;25(9):890."
* **Kriyadocs Workflow**:
  * Select **Journal** as the reference type.
  * Press "Validate data" to populate all fields associated with the original article.
  * Remove the original article's DOI/PMID from their fields.
  * Add retraction details in the **Retract Journal** field (include journal title, year, volume, issue, page first/last, DOI, PMID as available).
  * Add the retraction's own DOI/PMID in a separate DOI/PMID field to ensure proper hyperlinking.
  * Press Save.

### 3.5 Web References (including Gray Literature)
* **Scope**: All webpage citations, government reports, Pew Internet Research reports, and other gray literature.
* **URL requirement**: Provide a direct URL linking to the source or PDF.
* **Access dates**: Access dates are **mandatory** for all web references. If missing, insert the date you reviewed and verified the link (format: `YYYY-MM-DD` or `[accessed YYYY-MM-DD]`).
* **Casing**: Titles must be in **sentence case**.
* **Software**: Cite as a web reference *only* if the software is the primary subject of the paper. If mentioned in passing, refer to it in the Methods section with the developer's information in parentheses (eg, `SPSS, version 24.0 (IBM Corporation)`).
* *Example (Organization)*:
  > China Internet Network Information Center. 2020. The 45th China statistical report on internet development in China in Chinese [accessed 2020-04-28] https://cnnic.com.cn/IDR/ReportDownloads/201911/P020191112539794960687.pdf
* *Example (Article)*:
  > Belmonte A. Yahoo Finance. 2020 Mar 13. Don't believe the numbers you see?: Johns Hopkins professor says up to 500,000 Americans have coronavirus [accessed 2020-04-27] https://finance.yahoo.com/news/marty-makary-on-coronavirus-in-the-us-183558545.html
* *Example (Pew Report)*:
  > Lenhart A, Horrigan J, Rainie L, et al. The ever-shifting internet population: a new look at Internet access and the digital divide. Pew Research Center Internet & Technology. Washington, DC: Pew Internet & American Life Project; 2003 Apr 1. https://www.pewresearch.org/internet/2003/04/16/the-ever-shifting-internet-population-a-new-look-at-internet-access-and-the-digital-divide/

### 3.6 Social Media References
Tag all social media references as **web references** in RefCheck/Kriyadocs using these specific formats:
* **Facebook**: Limit post content to the first meaningful stand-alone sentence or phrase, followed by an ellipsis.
  * *Format*: `Mayo Clinic Sports Medicine Facebook page. #RotatorCuff tears are among the most common shoulder injuries... March 4, 2019. URL: https://www.facebook.com/mayoclinicsportsmedicine [Accessed 2019-05-04]`
* **Blog**:
  * *Format*: `Gray T. Advice after mischief is like medicine after death. AMA Style Insider blog. February 11, 2019. URL: https://amastyleinsider.com/2019/02/11/advice-after-mischief-is-like-medicine-after-death/ [Accessed 2019-03-10]`
* **YouTube Video**:
  * *Format*: `SciComm teaser: patient-led mass screening for atrial fibrillation in seniors using handheld ECGs. JMIR Publications YouTube page. April 11, 2022. URL: https://www.youtube.com/watch?v=l3PeFOS7awE [accessed 2022-08-10]`
* **YouTube Channel**:
  * *Format*: `Khan Academy Health and Medicine YouTube page. URL: https://www.youtube.com/user/khanacademymedicine [Accessed 2016-02-10]`
* **X (formerly Twitter)**: Include the entire post content in the reference.
  * *Format*: `@AMAManual. Double negatives can be used to express a positive, but this yields a weaker affirmative than the simpler positive and may be confusing. “Our results are not inconsistent with the prior hypothesis.” “That won’t do you no good.” And the classic: “I can’t get no satisfaction.” March 7, 2019. URL: https://x.com/AMAManual/status/1103678998327017483 [Accessed 2019-03-10]`

### 3.7 Mobile Applications (Apps)
* Query authors for the link to the app (app store or website) and format as a standard web reference.
* **If the app no longer exists (no URL)**:
  * Tag as a web reference.
  * Title: App Name.
  * Source Title: Developer's Name.
  * Year: Issued Year (query authors if unknown).
  * Web Page: Use a placeholder URL (eg, `https://www.google.com/`).
  * Access Date: Use today's date.
  * Leave a note for the production editor in the Layout Comments:
    > Please remove the URL and access date for the app reference in Ref [X] (app no longer exists online).

### 3.8 Books & Book Chapters
* **ISBN**: Provision of an ISBN is highly recommended to auto-populate fields in RefCheck/Kriyadocs. If missing in Step 1, query the author in Step 2 or search at [ISBNDB](http://isbndb.com/) to add it manually in Step 3.
* **Casing**:
  * Book titles must be in **title case** (headline style).
  * Book chapter titles must be in **sentence case**.
* **Chapter details**: Manually confirm and edit the Chapter Title, Page First, and Page Last fields.
* **Dissertations/theses**: Offline dissertations/theses follow the book format.
* *Example (Book)*:
  > McKenzie J, Neiger B, Thackeray R. Planning, Implementing, and Evaluating Health Promotion Programs: A Primer. 7th Edition. New York, NY: Pearson; 2017.
* *Example (Book Chapter)*:
  > Vanderpool D. An overview of practicing high quality telepsychiatry. In: Dewan N, Luo J, Lorenzi NG, editors. Mental Health Practice in a Digital World. Health Informatics. Cham, Switzerland: Springer; 2015 Feb 14. p. 159-181.

### 3.9 Dissertations and Theses
* **Online**: Format as a webpage/web reference. Add `[dissertation]` or `[Master's thesis]` in square brackets at the end of the title.
  * *Example*: `Ghanbari S. 2014. Integration of the arts in STEM: A collective case study of two interdisciplinary university programs [dissertation]. University of California. [accessed 2016-10-14] http://escholarship.org/uc/item/9wp9x8sj`
* **Offline**: Format as a book reference.
  * *Example*: `Borton M. Infant Sleep and Feeding: A Telephone Survey of Hispanic Americans [dissertation]. Mount Pleasant, MI: Central Michigan University; 2002.`

### 3.10 Conference Proceedings
* **Recognition**: Kriyadocs/RefCheck scripts look for the phrase "Proceedings of [the] CONFERENCE NAME".
* **Formatting**:
  * Add `[Poster]`, `[Abstract]`, or `[Webinar]` to the end of the Title field as appropriate.
  * Conference dates must follow the format: `Month date/date range, year` (eg, `May 13, 2006` or `September 22-23, 2011`).
  * Virtual events: Omit the "Conference location" field.
  * Published presentations: If you see publisher information, reformat as a Book or Journal reference to align with AMA guidelines.
* *Example*:
  > Resnick ML. The effect of affect: decision making in the emotional context of health care. In: Proceedings of the 2012 Symposium on Human Factors and Ergonomics in Health Care: Bridging the Gap. Human Factors and Ergonomics Society; 2012. p. 39-44. URL: https://api.semanticscholar.org/CorpusID:17277286 [Accessed 2024-06-06]
* *Example*:
  > Kimura J, Shibasaki H, editors. Recent advances in clinical neurophysiology. Proceedings of the 10th International Congress of EMG and Clinical Neurophysiology; 1995 Oct 15-19; Kyoto, Japan. Amsterdam: Elsevier; 1996.

### 3.11 Reports
* Select **Report** as the reference type.
* If the Publisher is the same as the Author (or Collaboration Author), fill in *only* the Publisher field to avoid duplication.
* Publisher location information is not required.
* URL and accessed date are **mandatory** for online reports.

### 3.12 Patents
* Select **Patent** as the reference type.
* URL and accessed date are **mandatory** for patents retrievable online.

---

## Section 4: Platform Workflows

### 4.1 OJS / RefCheck Workflow
* **Hyphenated first names**: The first letter of both parts of a hyphenated first name are included in the initials, but the hyphen is removed (eg, Ka-Wai Tam becomes `Tam KW`).
* **Missing Author**: If a journal reference has no author listed, enter "`No author listed`" in the author field. Leave a Layout Comment for the production editor to remove this text.
* **Mononyms**: If the author's name is a mononym (single name), enter the name in the "Last Name" field and leave the "First Name" field blank. Leave a Layout Comment for the production editor.
* **Adding references**: Copyeditors can add a new reference to RefCheck for the author. It is added as the last reference and then renumbered automatically during typesetting.
* **Deleting references**: Simply delete the in-text citation from the Word manuscript. Do not manually renumber citations; they will be automatically renumbered during XML conversion.
* **Reordering references**: Authors may reorder paragraphs and citations without changing the numbering. The typesetting script automatically renumbers the references in numerical order.

### 4.2 Kriyadocs Reference Editor Workflow
When checking and reviewing references in Kriyadocs, follow this step-by-step process:
1. Click on the reference in the reference list.
2. Click **Edit** to open the Edit Reference window.
3. Ensure at least one identifier is present (DOI, PMID, URL, etc.).
4. Click **Validate**. Do **not** click "Retain Edits" yet, as this freezes the title and prevents automated corrections from database lookup. (Note: "Save" only saves changes without running automated styling, whereas "Validate" runs styling).
5. If contradicting info is found, review changes, click **Run styling** to format according to AMA/JMIR style, and proceed to the Final Styled Reference window. If no contradicting info is found, it automatically goes to the Final Styled Reference window.
6. Click the **Retain Edits** box for titles to lock in the correct sentence case.
7. Perform a visual check. Add or remove fields as required (refer to type-specific fields below) and search the original source via PubMed/Google to verify accuracy.
8. If the original source cannot be found, add an Author Query (AQ).
9. Click **Accept Reference** to save.

#### Kriyadocs Field Mapping Table

During review, ensure mandatory fields are populated, and remove any fields not listed below for that reference type:

| Reference Type | Mandatory Fields | Add if Available / Optional | Special Instructions |
| :--- | :--- | :--- | :--- |
| **Journal** | Author, Article title, Journal title, Issued year | Volume, Issue, Issued month, Issued day, Collaboration author, Page first, Page last, DOI, PMID, or URL (+ accessed date) | Sentence case for titles. Non-English: add `[Article in Language]` to title. |
| **Book** | Book title, Issued year, Publisher | Author, Collaboration author, Editor, Edition, Volume, Issue, ISBN, URL (+ accessed date), DOI, Chapter title, Page first, Page last | Title case for Book title. Non-English: add `[Book in Language]` to title. |
| **Book Chapter** | Author, Book title, Chapter title, Issued year, Publisher, Page first, Page last | Collaboration author, Editor, Edition, ISBN, URL (+ accessed date), DOI | Sentence case for chapter title, title case for book title. |
| **Website** | Webpage title, Website title, URL, Accessed date | Author, Collaboration author, Issued year, Issued month, Issued day | Sentence case for webpage title. Webinars: add `[Webinar]` to website title. |
| **Proceeding** | Title, Conference name, Event date | Author, Collaboration author, Page first, Page last, DOI, PMID, URL (+ accessed date), Conference location | Add `[Poster]`, `[Abstract]`, or `[Webinar]` to Title. Virtual: omit location. |
| **Preprint** | Author, Title, Source, URL + accessed date, Issued year | Collaboration author, PMID, DOI, Issued month, Issued day | Non-English: add `[Article in Language]` to title. |
| **Thesis / Dissertation** | Author, Title, Publisher, Issued year | URL + accessed date | Add `[Dissertation]` or `[Master's thesis]` to Title. |
| **Report** | Title, Issued year, Publisher | Author, Collaboration author, Report number, Series, Editor, URL + accessed date | Publisher same as Author: omit Author. URL mandatory if online. |
| **Patent** | Inventor, Patent title, Patent number, Issued year | Assignee, URL + accessed date, Issued month, Issued day | URL mandatory if online. |

#### Kriyadocs Special Cases
* **Mononyms**: Use the "Author" field (not "Collaboration Author"). Enter the mononym in the **Surname** field, enter a temporary placeholder (eg, "X") in the **Given name** field, click **Save**, then edit the reference again and delete the placeholder in the Given name field.
* **Inclusive page numbers**: Retain letter prefix (eg, `110-119` or `e110-e119`).

