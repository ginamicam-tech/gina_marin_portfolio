# Gina Marín — Jekyll content

All projects, research entries and artworks live together as individual Markdown files. Content files contain YAML metadata and Markdown only. Templates control rendering; styling has not been redesigned.

## Structure

```text
content/
  _pages/           Home, About, Contact, Work and supporting overview pages
  _work/            One .md file per project, research entry or artwork
  _data/
    navigation.yml  Work, About, Contact (the wordmark links Home)
  media/            Images, videos and caption tracks
_layouts/
  default.html      Shared document, navigation and footer
  page.html         Pages and configurable work lists
  work.html         A project, research entry or artwork
_includes/
  work-list.html    Shared selection and list rendering
  media.html        Shared image, caption and video markup
  content.html      Base-path handling for Markdown links
  redirect.html     Compatibility for old page URLs
assets/             Existing template CSS and favicon
_site/              Generated output — never edit this
```

There are currently **56 entries**: 16 projects, 3 research entries, 34 artworks and 3 series. BODY.INTERFACE is the research parent of Clinical Fold and Self Archive. CARE LAB and its Human Warmth installation have separate entries, linked through `parent: care-lab` and links in their text. The Work page shows projects, research and series, with tag filters. Each artwork has its own year, technique, dimensions, image and series.

## Edit or add an entry

Edit a file under `content/_work/`, or duplicate one and give it a unique `key` and `permalink`. The filename is for organisation; the permalink preserves the public URL.

```yaml
---
key: care-lab
card_label: CARE LAB
name: CARE LAB
title: CARE LAB
type: project
tags:
  - participation
  - installation
  - learning
year: 2026
featured: true
order: 1
permalink: /work/care-lab/
role: Installation designer & facilitator
cover:
  src: /content/media/care-lab/care-print.jpg
  alt: A red CARE bandage print suspended in the festival space
---
```

Write the body as Markdown below the closing `---`.

- `type`: `project`, `research`, `artwork` or `series`.
- `tags`: reusable thematic categories, using consistent lowercase labels.
- `parent`: the stable `key` of a parent entry, when applicable.
- `series`: artwork grouping (`body-interface`, `chromatic-body`, `optical-pulse`).
- `order`: default list order; every entry has a numeric value.
- `featured`: selects entries for the homepage grid and carousel; the Work index includes featured and non-featured entries.
- `year`: taken from existing documentation where available; for projects it may be the first year of an activity spanning several years.
- `context`, `role`, `technique`, `dimensions`: facts displayed by the entry template.
- `cover`, `media`: image/video data rendered by the shared media template.
- `archive_notes`: original supplementary archive text, retained once with its project.
- `legacy_anchors`: compatibility for links from the former long artwork and research pages.

Keep prose in Markdown and facts in YAML. No HTML, Liquid includes or CSS belongs in these files. Layout defaults are configured centrally in `_config.yml`.

## Lists on pages

Pages select work through YAML. The current Work page uses:

```yaml
work_lists:
  - sort: order
```

That lists **all entries**, including projects, research and artworks. An example of a filtered list elsewhere:

```yaml
work_lists:
  - tags: [participation, installation]
    match: any
    sort: year
    reverse: true
    limit: 3
```

Supported selectors: `type`, `tags`, `match` (`any` by default, or `all`), `series`, `parent`, `featured`, `sort`, `reverse`, and `limit`. Multiple selectors combine as AND. Multiple lists can be configured in `work_lists`. The templates decide where and how they appear.

Studio, Artworks and Exhibitions have been removed. Their practice and series descriptions are in About; individual entries remain in Work. No redirects are provided for these removed pages or the old Practice alias. The profile and project contributions have been updated using Gina’s 2026 CV, alongside the existing project archive.

## Old URLs

Retained project URLs are preserved, even where they begin with `/portfolio/`. Duplicate overview pages redirect: `/portfolio/` → `/work/`, `/profile/` → `/about/`. The research material is consolidated into BODY.INTERFACE and its children; `/research/` redirects to `/work/body-interface/`. Redirect templates retain URL fragments and provide a plain link without JavaScript.

