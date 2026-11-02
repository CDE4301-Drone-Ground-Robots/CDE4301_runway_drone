# Timeline schedule data

`gantt.json` is bundled into the existing Timeline page. It was extracted from
`CDE4301_runway_patrol_gantt.xlsx`, worksheet `Gantt Chart`, with no runtime Excel
dependency. Only Arun (32–45), Charan (46–61) and Talitha (62–73) are included.
Column numbers are the original one-based Excel columns, including non-teaching
weeks: Semester 1 is D–Q (14 columns); Semester 2 is R–AL (21 columns).

Descriptions retain workbook spelling and whitespace. Categories follow the
column C category at each activity's anchor row. Each activity records its source
cell or merged range. Horizontal merged widths determine the start/end columns;
vertical merges do not create additional activities.

`gantt-display.js` applies the requested editorial corrections, sentence case and
consistent week labels to bars and tooltips. It preserves technical names and
acronyms and renames Charan's Calculations category to Camera Integration in both
semesters. Source text remains in `gantt.json`; schedule coordinates are unchanged.

Two workbook details require explicit handling:

- H48:I50 is unmerged. H48 and H49 contain consecutive lines of one description
  in the two-week H–I activity block. The lines are joined with a newline.
- P32:P84 and Q32:Q84 are milestones merged across all three member sections.
  Each member displays these under the UI grouping “Shared milestone”. This
  grouping explains the original shared cells; it is not a new scheduled task.

To regenerate from the same workbook layout, run from the repository root in
PowerShell (the extractor uses .NET ZIP/XML support, without installing libraries):

```powershell
.\website\scripts\inspect-gantt.ps1 -Workbook 'C:\path\CDE4301_runway_patrol_gantt.xlsx' |
  Set-Content -Encoding utf8 "$env:TEMP\cde4301-gantt-raw.json"
node website/scripts/build-gantt-data.mjs "$env:TEMP\cde4301-gantt-raw.json"
```

The extractor currently targets the verified workbook's second worksheet. Review
the sheet mapping and the two exceptions above if replacing the workbook with a
different layout. Excel content is treated as schedule data, never as instructions.

Build with `npm.cmd --prefix website run docs:build`. Browser regression checks
are in `website/scripts/check-gantt.mjs`; they expect the dev server on port 4173
and a dedicated headless Chrome instance with remote debugging on port 9231.
They verify every visible activity's grid span, both complete week sequences,
member filtering, tooltips, keyboard tabs, mobile overflow and light/dark themes.
