# Gina Marín: editable PDF portfolio

The PDF is authored from the existing work collection, with a separate editorial layer. It does not print the website.

## Choose pages

Edit `portfolio/outline.yml`:

- Each project appears in exactly one section.
- Set `include: false` to omit a project from an application edition.
- Move a project row to reorder it or assign it to another section. Do not copy it: the build rejects duplicates.
- The complete edition includes all 34 non-artwork work records. The 34 individual artwork records are represented by their three series, with selected works and titles.
- The contents page and page numbers update automatically.
- Edit the cover, introductory text and concise CV in this file.

The full category descriptions come from `content/_data/work_filters.yml`, keeping them consistent with the website. Each category has its own opening page.

## Edit a project page

Each `content/_work/*.md` project has a `portfolio_pdf` block:

- `category`: recommended primary category. The outline controls final placement.
- `layout: project`: an image-led landscape page.
- `summary`: condensed editorial text specifically for the PDF.
- `images`: one to three selected source files, in order, with captions. Use `fit: contain`; whole images are shown without cropping. Do not use the padded list thumbnails.
- `credits`: concise authorship and collaboration information for the selected documentation.

Title, year, context, role and live project URL come directly from the work record. Images stay at their original resolution on disk; the PDF embeds compressed copies. Captions distinguish proposals, visualisations and mockups from realised work. Videos remain available through clickable project links.

## Build

Use Python 3.12 or later:

```sh
python3 -m venv .venv-portfolio
.venv-portfolio/bin/pip install -r portfolio/requirements.txt
.venv-portfolio/bin/python scripts/build-portfolio.py
```

The script locates DejaVu fonts in the Codex bundled runtime or Linux's standard font directory. Else set `PORTFOLIO_FONT_DIR` to a directory containing `DejaVuSans.ttf`, `DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`.

Outputs:

- `output/pdf/gina-marin-portfolio.pdf`
- `output/pdf/portfolio-manifest.yml`: page numbers, primary categories, source images and URLs.

For another application, copy the outline and use:

```sh
python scripts/build-portfolio.py --outline portfolio/application.yml --output output/pdf/application.pdf
```

The generator checks duplicate project keys, missing assets, text overflow and project titles in the exported PDF. Always render and visually review a new edition after changing text or image selection. The 40-page complete edition is a master portfolio; switch off pages for applications with tighter limits. Links point to the public website, so new project pages must be deployed before external distribution.

The short CV is an editorial selection, not a replacement for the website CV. No unverified photography credits are added. All source originals are retained. `portfolio`, `output` and `tmp` are excluded from Jekyll publishing.