## Run locally

```sh
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
cd /Users/madshobye/Media/codeRepo/ginewebsite/gina_marin_portfolio
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --baseurl ""
```

Open http://localhost:4000. **Restart an already-running Jekyll server after this collection change**, because `_config.yml` is not reloaded automatically.

### Preview optimized images

```sh
bash scripts/preview-optimized.sh
```

This builds a temporary copy, runs the same image optimizer as GitHub Actions, checks its links and serves it at http://127.0.0.1:4001. Original images and the normal development server remain unchanged. Stop with Ctrl+C; rerun after edits to rebuild. Requires the Ruby dependencies above and Python 3.10 or newer. Pillow is installed in a temporary environment if needed. Set `PYTHON` to choose an interpreter or `PORT` to choose another port.

## Verify

```sh
bundle exec jekyll build
python3 scripts/validate-content.py _site
ruby scripts/validate-work.rb
```

Checks cover the 24 retained routes, all 51 work entries, unique keys/URLs, parent references, all-entry index, local media, links and fragments, and the absence of HTML/Liquid in content. `scripts/migration.json` records the original route-to-source mapping.

## GitHub Pages

Use this folder as the repository root, including `.github/`. Configure `url` and `baseurl` in `_config.yml`, select **Settings → Pages → Source → GitHub Actions**, and push to `main`. The workflow takes its hosting prefix from GitHub Pages. Nothing has been published by this restructuring.

Navigation is Work · About · Contact, with the name linking to Home. “How I work” follows selected projects on the homepage and also appears on About. Both use the three areas in `content/_data/work_filters.yml` and link directly to the matching Work filter. About has a short profile and links to `/cv/`, which contains education, experience, artistic projects, skills and languages. The Services page and its former subpages have been removed without redirects.

## Covers and square grids

Every page and work entry has a `cover` image in its YAML. The template displays it at full viewport height, with navigation over the image and content below. Existing work images are also retained uncropped in the body. Missing images use `content/media/placeholder.png` (the supplied white XX on black).

```yaml
cover:
  src: /content/media/example.jpg
  alt: Description of the image
  position: 50% 50%
thumbnail:
  src: /content/media/example-detail.jpg
  position: 50% 50%
```

`position` is optional and controls the crop focal point. `thumbnail` is optional; square listing cards use the cover by default. Listing grids adapt from three columns to two and then one on small screens. The homepage's `featured_work` selects entries with `featured: true`, using the same card template as Work. Cards show one compact context line followed by the full question (or title). Every work record has a `card_label` and numeric `year`. The card always renders context first and year last; these are not inferred from the title or question. Artwork series also have `year_start` for their displayed range, while `year` remains the latest year for sorting. Human Warmth uses `card_label: Art installation`. `work_intro` and `after_work_sections` hold the surrounding Markdown.

## Homepage featured carousel

The homepage cover uses work entries with `featured: true` (currently six), sorted by `order` (lowest first). Each slide takes its image and focal point from `cover`, its heading from `question` (falling back to `name` or `title`), and its short description from `summary` (falling back to `listing_context` or `title`). The entire image and caption link to the project. Update those fields in the work Markdown files to curate the carousel. Navigation is manual, with previous/next buttons, keyboard arrows and native touch swiping; there is no automatic rotation. With no featured entries, the normal homepage cover is shown.

## Work filters

Work has no cover image. Its filter buttons are configured in `content/_data/work_filters.yml`, where each broad label maps to existing work tags (any matching tag includes an entry). A work entry can appear in several filters. To explicitly assign an entry, set `filter_groups: [art-research]` (or other filter IDs) in its front matter; this overrides tag matching for the Work filters while preserving its thematic tags. Each area has a short `summary` for Home/About and a Markdown `description` displayed above its filtered results. Links use `/work/?filter=projects-production#work-filters` (or `art-research` / `design-communication`); selection updates the URL and supports browser back/forward. Filtering preserves the newest-first year order and All restores the complete list. Without JavaScript, all entries remain visible.

## Artwork series

The Work index shows projects, research and three series cards (22 cards total). Individual artworks remain in their original Markdown files and URLs. Each series has one Markdown file in `content/_work/`, such as `body-interface-series.md`. Its body is the introduction; its YAML supplies the card/cover and gallery selection:

```yaml
type: series
work_lists:
  - type: artwork
    series: body-interface
    sort: year
    reverse: true
    details: true
```

The gallery finds artworks with the matching `series` field automatically and shows their title, year, technique and dimensions. Clicking a card opens the individual artwork with its full image. Set the series entry's `year` to the latest artwork year for its position on Work, and update `listing_context` if the date range changes. The series cards retain artwork tags, so they appear under Art & Research. The separate BODY.INTERFACE research entry remains separate from the Body Interface drawing series.

The Work page uses `exclude_type: artwork` to show series instead of individual artworks; other lists can still select artworks directly. The work validator checks that all artworks appear in exactly one series gallery and both galleries and Work are sorted newest first.

## Two-column content

The homepage introduction has the name/title on the left and its Markdown body on the right. Everywhere else, text flows down the first column and continues into the second, with headings kept in the text. Columns stack on mobile.

Sections are plain Markdown strings in YAML:

```yaml
sections:
  - layout: newspaper
    text: |
      ## About the project

      Project description with **Markdown formatting**.

      ## My part

      Description of my contribution.
  - layout: full-width
    text: |
      A section that needs the full width.
```

The homepage uses `after_work_sections` for text after selected projects, and `work_areas: true` adds the shared three-area overview. About uses the same overview and links to the detailed CV in `content/_pages/cv.md`. Supplemental archive text uses `archive_sections` with the same structure. Layout stays in templates and CSS; text does not need manual left/right splits. Listing grids show three cards per row on desktop, two on tablet and one on mobile. Media grids use two columns, while full artwork images remain uncropped.

## CV content

### Work and image credits

Every Work entry records known authorship. Individual artworks use `artist`; projects and series can use a `credits` list with `role`, `name` and an optional `url`. Detailed collective credit sections can remain in Markdown. Use `credit_note` for necessary context, such as archive photographs predating Gina’s involvement.

Images and videos support `credit` alongside `caption`, plus an optional `source_url`. These appear together beneath the gallery item. If a credited cover is hidden from the gallery, also include its attribution in the project credits so it remains visible. Credit the photographer separately from the artist, designer, editor or commissioning organisation.

The evidence and unresolved attributions from the October 2026 review are in `scripts/credits-audit.json`, which is excluded from the published site. Do not infer a photographer from adjacent images or invent missing credits. Supplied CV dates and wording remain authoritative for Gina’s roles.

`content/_pages/cv.md` is the dedicated CV, linked from About. It is plain Markdown with YAML page metadata. The supplied 2026 CV is the source for the updated roles and dates; additional existing portfolio records are retained. Xplore (Rituals of Collective Descent, Berlin) and HOP (The Poetics of the Collective, Copenhagen) are separate 2026 entries. HOP uses the supplied photograph without typography as its cover and the full event poster as documentation.

### Thesis documentation

The BODY.INTERFACE page contains an English summary of **IN/Pressions of a Body. Interface: Poetics, Clinical Practice, and Its Symbolic Activation in the Age of Liquid Architecture.** Clinical Fold and Self Archive have their own descriptions, photographs and credits. Five earlier projects are also separate Work entries: IN_Huellas, IN_Desterritorio, IN_Cavilaciones, IN_Plano Metamórfico and IN_Resonancia Corpórea. Related existing artwork records link to the project documentation rather than being duplicated.

Only selected extracted images are stored in `content/media/thesis/`. The source thesis and presentation PDFs stay outside the repository. Source identities and the deliberately retained CV wording/date differences are recorded in `content/_data/research_sources.yml`; each research entry's `documentation_sources` records the relevant PDF pages. Artwork catalogue dates have not been inferred from dates of the broader projects.

About's optional `portrait` YAML field displays a small, uncropped image beside its introduction. About, CV and Contact covers use graphics from the supplied material. All list thumbnails crop to fill their square. Use `thumbnail.position` to adjust the focal point; full artwork images remain uncropped on individual pages.
